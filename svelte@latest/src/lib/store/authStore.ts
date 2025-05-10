// src/lib/store/authStore.ts

/**
 * @file authStore.ts
 * @description Manages user authentication state, including tokens and user profile information.
 * Persists authentication state to localStorage to maintain session across page reloads.
 */

import { writable, type Writable, derived, type Readable } from 'svelte/store';
import { browser } from '$app/environment'; // To check if we are in the browser environment for localStorage

// Define the structure for user profile data
export interface UserProfile {
  id: number | null;
  username: string | null;
  email: string | null;
  // Add any other user-specific fields you expect from the /auth/me endpoint
  // For example: created_at?: string; updated_at?: string;
}

// Define the structure for the authentication state
export interface AuthState {
  user: UserProfile | null;
  accessToken: string | null;
  refreshToken: string | null;
}

// Define the structure for the auth store, including methods
export interface AuthStore extends Writable<AuthState> {
  login: (tokens: { access_token: string; refresh_token: string }, userData?: UserProfile) => void;
  logout: () => void;
  setUserProfile: (userData: UserProfile) => void;
  setTokens: (tokens: { accessToken?: string | null, refreshToken?: string | null }) => void;
  // Potentially add methods for refreshing tokens if handled client-side
  // refreshAccessToken: (newAccessToken: string) => void;
}

// Key for localStorage
const AUTH_STORAGE_KEY = 'app_auth_state';

/**
 * Helper function to get initial state from localStorage.
 * This ensures that the session can be restored if the user previously logged in.
 * @returns {AuthState} The initial authentication state.
 */
function getInitialState(): AuthState {
  if (!browser) {
    // If not in browser (e.g., during SSR), return default initial state
    return {
      user: null,
      accessToken: null,
      refreshToken: null,
    };
  }

  const storedState = localStorage.getItem(AUTH_STORAGE_KEY);
  if (storedState) {
    try {
      const parsedState = JSON.parse(storedState);
      // Basic validation of the stored state
      if (parsedState && typeof parsedState.accessToken === 'string' || parsedState.accessToken === null) {
        return parsedState;
      }
    } catch (error) {
      console.error('Error parsing stored auth state:', error);
      localStorage.removeItem(AUTH_STORAGE_KEY); // Clear corrupted state
    }
  }
  // Default initial state if nothing is stored or if parsing fails
  return {
    user: null,
    accessToken: null,
    refreshToken: null,
  };
}

// Create the underlying writable store with the initial state
const { subscribe, set, update }: Writable<AuthState> = writable<AuthState>(getInitialState());

// Subscribe to changes in the store and update localStorage
if (browser) {
  subscribe((currentState) => {
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(currentState));
  });
}

// --- Store Methods ---

/**
 * Sets user data and tokens upon successful login.
 * @param tokens - Object containing access_token and refresh_token.
 * @param userData - Optional user profile data. If not provided, user might be fetched separately.
 */
function login(tokens: { access_token: string; refresh_token: string }, userData?: UserProfile): void {
  update((state) => ({
    ...state,
    user: userData || state.user, // Keep existing user data if new data isn't provided immediately
    accessToken: tokens.access_token,
    refreshToken: tokens.refresh_token,
  }));
}

/**
 * Clears user data and tokens upon logout.
 */
function logout(): void {
  set({ // Reset to initial empty state
    user: null,
    accessToken: null,
    refreshToken: null,
  });
  if (browser) {
    localStorage.removeItem(AUTH_STORAGE_KEY); // Also clear from localStorage
  }
  // Optionally, you might want to redirect to the login page here
  // import { goto } from '$app/navigation'; goto('/login');
}

/**
 * Updates the user profile information in the store.
 * @param userData - The user profile data.
 */
function setUserProfile(userData: UserProfile): void {
  update((state) => ({
    ...state,
    user: userData,
  }));
}

/**
 * Updates only the tokens in the store.
 * Useful for token refresh mechanisms or if tokens are set separately from user profile.
 * @param tokens - Object containing new accessToken and/or refreshToken.
 */
function setTokens(tokens: { accessToken?: string | null, refreshToken?: string | null }): void {
  update((state) => {
    const newState = { ...state };
    if (tokens.accessToken !== undefined) {
      newState.accessToken = tokens.accessToken;
    }
    if (tokens.refreshToken !== undefined) {
      newState.refreshToken = tokens.refreshToken;
    }
    return newState;
  });
}

// --- Derived Store for isAuthenticated ---
// This provides a convenient way to check if the user is authenticated.
export const isAuthenticated: Readable<boolean> = derived(
  { subscribe }, // Pass the subscribe method of the writable store
  ($authState) => !!$authState.accessToken // User is considered authenticated if an access token exists
);

// Export the store with its methods
export const authStore: AuthStore = {
  subscribe,
  set, // Expose set if direct manipulation is ever needed, though methods are preferred
  update, // Expose update for more complex state changes if necessary
  login,
  logout,
  setUserProfile,
  setTokens,
};

// Example of how to use the store in a Svelte component:
// <script lang="ts">
//   import { authStore, isAuthenticated } from '$lib/store/authStore';
//   import type { UserProfile } from '$lib/store/authStore'; // For type checking

//   let currentUser: UserProfile | null = null;
//   let isUserAuthenticated: boolean = false;

//   authStore.subscribe(value => {
//     currentUser = value.user;
//   });

//   isAuthenticated.subscribe(value => {
//     isUserAuthenticated = value;
//   });

//   function handleLogout() {
//     authStore.logout();
//   }
// </script>

// {#if isUserAuthenticated && currentUser}
//   <p>Welcome, {currentUser.username}!</p>
//   <button on:click={handleLogout}>Logout</button>
// {:else}
//   <p>Please log in.</p>
// {/if}
