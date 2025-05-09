// src/lib/store/anchorStore.ts

/**
 * @file anchorStore.ts
 * @description Manages state for the user's "Personal Anchor" data,
 * including Identity Profile, Achievements, Current Focus, and Future Plans.
 */

import { writable, type Writable } from 'svelte/store';
import {
  anchorService,
  type UserProfileData,
  type UpdateUserProfilePayload,
  type CurrentFocusItem, // Added
  type CreateCurrentFocusPayload, // Added
  type UpdateCurrentFocusPayload // Added
} from '$lib/services/anchorService';
import type { ApiError } from '$lib/services/api';

// --- State Interface for the Identity Profile part of the store ---
export interface IdentityProfileState {
  profile: UserProfileData | null;
  isLoading: boolean;
  error: string | null;
}

// --- State Interface for the Current Focus part of the store --- (NEW)
export interface CurrentFocusState {
  items: CurrentFocusItem[];
  isLoading: boolean;
  error: string | null;
}

// --- State Interface for the entire Anchor Store (will grow) ---
export interface AnchorStoreState {
  identityProfile: IdentityProfileState;
  currentFocus: CurrentFocusState; // Added
  // achievements: AchievementState; // To be added
  // futurePlans: FuturePlanState; // To be added
}

// --- Custom Store Interface ---
export interface CustomAnchorStore extends Writable<AnchorStoreState> {
  // Identity Profile methods
  loadIdentityProfile: () => Promise<void>;
  saveIdentityProfile: (payload: UpdateUserProfilePayload) => Promise<UserProfileData | null>;

  // Current Focus methods (NEW)
  loadCurrentFocusItems: () => Promise<void>;
  addCurrentFocusItem: (payload: CreateCurrentFocusPayload) => Promise<CurrentFocusItem | null>;
  updateCurrentFocusItem: (itemId: number, payload: UpdateCurrentFocusPayload) => Promise<CurrentFocusItem | null>;
  deleteCurrentFocusItem: (itemId: number) => Promise<void>;

  // Methods for other sections will be added here
}

// --- Initial State ---
const initialIdentityProfileState: IdentityProfileState = {
  profile: null,
  isLoading: false,
  error: null,
};

const initialCurrentFocusState: CurrentFocusState = { // Added
  items: [],
  isLoading: false,
  error: null,
};

const initialAnchorStoreState: AnchorStoreState = {
  identityProfile: initialIdentityProfileState,
  currentFocus: initialCurrentFocusState, // Added
  // Initialize other sections here when added
};

// --- Create the Writable Store ---
const { subscribe, set, update }: Writable<AnchorStoreState> = writable<AnchorStoreState>(initialAnchorStoreState);

// --- Store Methods for Identity Profile (already defined) ---
async function loadIdentityProfile(): Promise<void> {
  update(state => ({
    ...state,
    identityProfile: { ...state.identityProfile, isLoading: true, error: null }
  }));
  try {
    const profileData = await anchorService.getIdentityProfile();
    update(state => ({
      ...state,
      identityProfile: { profile: profileData, isLoading: false, error: null }
    }));
  } catch (err) {
    const error = err as ApiError;
    console.error('AnchorStore: Error fetching identity profile', error);
    update(state => ({
      ...state,
      identityProfile: {
        ...state.identityProfile,
        isLoading: false,
        error: error.message || 'Failed to fetch identity profile.'
      }
    }));
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
    const error = err as ApiError;
    console.error('AnchorStore: Error saving identity profile', error);
    update(state => ({
      ...state,
      identityProfile: {
        ...state.identityProfile,
        isLoading: false,
        error: error.message || 'Failed to save identity profile.'
      }
    }));
    return null;
  }
}

// --- Store Methods for Current Focus (NEW) ---

/**
 * Fetches all Current Focus items from the backend and updates the store.
 */
