/**
 * @file apiClient.ts
 * @description API client for making HTTP requests to the backend
 */

import { authStore } from '$lib/store/authStore';
import { get } from 'svelte/store';

// Simple fetch-based API client
const createApiClient = () => {
  const baseURL = import.meta.env.VITE_API_URL || '/api';

  const request = async (method: string, url: string, data?: any) => {
    // Get the current auth state
    const authState = get(authStore);

    // Prepare headers
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // If there's a token, add it to the request headers
    if (authState.token) {
      headers.Authorization = `Bearer ${authState.token}`;
    }

    try {
      // Prepare request options
      const options: RequestInit = {
        method,
        headers,
      };

      // Add body for POST, PUT, PATCH requests
      if (data && ['POST', 'PUT', 'PATCH'].includes(method)) {
        options.body = JSON.stringify(data);
      }

      // Make the request
      const response = await fetch(`${baseURL}${url}`, options);

      // Handle 401 Unauthorized errors
      if (response.status === 401) {
        authStore.logout();
        throw new Error('Unauthorized');
      }

      // Parse the response
      const responseData = await response.json();

      // Return the response data
      return { data: responseData };
    } catch (error) {
      console.error(`API ${method} request failed:`, error);
      throw error;
    }
  };

  return {
    get: (url: string) => request('GET', url),
    post: (url: string, data: any) => request('POST', url, data),
    put: (url: string, data: any) => request('PUT', url, data),
    delete: (url: string) => request('DELETE', url),
  };
};

const apiClient = createApiClient();

// Mock API implementation for development
const useMockApi = true; // Set to false to use real API

// Create a mock API client that returns fake data
const mockApiClient = {
  get: async (url: string) => {
    console.log(`Mock GET request to ${url}`);

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Return mock data based on the URL
    if (url === '/anchor/profile') {
      return {
        data: {
          id: 1,
          username: 'testuser',
          email: 'test@example.com',
          professional_title: 'Software Developer',
          one_liner_bio: 'Passionate about building great software',
          skill: 'JavaScript, TypeScript, Svelte, React, Node.js',
          summary: 'Experienced software developer with a focus on frontend technologies.'
        }
      };
    }

    // Default response
    return { data: {} };
  },

  post: async (url: string, data: any) => {
    console.log(`Mock POST request to ${url}`, data);

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Return mock data based on the URL
    if (url === '/auth/login') {
      return {
        data: {
          token: 'mock-jwt-token',
          user: {
            id: 1,
            username: 'testuser',
            email: 'test@example.com'
          }
        }
      };
    }

    // Default response
    return { data: { ...data, id: Math.floor(Math.random() * 1000) } };
  },

  put: async (url: string, data: any) => {
    console.log(`Mock PUT request to ${url}`, data);

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Return mock data based on the URL
    if (url === '/anchor/profile') {
      return {
        data: {
          id: 1,
          username: 'testuser',
          email: 'test@example.com',
          ...data
        }
      };
    }

    // Default response
    return { data: { ...data, id: 1 } };
  },

  delete: async (url: string) => {
    console.log(`Mock DELETE request to ${url}`);

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Default response
    return { data: { success: true } };
  }
};

// Export the appropriate client based on the useMockApi flag
const client = useMockApi ? mockApiClient : apiClient;
export { client as apiClient };
