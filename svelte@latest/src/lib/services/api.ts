// src/lib/services/api.ts

/**
 * @file api.ts
 * @description Centralized API request handler with token refresh logic.
 */

import { authStore, type AuthState } from '$lib/store/authStore';
import { get } from 'svelte/store';
import { goto } from '$app/navigation'; // For redirecting to login

// 避免循环依赖问题
// 我们将使用一个简单的方法来解决循环依赖问题
// 不直接导入 authService，而是通过回调函数来处理 token 刷新
// 这个函数将在 authService 中被设置
let refreshTokenCallback: (() => Promise<string | null>) | null = null;

// 设置 token 刷新回调函数
export function setRefreshTokenCallback(callback: () => Promise<string | null>) {
  refreshTokenCallback = callback;
  console.log('API Service: Token refresh callback set');
}

// 确保 BASE_URL 有一个默认值，即使环境变量未定义
// When using Vite proxy, we use a relative URL to avoid CORS issues
const BASE_URL: string = import.meta.env.VITE_API_BASE_URL || '/api/v1';

console.log('API Service: Using BASE_URL:', BASE_URL);

export interface ApiError extends Error {
  response?: Response;
  status?: number;
  data?: any;
}

// Variable to prevent infinite refresh token loops
let isRefreshing = false;
// Queue for requests that failed due to 401 and are waiting for token refresh
let failedQueue: Array<{resolve: (value: any) => void, reject: (reason?: any) => void, config: RequestConfig}> = [];

interface RequestConfig {
  endpoint: string;
  method: string;
  body: Record<string, any> | null;
  requiresAuth: boolean;
  customHeaders: Record<string, string>;
  isRetry?: boolean; // Flag to indicate if this is a retried request
}

function processQueue(error: ApiError | null, token: string | null = null) {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else if (token) { // If token is successfully refreshed
      // Update header for the retried request (not strictly needed if original request function re-fetches token)
      // prom.config.customHeaders['Authorization'] = `Bearer ${token}`; // This might be tricky
      // Re-request with the original config, now that token is refreshed
      // The 'request' function will pick up the new token from the store
      request(prom.config.endpoint, prom.config.method, prom.config.body, prom.config.requiresAuth, prom.config.customHeaders, true)
        .then(prom.resolve)
        .catch(prom.reject);
    }
  });
  failedQueue = [];
}