async function loadCurrentFocusItems(): Promise<void> {
  update(state => ({
    ...state,
    currentFocus: { ...state.currentFocus, isLoading: true, error: null }
  }));
  try {
    const items = await anchorService.getAllCurrentFocusItems();
    // Sort items, e.g., by creation date descending
    items.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    update(state => ({
      ...state,
      currentFocus: { items, isLoading: false, error: null }
    }));
  } catch (err) {
    const error = err as ApiError;
    console.error('AnchorStore: Error fetching current focus items', error);
    update(state => ({
      ...state,
      currentFocus: { items: [], isLoading: false, error: error.message || 'Failed to fetch current focus items.' }
    }));
  }
}

/**
 * Adds a new Current Focus item and updates the store.
 * @param payload - Data for the new item.
 * @returns {Promise<CurrentFocusItem | null>} The created item or null if failed.
 */
async function addCurrentFocusItem(payload: CreateCurrentFocusPayload): Promise<CurrentFocusItem | null> {
  update(state => ({
    ...state,
    currentFocus: { ...state.currentFocus, isLoading: true, error: null } // More granular loading
  }));
  try {
    const newItem = await anchorService.createCurrentFocusItem(payload);
    update(state => ({
      ...state,
      currentFocus: {
        ...state.currentFocus,
        items: [newItem, ...state.currentFocus.items], // Add to the beginning
        isLoading: false,
      }
    }));
    return newItem;
  } catch (err) {
    const error = err as ApiError;
    console.error('AnchorStore: Error adding current focus item', error);
    update(state => ({
      ...state,
      currentFocus: {
        ...state.currentFocus,
        isLoading: false,
        error: error.message || 'Failed to add current focus item.'
      }
    }));
    return null;
  }
}

/**
 * Updates an existing Current Focus item and updates the store.
 * @param itemId - The ID of the item to update.
 * @param payload - The data to update.
 * @returns {Promise<CurrentFocusItem | null>} The updated item or null if failed.
 */
async function updateCurrentFocusItem(itemId: number, payload: UpdateCurrentFocusPayload): Promise<CurrentFocusItem | null> {
  update(state => ({
    ...state,
    currentFocus: { ...state.currentFocus, isLoading: true, error: null }
  }));
  try {
    const updatedItem = await anchorService.updateCurrentFocusItem(itemId, payload);
    update(state => ({
      ...state,
      currentFocus: {
        ...state.currentFocus,
        items: state.currentFocus.items.map(item => (item.id === itemId ? updatedItem : item)),
        isLoading: false,
      }
    }));
    return updatedItem;
  } catch (err) {
    const error = err as ApiError;
    console.error('AnchorStore: Error updating current focus item', error);
    update(state => ({
      ...state,
      currentFocus: {
        ...state.currentFocus,
        isLoading: false,
        error: error.message || `Failed to update item ${itemId}.`
      }
    }));
    return null;
  }
}

/**
 * Deletes a Current Focus item and updates the store.
 * @param itemId - The ID of the item to delete.
 */
async function deleteCurrentFocusItem(itemId: number): Promise<void> {
  update(state => ({
    ...state,
    currentFocus: { ...state.currentFocus, isLoading: true, error: null }
  }));
  try {
    await anchorService.deleteCurrentFocusItem(itemId);
    update(state => ({
      ...state,
      currentFocus: {
        ...state.currentFocus,
        items: state.currentFocus.items.filter(item => item.id !== itemId),
        isLoading: false,
      }
    }));
  } catch (err) {
    const error = err as ApiError;
    console.error('AnchorStore: Error deleting current focus item', error);
    update(state => ({
      ...state,
      currentFocus: {
        ...state.currentFocus,
        isLoading: false,
        error: error.message || `Failed to delete item ${itemId}.`
      }
    }));
  }
}

// --- Export the Custom Store ---
export const anchorStore: CustomAnchorStore = {
  subscribe,
  set,
  update,
  // Identity Profile
  loadIdentityProfile,
  saveIdentityProfile,
  // Current Focus
  loadCurrentFocusItems,
  addCurrentFocusItem,
  updateCurrentFocusItem,
  deleteCurrentFocusItem,
};
