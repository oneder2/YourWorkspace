import { api } from './api'; // Import the generic API handler
import { mockAchievementApi } from './mockApi'; // Import the mock API

const BASE_URL = '/achievements'; // Base URL for API endpoints without trailing slash to match backend routes

// Use real API for production
const USE_MOCK_API = false;

/**
 * Achievement object structure from the backend.
 */
export interface Achievement {
  id: number;
  user_id: number;
  title: string;
  description?: string | null;
  quantifiable_results?: string | null;
  core_skills_json?: string[];
  date_achieved?: string | null; // YYYY-MM-DD format
  created_at?: string; // ISO 8601
  updated_at?: string; // ISO 8601
}

/**
 * Data Transfer Object for creating an achievement.
 */
export interface AchievementCreateDto {
  title: string;
  description?: string | null;
  quantifiable_results?: string | null;
  core_skills_json?: string[];
  date_achieved?: string | null; // YYYY-MM-DD format
}

/**
 * Data Transfer Object for updating an achievement.
 * All fields are optional.
 */
export interface AchievementUpdateDto {
  title?: string;
  description?: string | null;
  quantifiable_results?: string | null;
  core_skills_json?: string[];
  date_achieved?: string | null; // YYYY-MM-DD format
}

/**
 * Service for interacting with the achievement API endpoints.
 */
export const achievementService = {
  /**
   * Retrieves all achievements for the authenticated user.
   * GET /api/achievements
   * @returns Promise<Achievement[]>
   */
  async getAchievements(): Promise<Achievement[]> {
    if (USE_MOCK_API) {
      console.log('Using mock API for getAchievements');
      return mockAchievementApi.getAll();
    }

    try {
      // Assuming api.get directly returns the data array
      const responseData = await api.get<Achievement[]>(BASE_URL);
      return responseData;
    } catch (error) {
      console.error('Error fetching achievements:', error);
      throw error;
    }
  },

  /**
   * Creates a new achievement.
   * POST /api/achievements
   * @param achievementData - The data for the new achievement.
   * @returns Promise<Achievement> - The newly created achievement.
   */
  async createAchievement(achievementData: AchievementCreateDto): Promise<Achievement> {
    if (USE_MOCK_API) {
      console.log('Using mock API for createAchievement', achievementData);
      return mockAchievementApi.create(achievementData);
    }

    try {
      // Assuming api.post directly returns the created object
      const responseData = await api.post<Achievement>(BASE_URL, achievementData);
      return responseData;
    } catch (error) {
      console.error('Error creating achievement:', error);
      throw error;
    }
  },

  /**
   * Retrieves a specific achievement by its ID.
   * GET /api/achievements/<achievement_id>
   * @param id - The ID of the achievement to retrieve.
   * @returns Promise<Achievement> - The requested achievement.
   */
  async getAchievementById(id: number): Promise<Achievement> {
    if (USE_MOCK_API) {
      console.log(`Using mock API for getAchievementById(${id})`);
      return mockAchievementApi.getById(id);
    }

    try {
      // Assuming api.get directly returns the object
      const responseData = await api.get<Achievement>(`${BASE_URL}/${id}`);
      return responseData;
    } catch (error) {
      console.error(`Error fetching achievement with ID ${id}:`, error);
      throw error;
    }
  },

  /**
   * Updates an existing achievement.
   * PUT /api/achievements/<achievement_id>
   * @param id - The ID of the achievement to update.
   * @param achievementData - The data to update the achievement with.
   * @returns Promise<Achievement> - The updated achievement.
   */
  async updateAchievement(id: number, achievementData: AchievementUpdateDto): Promise<Achievement> {
    if (USE_MOCK_API) {
      console.log(`Using mock API for updateAchievement(${id})`, achievementData);
      return mockAchievementApi.update(id, achievementData);
    }

    try {
      // Assuming api.put directly returns the updated object
      const responseData = await api.put<Achievement>(`${BASE_URL}/${id}`, achievementData);
      return responseData;
    } catch (error) {
      console.error(`Error updating achievement with ID ${id}:`, error);
      throw error;
    }
  },

  /**
   * Deletes a specific achievement.
   * DELETE /api/achievements/<achievement_id>
   * @param id - The ID of the achievement to delete.
   * @returns Promise<void>
   */
  async deleteAchievement(id: number): Promise<void> {
    if (USE_MOCK_API) {
      console.log(`Using mock API for deleteAchievement(${id})`);
      mockAchievementApi.delete();
      return;
    }

    try {
      await api.delete(`${BASE_URL}/${id}`);
    } catch (error) {
      console.error(`Error deleting achievement with ID ${id}:`, error);
      throw error;
    }
  },
};
