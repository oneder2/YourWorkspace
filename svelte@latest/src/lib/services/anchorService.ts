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
  skill: string | null;
  summary: string | null;
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
}

export interface UpdateUserProfilePayload {
  professional_title?: string | null;
  one_liner_bio?: string | null;
  skill?: string | null;
  summary?: string | null;
}


// --- Profile Service Methods ---
async function getIdentityProfile(): Promise<UserProfileData> {
  try {
    console.log('AnchorService: Fetching identity profile');
    // 使用正确的 API 路径，不需要包含 /api/v1 前缀，因为它已经在 BASE_URL 中定义
    const profileData = await api.get<UserProfileData>('/anchor/profile');

    if (!profileData) {
      console.error('AnchorService: Profile data not found or API returned an unexpected empty response');
      throw new Error('Profile data not found or API returned an unexpected empty response.');
    }

    console.log('AnchorService: Successfully fetched identity profile', profileData);
    return profileData;
  } catch (error) {
    console.error('AnchorService: Failed to fetch identity profile', error);

    // Add more detailed error information
    if (error instanceof Error) {
      console.error('Error details:', {
        message: error.message,
        stack: error.stack,
        name: error.name
      });

      // Enhance error message with more context
      const enhancedError = new Error(`Failed to fetch identity profile: ${error.message}`);
      enhancedError.stack = error.stack;
      throw enhancedError;
    }

    throw error;
  }
}

async function updateIdentityProfile(payload: UpdateUserProfilePayload): Promise<UserProfileData> {
  try {
    console.log('AnchorService: Updating identity profile with payload:', payload);
    // 使用正确的 API 路径，不需要包含 /api/v1 前缀，因为它已经在 BASE_URL 中定义
    const updatedProfile = await api.put<UserProfileData>('/anchor/profile', payload);

    if (!updatedProfile) {
      console.error('AnchorService: Updated profile data not found or API returned an unexpected empty response');
      throw new Error('Updated profile data not found or API returned an unexpected empty response.');
    }

    console.log('AnchorService: Successfully updated identity profile', updatedProfile);
    return updatedProfile;
  } catch (error) {
    console.error('AnchorService: Failed to update identity profile', error);

    // Add more detailed error information
    if (error instanceof Error) {
      console.error('Error details:', {
        message: error.message,
        stack: error.stack,
        name: error.name
      });

      // Enhance error message with more context
      const enhancedError = new Error(`Failed to update identity profile: ${error.message}`);
      enhancedError.stack = error.stack;
      throw enhancedError;
    }

    throw error;
  }
}

export const anchorService = {
  // Profile methods
  getIdentityProfile,
  updateIdentityProfile,
  // Methods for Achievements and Future Plans will be added here later
};
