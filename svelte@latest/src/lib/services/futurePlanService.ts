// Import the generic API handler and mock API
import { api } from './api';
import { mockFuturePlanApi } from './mockApi';

// Base URL for future plan endpoints without trailing slash to match backend routes
const BASE_URL = '/plans';

// Use real API for production
const USE_MOCK_API = false;

// Define the structure of a Future Plan item based on the API documentation
export interface FuturePlan {
  id: number;
  user_id: number;
  goal_type?: string | null;
  title: string;
  description: string;
  target_date?: string | null; // Format: YYYY-MM-DD
  status: 'active' | 'achieved' | 'deferred' | 'abandoned';
  created_at?: string; // ISO 8601 format
  updated_at?: string; // ISO 8601 format
}

// Data Transfer Object for creating a new future plan
export interface FuturePlanCreateDto {
  title: string; // Required
  description: string; // Required
  goal_type?: string | null;
  target_date?: string | null; // Format: YYYY-MM-DD
  status?: 'active' | 'achieved' | 'deferred' | 'abandoned'; // Defaults to 'active' on backend
}

// Data Transfer Object for updating an existing future plan
// All fields are optional for updates.
export interface FuturePlanUpdateDto {
  title?: string;
  description?: string;
  goal_type?: string | null;
  target_date?: string | null; // Format: YYYY-MM-DD
  status?: 'active' | 'achieved' | 'deferred' | 'abandoned';
}

/**
 * Service for interacting with the future plan API endpoints.
 * All methods require authentication (handled by the generic 'api' handler).
 */
export const futurePlanService = {
  /**
   * Retrieves all future plans for the authenticated user.
   * GET /api/plans
   * Ordered by target_date asc (nulls last), then created_at desc.
   * @returns Promise<FuturePlan[]> - A list of future plans.
   */
  async getFuturePlans(): Promise<FuturePlan[]> {
    if (USE_MOCK_API) {
      console.log('Using mock API for getFuturePlans');
      return mockFuturePlanApi.getAll();
    }

    try {
      const responseData = await api.get<FuturePlan[]>(BASE_URL);
      return responseData;
    } catch (error) {
      console.error('Error fetching future plans:', error);
      // Propagate the error for handling by the caller (e.g., the store)
      throw error;
    }
  },

  /**
   * Creates a new future plan.
   * POST /api/plans
   * @param planData - The data for the new future plan.
   * @returns Promise<FuturePlan> - The newly created future plan.
   */
  async createFuturePlan(planData: FuturePlanCreateDto): Promise<FuturePlan> {
    if (USE_MOCK_API) {
      console.log('Using mock API for createFuturePlan', planData);
      return mockFuturePlanApi.create(planData);
    }

    try {
      const responseData = await api.post<FuturePlan>(BASE_URL, planData);
      return responseData;
    } catch (error) {
      console.error('Error creating future plan:', error);
      throw error;
    }
  },

  /**
   * Retrieves a specific future plan by its ID.
   * GET /api/plans/<plan_id>
   * @param planId - The ID of the future plan to retrieve.
   * @returns Promise<FuturePlan> - The requested future plan.
   */
  async getFuturePlanById(planId: number): Promise<FuturePlan> {
    if (USE_MOCK_API) {
      console.log(`Using mock API for getFuturePlanById(${planId})`);
      return mockFuturePlanApi.getById(planId);
    }

    try {
      const responseData = await api.get<FuturePlan>(`${BASE_URL}/${planId}`);
      return responseData;
    } catch (error) {
      console.error(`Error fetching future plan with ID ${planId}:`, error);
      throw error;
    }
  },

  /**
   * Updates an existing future plan.
   * PUT /api/plans/<plan_id>
   * @param planId - The ID of the future plan to update.
   * @param planData - The data to update the future plan with.
   * @returns Promise<FuturePlan> - The updated future plan.
   */
  async updateFuturePlan(planId: number, planData: FuturePlanUpdateDto): Promise<FuturePlan> {
    if (USE_MOCK_API) {
      console.log(`Using mock API for updateFuturePlan(${planId})`, planData);
      return mockFuturePlanApi.update(planId, planData);
    }

    try {
      const responseData = await api.put<FuturePlan>(`${BASE_URL}/${planId}`, planData);
      return responseData;
    } catch (error) {
      console.error(`Error updating future plan with ID ${planId}:`, error);
      throw error;
    }
  },

  /**
   * Deletes a specific future plan.
   * DELETE /api/plans/<plan_id>
   * @param planId - The ID of the future plan to delete.
   * @returns Promise<void> - Resolves when deletion is successful.
   */
  async deleteFuturePlan(planId: number): Promise<void> {
    if (USE_MOCK_API) {
      console.log(`Using mock API for deleteFuturePlan(${planId})`);
      mockFuturePlanApi.delete();
      return;
    }

    try {
      // DELETE requests typically return 204 No Content, so no response data is expected.
      await api.delete(`${BASE_URL}/${planId}`);
    } catch (error) {
      console.error(`Error deleting future plan with ID ${planId}:`, error);
      throw error;
    }
  },
};
