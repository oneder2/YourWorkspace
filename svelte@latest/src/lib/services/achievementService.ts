import { api } from './api'; // 引入通用的 API 请求处理器

const BASE_URL = '/anchor/achievements'; // API 基础路径

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
   * GET /api/v1/anchor/achievements
   * @returns Promise<Achievement[]>
   */
  async getAchievements(): Promise<Achievement[]> {
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
   * POST /api/v1/anchor/achievements
   * @param achievementData - The data for the new achievement.
   * @returns Promise<Achievement> - The newly created achievement.
   */
  async createAchievement(achievementData: AchievementCreateDto): Promise<Achievement> {
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
   * GET /api/v1/anchor/achievements/<achievement_id>
   * @param id - The ID of the achievement to retrieve.
   * @returns Promise<Achievement> - The requested achievement.
   */
  async getAchievementById(id: number): Promise<Achievement> {
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
   * PUT /api/v1/anchor/achievements/<achievement_id>
   * @param id - The ID of the achievement to update.
   * @param achievementData - The data to update the achievement with.
   * @returns Promise<Achievement> - The updated achievement.
   */
  async updateAchievement(id: number, achievementData: AchievementUpdateDto): Promise<Achievement> {
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
   * DELETE /api/v1/anchor/achievements/<achievement_id>
   * @param id - The ID of the achievement to delete.
   * @returns Promise<void>
   */
  async deleteAchievement(id: number): Promise<void> {
    try {
      await api.delete(`${BASE_URL}/${id}`);
    } catch (error) {
      console.error(`Error deleting achievement with ID ${id}:`, error);
      throw error;
    }
  },
};
