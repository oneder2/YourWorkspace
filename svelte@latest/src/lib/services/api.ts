// src/lib/services/api.ts

/**
 * @file api.ts
 * @description Centralized API request handler for the SvelteKit application (TypeScript version).
 * This module provides a wrapper around the native `fetch` API to streamline
 * interactions with the backend, including base URL management,
 * automatic JSON parsing, Authorization header injection, and basic error handling.
 */

import { authStore, type AuthState } from '$lib/store/authStore'; // 我们很快会创建这个 store
import { get } from 'svelte/store'; // 用于读取 store 的值

// 从环境变量中获取 API 基础 URL
// 请确保您的 .env 文件中定义了 VITE_API_BASE_URL (例如 VITE_API_BASE_URL=http://localhost:5000/api/v1)
const BASE_URL: string = import.meta.env.VITE_API_BASE_URL;

if (!BASE_URL) {
  console.warn(
    'VITE_API_BASE_URL is not defined in your .env file. API calls may fail.'
  );
}

/**
 * 定义 API 错误对象的结构
 */
export interface ApiError extends Error {
  response?: Response;
  status?: number;
  data?: any; // 后端返回的错误数据
}

/**
 * 执行 API 请求.
 * @param endpoint - API 端点 (例如, '/auth/login').
 * @param method - HTTP 方法 (GET, POST, PUT, DELETE, etc.).
 * @param body - POST/PUT 请求的请求体 (可选).
 * @param requiresAuth - 请求是否需要认证 Token (可选, 默认为 true).
 * @param customHeaders - 自定义请求头 (可选).
 * @returns {Promise<T>} - 返回一个 Promise，解析为 JSON 响应或因错误而拒绝.
 */
async function request<T = any>( // T 是期望的响应数据类型
  endpoint: string,
  method: string,
  body: Record<string, any> | null = null,
  requiresAuth: boolean = true,
  customHeaders: Record<string, string> = {}
): Promise<T> {
  const url = `${BASE_URL}${endpoint}`;
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...customHeaders,
  };

  // 获取 authStore 的当前状态
  const currentAuth: AuthState = get(authStore);

  if (requiresAuth && currentAuth && currentAuth.accessToken) {
    headers['Authorization'] = `Bearer ${currentAuth.accessToken}`;
  } else if (requiresAuth && (!currentAuth || !currentAuth.accessToken)) {
    console.warn(`Attempting to make an authenticated request to ${endpoint} without an access token.`);
  }

  const config: RequestInit = {
    method,
    headers,
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  try {
    const response: Response = await fetch(url, config);

    if (response.status === 204) { // 处理 204 No Content
      return null as T; // 或者一个空对象, 取决于您如何处理 204
    }

    let responseData: any;
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      responseData = await response.json();
    } else {
      responseData = await response.text() || response.statusText || null;
    }

    if (!response.ok) {
      const error: ApiError = new Error(
        responseData?.message || response.statusText || 'API Request Failed'
      );
      error.response = response;
      error.status = response.status;
      error.data = responseData; // 附加解析后的 JSON 错误数据
      throw error;
    }

    return responseData as T;
  } catch (error: any) {
    console.error(`API Error (${method} ${endpoint}):`, error.status, error.message, error.data || error);
    // 重新抛出错误，以便调用它的服务或组件可以捕获它
    throw error;
  }
}

// 常用 HTTP 方法的便捷函数
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