async function request<T = any>(
  endpoint: string,
  method: string,
  body: Record<string, any> | null = null,
  requiresAuth: boolean = true,
  customHeaders: Record<string, string> = {},
  isRetry: boolean = false // Added isRetry flag
): Promise<T> {
  const configArgs: RequestConfig = { endpoint, method, body, requiresAuth, customHeaders, isRetry };

  const url = `${BASE_URL}${endpoint}`;
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...customHeaders,
  };

  const currentAuth: AuthState = get(authStore);

  if (requiresAuth && currentAuth && currentAuth.accessToken) {
    headers['Authorization'] = `Bearer ${currentAuth.accessToken}`;
  } else if (requiresAuth && (!currentAuth || !currentAuth.accessToken) && !isRefreshing) {
    // If auth is required, no token, and not currently refreshing, likely needs login
    console.warn(`Authenticated request to ${url} without an access token and not refreshing.`);
    // This case might lead to an immediate 401 which then triggers refresh logic
  }

  const config: RequestInit = {
    method,
    headers,
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  try {
    // Log the request for debugging
    console.log(`API Request: ${method} ${url}`, body ? { body } : '');
    console.log(`API Request Headers:`, headers);

    const response: Response = await fetch(url, config);
    console.log(`API Response Status: ${response.status} ${response.statusText}`);

    // Handle redirects (308 Permanent Redirect, 307 Temporary Redirect)
    if (response.status === 308 || response.status === 307) {
      console.warn(`Redirect detected (${response.status}) for ${url}. Following redirect...`);
      const redirectUrl = response.headers.get('Location');
      if (redirectUrl) {
        console.log(`Redirect URL: ${redirectUrl}`);

        // Extract the relative path or use the full URL as needed
        let redirectEndpoint;
        let useFullUrl = false;

        // Handle full URLs
        if (redirectUrl.startsWith('http')) {
          try {
            const urlObj = new URL(redirectUrl);
            // Extract the path portion, e.g., /api/v1/achievements/
            const pathname = urlObj.pathname;

            // If the path starts with /api/v1/, remove that prefix for our endpoint
            if (pathname.startsWith('/api/v1/')) {
              redirectEndpoint = pathname.substring('/api/v1'.length);
            } else {
              // For other paths, use the full URL
              redirectEndpoint = redirectUrl;
              useFullUrl = true;
            }
          } catch (e) {
            console.error('Error parsing redirect URL:', e);
            redirectEndpoint = redirectUrl;
            useFullUrl = true;
          }
        } else if (redirectUrl.startsWith(BASE_URL)) {
          // If it's relative to BASE_URL
          redirectEndpoint = redirectUrl.substring(BASE_URL.length);
        } else {
          // For other relative URLs
          redirectEndpoint = redirectUrl;
        }

        console.log(`Following redirect to endpoint: ${redirectEndpoint} (useFullUrl: ${useFullUrl})`);

        // For full URLs, make a direct fetch request
        if (useFullUrl) {
          console.log(`Making direct fetch to: ${redirectEndpoint}`);
          const directResponse = await fetch(redirectEndpoint, {
            method,
            headers,
            ...(body ? { body: JSON.stringify(body) } : {})
          });

          if (directResponse.status === 204) {
            return null as T;
          }

          const contentType = directResponse.headers.get('content-type');
          if (contentType && contentType.includes('application/json')) {
            return await directResponse.json();
          } else {
            return await directResponse.text() as unknown as T;
          }
        }

        // For relative endpoints, use our request function
        return request(redirectEndpoint, method, body, requiresAuth, customHeaders, isRetry);
      }
    }

    if (response.status === 204) {
      return null as T;
    }

    let responseData: any;
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      responseData = await response.json();
    } else {
      responseData = await response.text() || response.statusText || null;
    }

    if (!response.ok) {
      console.error(`API Error: ${method} ${url} returned ${response.status} ${response.statusText}`);
      console.error('API Error Response Data:', responseData);

      const error: ApiError = new Error(
        responseData?.message || response.statusText || 'API Request Failed'
      );
      error.response = response;
      error.status = response.status;
      error.data = responseData;

      // 添加更多调试信息
      console.error('API Error Object:', {
        status: error.status,
        message: error.message,
        data: error.data,
        url: url,
        method: method
      });

      throw error; // Throw error to be caught by the catch block
    }

    return responseData as T;
  } catch (error: any) {
    const originalRequestConfig: RequestConfig = configArgs;
    // Check if it's a 401 error, not a retry, and auth is required
    if (error.status === 401 && !originalRequestConfig.isRetry && originalRequestConfig.requiresAuth) {
      console.log('API: 401 Unauthorized error detected for', originalRequestConfig.endpoint);
      console.log('API: isRetry =', originalRequestConfig.isRetry, 'requiresAuth =', originalRequestConfig.requiresAuth);

      if (!isRefreshing) {
        console.log('API: Starting token refresh process');
        isRefreshing = true;
        try {
          console.log('API: Access token expired or invalid. Attempting to refresh...');

          if (!refreshTokenCallback) {
            console.error('No refresh token callback set. Cannot refresh token.');
            // 如果没有设置回调函数，直接重定向到登录页面
            authStore.logout();
            if (typeof window !== 'undefined') goto('/login');
            throw error;
          }

          const newAccessToken = await refreshTokenCallback(); // This should update the store
          if (newAccessToken) {
            console.log('Token refreshed successfully. Retrying original request and processing queue.');
            // The store is updated by refreshAccessToken, so subsequent calls to get(authStore) will have the new token.
            processQueue(null, newAccessToken); // Process queued requests with new token
            // Retry the original request. The `request` function will pick up the new token from the store.
            return request(
              originalRequestConfig.endpoint,
              originalRequestConfig.method,
              originalRequestConfig.body,
              originalRequestConfig.requiresAuth,
              originalRequestConfig.customHeaders,
              true // Mark as retry
            );
          } else {
            // Refresh failed, newAccessToken is null. authService.refreshAccessToken should have handled logout.
            console.error('Failed to refresh token, newAccessToken is null. User should be logged out.');
            processQueue(error, null); // Reject queued requests
            // authService.refreshAccessToken or authStore.logout should handle redirect
            // If not, uncomment:
            // if (typeof window !== 'undefined') goto('/login');
            throw error; // Re-throw original 401 error or a new "session expired" error
          }
        } catch (refreshError: any) {
          console.error('Error during token refresh process:', refreshError);
          processQueue(refreshError, null); // Reject queued requests with refresh error
          // authService.refreshAccessToken or authStore.logout should handle redirect
          // If not, uncomment:
          // if (typeof window !== 'undefined') authStore.logout(); // Ensure logout
          // if (typeof window !== 'undefined') goto('/login');
          throw refreshError; // Re-throw the error from the refresh attempt
        } finally {
          isRefreshing = false;
        }
      } else {
        // Is already refreshing, queue this request
        console.log('Token refresh in progress. Queuing request to:', originalRequestConfig.endpoint);
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject, config: originalRequestConfig });
        });
      }
    }

    // For non-401 errors or if it's a retry that failed again
    console.error(`API Error (${method} ${endpoint}):`, error.status, error.message, error.data || error);
    throw error;
  }
}

export const api = {
  get: <T = any>(endpoint: string, requiresAuth: boolean = true, customHeaders: Record<string, string> = {}): Promise<T> =>
    request<T>(endpoint, 'GET', null, requiresAuth, customHeaders),
  post: <T = any>(endpoint: string, body: Record<string, any>, requiresAuth: boolean = true, customHeaders: Record<string, string> = {}): Promise<T> =>
    request<T>(endpoint, 'POST', body, requiresAuth, customHeaders),
  put: <T = any>(endpoint: string, body: Record<string, any>, requiresAuth: boolean = true, customHeaders: Record<string, string> = {}): Promise<T> =>
    request<T>(endpoint, 'PUT', body, requiresAuth, customHeaders),
  delete: <T = any>(endpoint: string, requiresAuth: boolean = true, customHeaders: Record<string, string> = {}): Promise<T> =>
    request<T>(endpoint, 'DELETE', null, requiresAuth, customHeaders),
  patch: <T = any>(endpoint: string, body: Record<string, any>, requiresAuth: boolean = true, customHeaders: Record<string, string> = {}): Promise<T> =>
    request<T>(endpoint, 'PATCH', body, requiresAuth, customHeaders),
};
