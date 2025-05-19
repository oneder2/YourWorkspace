// src/lib/services/authService.ts

/**
 * @file authService.ts
 * @description Service layer for handling all authentication-related API interactions.
 * It uses the generic `api` service for making HTTP requests and updates the
 * `authStore` with the authentication state and user profile.
 */

import { api, type ApiError, setRefreshTokenCallback } from './api';
import { authStore, type UserProfile, type AuthState } from '$lib/store/authStore';
import { get } from 'svelte/store'; // Import get for synchronously reading store values

// Define interfaces for request payloads based on your API documentation
// (prompts/frontend/phase1.txt)

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
}

export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
}

export interface RegisterResponse {
  message: string;
  user: {
    id: number;
    username: string;
    email: string;
    created_at: string;
  };
}

export interface ChangePasswordPayload {
  new_password: string;
}

/**
 * Logs in a user with the provided credentials.
 * On success, updates the authStore with tokens and fetches user profile.
 * @param credentials - The user's login credentials (email and password).
 * @returns {Promise<void>}
 * @throws {ApiError} If login fails.
 */
async function loginUser(credentials: LoginCredentials): Promise<void> {
  console.log('AuthService: loginUser called with email:', credentials.email);

  try {
    console.log('AuthService: Sending login request to API');
    const response = await api.post<LoginResponse>('/auth/login', credentials, false); // Login doesn't require auth initially
    console.log('AuthService: Login API response received:', response);

    if (response.access_token && response.refresh_token) {
      console.log('AuthService: Login successful, storing tokens');
      // Store tokens and then fetch user profile
      authStore.login({ access_token: response.access_token, refresh_token: response.refresh_token });

      console.log('AuthService: Fetching user profile');
      await fetchUserProfile(); // Fetch and store user profile after successful login
      console.log('AuthService: User profile fetched and stored');
    } else {
      console.error('AuthService: Login response did not include tokens');
      throw new Error('Login response did not include tokens.');
    }
  } catch (error) {
    console.error('AuthService: Login failed', error);

    // 添加更详细的错误日志
    if (error instanceof Error) {
      console.error('AuthService: Error details:', {
        message: error.message,
        stack: error.stack,
        name: error.name
      });
    }

    authStore.logout(); // Ensure state is cleared on failed login
    throw error; // Re-throw the error for the UI to handle
  }
}

/**
 * Registers a new user.
 * @param userData - The data for the new user (username, email, password).
 * @returns {Promise<RegisterResponse>} The registration success response.
 * @throws {ApiError} If registration fails.
 */
async function registerUser(userData: RegisterPayload): Promise<RegisterResponse> {
  try {
    console.log('AuthService: Starting user registration process');

    // 验证输入数据
    if (!userData.username || !userData.email || !userData.password) {
      console.error('AuthService: Missing required registration fields');
      throw new Error('Missing required fields (username, email, password)');
    }

    // 确保密码长度符合要求
    if (userData.password.length < 8) {
      console.error('AuthService: Password too short');
      throw new Error('Password must be at least 8 characters long');
    }

    // Registration does not require auth
    console.log('AuthService: Sending registration request to API');
    const response = await api.post<RegisterResponse>('/auth/register', userData, false);

    console.log('AuthService: Registration successful', {
      userId: response.user?.id,
      username: response.user?.username,
      message: response.message
    });

    return response;
  } catch (error) {
    console.error('AuthService: Registration failed', error);

    // 增强错误信息
    if (error instanceof Error) {
      console.error('AuthService: Error details:', {
        message: error.message,
        stack: error.stack,
        name: error.name
      });

      // 如果是 ApiError，添加更多详细信息
      const apiError = error as ApiError;
      if (apiError.status) {
        console.error('AuthService: API error details:', {
          status: apiError.status,
          data: apiError.data
        });
      }
    }

    throw error;
  }
}

/**
 * Fetches the profile of the currently authenticated user.
 * Updates the authStore with the user's profile information.
 * @returns {Promise<UserProfile | null>} The user profile or null if fetch fails.
 * @throws {ApiError} If fetching profile fails (e.g., due to invalid token).
 */
