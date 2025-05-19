// src/lib/store/anchorStore.ts

/**
 * @file anchorStore.ts
 * @description Manages state for the user's "Personal Anchor" data,
 * including Identity Profile, Achievements, and Future Plans.
 * "Current Focus" items are now managed as part of the todoStore.
 */

import { writable, type Writable } from 'svelte/store';
import {
  anchorService, // This service no longer handles current focus items directly
  type UserProfileData,
  type UpdateUserProfilePayload
  // Types related to CurrentFocusItem are removed from here
} from '$lib/services/anchorService';
import type { ApiError } from '$lib/services/api';

// --- State Interface for the Identity Profile part of the store ---
export interface IdentityProfileState {
  profile: UserProfileData | null;
  isLoading: boolean;
  error: string | null; // Stores error messages
}

// --- State Interface for the Current Focus part of the store (REMOVED) ---
// export interface CurrentFocusState { ... }

// --- State Interface for the entire Anchor Store (will grow) ---
export interface AnchorStoreState {
  identityProfile: IdentityProfileState;
  // currentFocus: CurrentFocusState; // REMOVED
  // achievements: AchievementState; // To be added
  // futurePlans: FuturePlanState; // To be added
}

// --- Custom Store Interface ---
// This defines the contract for our anchorStore
export interface CustomAnchorStore extends Writable<AnchorStoreState> {
  // Identity Profile methods
  loadIdentityProfile: () => Promise<void>;
  saveIdentityProfile: (payload: UpdateUserProfilePayload) => Promise<UserProfileData | null>;

  // Current Focus methods (REMOVED)
  // loadCurrentFocusItems: () => Promise<void>;
  // addCurrentFocusItem: (payload: CreateCurrentFocusPayload) => Promise<CurrentFocusItem | null>;
  // updateCurrentFocusItem: (itemId: number, payload: UpdateCurrentFocusPayload) => Promise<CurrentFocusItem | null>;
  // deleteCurrentFocusItem: (itemId: number) => Promise<void>;

  // Methods for other sections will be added here
}

// --- Initial State ---
const initialIdentityProfileState: IdentityProfileState = {
  profile: null,
  isLoading: false,
  error: null,
};

// const initialCurrentFocusState: CurrentFocusState = { ... }; // REMOVED

const initialAnchorStoreState: AnchorStoreState = {
  identityProfile: initialIdentityProfileState,
  // currentFocus: initialCurrentFocusState, // REMOVED
  // Initialize other sections here when added
};

// --- Create the Writable Store ---
const { subscribe, set, update }: Writable<AnchorStoreState> = writable<AnchorStoreState>(initialAnchorStoreState);

// --- Store Methods for Identity Profile (already defined) ---
async function loadIdentityProfile(): Promise<void> {
  console.log('AnchorStore: Starting loadIdentityProfile');
  update(state => ({
    ...state,
    identityProfile: { ...state.identityProfile, isLoading: true, error: null }
  }));
  try {
    console.log('AnchorStore: Calling anchorService.getIdentityProfile');
    const profileData = await anchorService.getIdentityProfile();
    console.log('AnchorStore: Successfully received profile data:', profileData);
    update(state => ({
      ...state,
      identityProfile: { profile: profileData, isLoading: false, error: null }
    }));
  } catch (err) {
    console.error('AnchorStore: Error fetching identity profile', err);

    // 安全地处理错误对象
    let errorMessage = 'Failed to fetch identity profile.';

    if (err instanceof Error) {
      console.error('AnchorStore: Error details:', {
        message: err.message,
        stack: err.stack,
        name: err.name
      });
      errorMessage = err.message;
    } else if (typeof err === 'object' && err !== null) {
      // 尝试从对象中提取消息
      const anyErr = err as any;
      if (anyErr.message) {
        errorMessage = anyErr.message;
      } else if (anyErr.data && anyErr.data.message) {
        errorMessage = anyErr.data.message;
      }
    }

    update(state => ({
      ...state,
      identityProfile: {
        ...state.identityProfile,
        isLoading: false,
        error: errorMessage
      }
    }));

    // 创建一个新的错误对象，避免类型问题
    const safeError = new Error(errorMessage);
    // Re-throw the error to allow the component to handle it
    throw safeError;
  }
}

async function saveIdentityProfile(payload: UpdateUserProfilePayload): Promise<UserProfileData | null> {
  update(state => ({
    ...state,
    identityProfile: { ...state.identityProfile, isLoading: true, error: null }
  }));
  try {
    const updatedProfile = await anchorService.updateIdentityProfile(payload);
    update(state => ({
      ...state,
      identityProfile: { profile: updatedProfile, isLoading: false, error: null }
    }));
    return updatedProfile;
  } catch (err) {
    console.error('AnchorStore: Error saving identity profile', err);

    // 安全地处理错误对象
    let errorMessage = 'Failed to save identity profile.';

    if (err instanceof Error) {
      console.error('AnchorStore: Error details:', {
        message: err.message,
        stack: err.stack,
        name: err.name
      });
      errorMessage = err.message;
    } else if (typeof err === 'object' && err !== null) {
      // 尝试从对象中提取消息
      const anyErr = err as any;
      if (anyErr.message) {
        errorMessage = anyErr.message;
      } else if (anyErr.data && anyErr.data.message) {
        errorMessage = anyErr.data.message;
      }
    }

    update(state => ({
      ...state,
      identityProfile: {
        ...state.identityProfile,
        isLoading: false,
        error: errorMessage
      }
    }));
    return null;
  }
}

// --- Store Methods for Current Focus (ALL REMOVED) ---
// async function loadCurrentFocusItems(): Promise<void> { ... }
// async function addCurrentFocusItem(payload: CreateCurrentFocusPayload): Promise<CurrentFocusItem | null> { ... }
// async function updateCurrentFocusItem(itemId: number, payload: UpdateCurrentFocusPayload): Promise<CurrentFocusItem | null> { ... }
// async function deleteCurrentFocusItem(itemId: number): Promise<void> { ... }


// --- Export the Custom Store ---
export const anchorStore: CustomAnchorStore = {
  subscribe,
  set,
  update,
  // Identity Profile
  loadIdentityProfile,
  saveIdentityProfile,
  // Current Focus methods are now removed.
  // Other methods will be added here
};
