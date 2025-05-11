// src/lib/services/profileService.ts

/**
 * @file profileService.ts
 * @description Service for managing user profile operations
 */

import { apiClient } from './apiClient';
import type { UserProfile } from '$lib/store/authStore';

/**
 * Interface for profile update data
 */
export interface ProfileUpdateDto {
  professional_title?: string | null;
  one_liner_bio?: string | null;
  skill?: string | null;
  summary?: string | null;
}

/**
 * Service for managing user profile operations
 */
class ProfileService {
  /**
   * Get the current user's profile
   * @returns Promise resolving to the user profile
   */
  async getProfile(): Promise<UserProfile> {
    try {
      const response = await apiClient.get('/anchor/profile');
      return response.data;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      throw error;
    }
  }

  /**
   * Update the current user's profile
   * @param profileData - The profile data to update
   * @returns Promise resolving to the updated user profile
   */
  async updateProfile(profileData: ProfileUpdateDto): Promise<UserProfile> {
    try {
      const response = await apiClient.put('/anchor/profile', profileData);
      return response.data;
    } catch (error) {
      console.error('Error updating user profile:', error);
      throw error;
    }
  }
}

// Export a singleton instance
export const profileService = new ProfileService();