async function fetchUserProfile(): Promise<UserProfile | null> {
  console.log('AuthService: fetchUserProfile called');

  try {
    console.log('AuthService: Sending request to /auth/me endpoint');
    // Requires auth (access token will be automatically attached by api.ts)
    const userProfile = await api.get<UserProfile>('/auth/me');
    console.log('AuthService: User profile received:', userProfile);

    if (userProfile) {
      console.log('AuthService: Setting user profile in authStore');
      authStore.setUserProfile(userProfile);
      return userProfile;
    }

    console.log('AuthService: No user profile received');
    return null;
  } catch (error: any) {
    console.error('AuthService: Failed to fetch user profile', error);

    // 添加更详细的错误日志
    if (error.status) {
      console.error('AuthService: Error status:', error.status);
    }

    if (error.data) {
      console.error('AuthService: Error data:', error.data);
    }

    if (error instanceof Error) {
      console.error('AuthService: Error details:', {
        message: error.message,
        stack: error.stack,
        name: error.name
      });
    }

    if (error.status === 401 || error.status === 422) {
        console.log('AuthService: Unauthorized or invalid token, logging out');
        authStore.logout();
    }

    throw error;
  }
}

/**
 * Logs out the currently authenticated user.
 * This involves revoking the access token on the server and clearing local auth state.
 * @returns {Promise<void>}
 * @throws {ApiError} If logout fails on the server side.
 */
async function logoutUser(): Promise<void> {
  try {
    const currentAuthState = get(authStore); // Use get() for synchronous access

    if (currentAuthState.accessToken) {
        await api.post('/auth/logout', {}, true); // Revoke access token
    }

    // Optional: Revoke refresh token if API and api.ts support it easily.
    // As discussed, /auth/logout-refresh needs the refresh token in the Bearer header.
    // if (currentAuthState.refreshToken) {
    //   // Special call needed here, similar to refreshAccessToken logic
    // }

  } catch (error) {
    console.error('AuthService: Server logout failed (access token revocation)', error);
    // Do not re-throw, client-side logout should still proceed.
  } finally {
    authStore.logout(); // Always clear local authentication state
  }
}

/**
 * Changes the password for the currently authenticated user.
 * Requires a "fresh" access token (obtained directly from login).
 * @param payload - Object containing the new_password.
 * @returns {Promise<{ message: string }>} Success message.
 * @throws {ApiError} If password change fails.
 */
async function changePassword(payload: ChangePasswordPayload): Promise<{ message: string }> {
  try {
    const response = await api.post<{ message: string }>('/auth/change-password', payload, true);
    return response;
  } catch (error) {
    console.error('AuthService: Change password failed', error);
    throw error;
  }
}

/**
 * Refreshes the access token using the refresh token.
 * @returns {Promise<string | null>} The new access token or null if refresh fails.
 * @throws {ApiError} If token refresh fails.
 */
async function refreshAccessToken(): Promise<string | null> {
  const currentAuthState = get(authStore); // Use get() for synchronous access

  if (!currentAuthState.refreshToken) {
      console.warn('AuthService: No refresh token available to refresh access token.');
      authStore.logout(); // No way to recover session if refresh token is missing
      return null;
  }

  try {
    // The /auth/refresh endpoint expects the Refresh Token in the Bearer header.
    // We make a direct fetch call here, bypassing api.ts's default behavior of sending Access Token.
    const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';
    console.log('AuthService: Refreshing token with URL:', `${BASE_URL}/auth/refresh`);

    const response = await fetch(`${BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${currentAuthState.refreshToken}`,
            'Content-Type': 'application/json', // Though body is empty, Content-Type might be expected
        },
        // 添加重定向跟随
        redirect: 'follow'
        // No body is sent for this specific endpoint as per API spec
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: response.statusText }));
        const error: ApiError = new Error(errorData.message || 'Token refresh failed');
        error.status = response.status;
        error.data = errorData;
        throw error;
    }

    const tokenResponse = await response.json();
    const newAccessToken = tokenResponse.access_token;

    if (newAccessToken) {
      authStore.setTokens({ accessToken: newAccessToken });
      return newAccessToken;
    } else {
      throw new Error('New access token not found in refresh response.');
    }

  } catch (error: any) {
    console.error('AuthService: Failed to refresh access token', error);
    if (error.status === 401 || error.status === 422) { // Unauthorized or Unprocessable (e.g. token revoked/invalid)
      authStore.logout(); // Log out if refresh token is invalid
    }
    throw error; // Re-throw for UI or global error handler
  }
}


export const authService = {
  loginUser,
  registerUser,
  logoutUser,
  fetchUserProfile,
  changePassword,
  refreshAccessToken,
};

// 设置 refreshTokenCallback，解决循环依赖问题
setRefreshTokenCallback(refreshAccessToken);
