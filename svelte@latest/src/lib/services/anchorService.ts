// src/lib/services/anchorService.ts

/**
 * @file anchorService.ts
 * @description Service layer for handling "Personal Anchor" related API interactions.
 * Includes Profile, Achievements, Current Focus, and Future Plans.
 */

import { api, type ApiError } from './api';

// --- Interfaces for Profile (already defined) ---
export interface UserProfileData {
  user_id: number;
  professional_title: string | null;
  one_liner_bio: string | null;
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
}

export interface UpdateUserProfilePayload {
  professional_title?: string | null;
  one_liner_bio?: string | null;
}

// --- Interfaces for Current Focus (based on API documentation Section 3.3) ---
export interface CurrentFocusItem {
  id: number;
  user_id: number;
  item_type: string | null; // e.g., "Project", "Learning Goal", "Skill Development"
  title: string;
  description: string | null;
  start_date: string | null; // YYYY-MM-DD
  status: string | null; // e.g., "Active", "On Hold", "Nearing Completion"
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
}

export interface CreateCurrentFocusPayload {
  title: string; // Required
  item_type?: string;
  description?: string;
  start_date?: string; // YYYY-MM-DD
  status?: string;
}

export interface UpdateCurrentFocusPayload {
  title?: string;
  item_type?: string;
  description?: string | null;
  start_date?: string | null; // YYYY-MM-DD
  status?: string | null;
}


// --- Profile Service Methods (already defined) ---
async function getIdentityProfile(): Promise<UserProfileData> {
  try {
    const profileData = await api.get<UserProfileData>('/anchor/profile');
    if (!profileData) {
      throw new Error('Profile data not found or API returned an unexpected empty response.');
    }
    return profileData;
  } catch (error) {
    console.error('AnchorService: Failed to fetch identity profile', error);
    throw error;
  }
}

async function updateIdentityProfile(payload: UpdateUserProfilePayload): Promise<UserProfileData> {
  try {
    const updatedProfile = await api.put<UserProfileData>('/anchor/profile', payload);
    return updatedProfile;
  } catch (error) {
    console.error('AnchorService: Failed to update identity profile', error);
    throw error;
  }
}

// --- Current Focus Service Methods ---

/**
 * Fetches all Current Focus items for the authenticated user.
 * API: GET /anchor/current_focus
 * @returns {Promise<CurrentFocusItem[]>} A list of current focus items.
 * @throws {ApiError} If the request fails.
 */
async function getAllCurrentFocusItems(): Promise<CurrentFocusItem[]> {
  try {
    const items = await api.get<CurrentFocusItem[]>('/anchor/current_focus');
    return items || [];
  } catch (error) {
    console.error('AnchorService: Failed to fetch all current focus items', error);
    throw error;
  }
}

/**
 * Creates a new Current Focus item.
 * API: POST /anchor/current_focus
 * @param payload - The data for the new current focus item.
 * @returns {Promise<CurrentFocusItem>} The newly created current focus item.
 * @throws {ApiError} If the request fails.
 */
async function createCurrentFocusItem(payload: CreateCurrentFocusPayload): Promise<CurrentFocusItem> {
  try {
    const newItem = await api.post<CurrentFocusItem>('/anchor/current_focus', payload);
    return newItem;
  } catch (error) {
    console.error('AnchorService: Failed to create current focus item', error);
    throw error;
  }
}

/**
 * Fetches a specific Current Focus item by its ID.
 * API: GET /anchor/current_focus/<int:focus_id>
 * @param focusId - The ID of the item to fetch.
 * @returns {Promise<CurrentFocusItem | null>} The item, or null if not found.
 * @throws {ApiError} If the request fails (other than 404).
 */
async function getCurrentFocusItemById(focusId: number): Promise<CurrentFocusItem | null> {
  try {
    const item = await api.get<CurrentFocusItem>(`/anchor/current_focus/${focusId}`);
    return item;
  } catch (error: any) {
    if (error.status === 404) {
      console.warn(`AnchorService: Current focus item with ID ${focusId} not found.`);
      return null;
    }
    console.error(`AnchorService: Failed to fetch current focus item with ID ${focusId}`, error);
    throw error;
  }
}

/**
 * Updates an existing Current Focus item.
 * API: PUT /anchor/current_focus/<int:focus_id>
 * @param focusId - The ID of the item to update.
 * @param payload - The data to update.
 * @returns {Promise<CurrentFocusItem>} The updated item.
 * @throws {ApiError} If the request fails.
 */
async function updateCurrentFocusItem(focusId: number, payload: UpdateCurrentFocusPayload): Promise<CurrentFocusItem> {
  try {
    const updatedItem = await api.put<CurrentFocusItem>(`/anchor/current_focus/${focusId}`, payload);
    return updatedItem;
  } catch (error) {
    console.error(`AnchorService: Failed to update current focus item with ID ${focusId}`, error);
    throw error;
  }
}

/**
 * Deletes a specific Current Focus item.
 * API: DELETE /anchor/current_focus/<int:focus_id>
 * @param focusId - The ID of the item to delete.
 * @returns {Promise<void>}
 * @throws {ApiError} If the request fails.
 */
async function deleteCurrentFocusItem(focusId: number): Promise<void> {
  try {
    await api.delete(`/anchor/current_focus/${focusId}`);
  } catch (error) {
    console.error(`AnchorService: Failed to delete current focus item with ID ${focusId}`, error);
    throw error;
  }
}


export const anchorService = {
  // Profile methods
  getIdentityProfile,
  updateIdentityProfile,

  // Current Focus methods
  getAllCurrentFocusItems,
  createCurrentFocusItem,
  getCurrentFocusItemById,
  updateCurrentFocusItem,
  deleteCurrentFocusItem,

  // Methods for Achievements and Future Plans will be added here later
};
