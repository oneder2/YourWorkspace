// src/lib/services/anchorService.ts

/**
 * @file anchorService.ts
 * @description Service layer for handling "Personal Anchor" related API interactions.
 * Includes Profile, Achievements, and Future Plans.
 * "Current Focus" is now managed via todoService as an attribute of To-Do items.
 */

import { api, type ApiError } from './api';

// --- Interfaces for Profile ---
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


// --- Profile Service Methods ---
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

export const anchorService = {
  // Profile methods
  getIdentityProfile,
  updateIdentityProfile,
  // Methods for Achievements and Future Plans will be added here later
};
