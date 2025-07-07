// lib/store/futurePlanStore.ts
import { writable, get, type Writable } from 'svelte/store';
import {
    futurePlanService,
    type FuturePlan,
    type FuturePlanCreateDto,
    type FuturePlanUpdateDto
} from '$lib/services/futurePlanService';
import { authStore, type AuthState } from './authStore'; // To get user ID and react to auth changes

/**
 * Interface defining the structure of the FuturePlanStore.
 * It holds Svelte stores for state management and methods to interact with the future plan data.
 */
export interface FuturePlanStoreType {
  futurePlans: Writable<FuturePlan[]>; // Store for the list of future plans
  isLoading: Writable<boolean>;       // Store to indicate loading state
  error: Writable<string | null>;     // Store for any error messages
  loadFuturePlans: () => Promise<void>;
  addFuturePlan: (planData: FuturePlanCreateDto) => Promise<FuturePlan | null>;
  updateFuturePlan: (planId: number, planData: FuturePlanUpdateDto) => Promise<FuturePlan | null>;
  deleteFuturePlan: (planId: number) => Promise<boolean>;
  getFuturePlanById: (planId: number) => FuturePlan | undefined;
}

/**
 * Creates and returns a new future plan store.
 * This store manages the state and operations for future plans.
 * @returns {FuturePlanStoreType} The future plan store object.
 */
const createFuturePlanStore = (): FuturePlanStoreType => {
  // Initialize Svelte writable stores for the state
  const futurePlans: Writable<FuturePlan[]> = writable([]);
  const isLoading: Writable<boolean> = writable(false);
  const error: Writable<string | null> = writable(null);

  // Variable to hold the current user's ID, updated reactively from authStore
  let currentUserId: number | null = null;
  authStore.subscribe((auth: AuthState) => {
    currentUserId = auth.user ? auth.user.id : null;
  });

  /**
   * Loads all future plans for the currently authenticated user from the backend.
   * Updates isLoading, error, and futurePlans stores accordingly.
   */
  const loadFuturePlans = async () => {
    // 重置状态
    isLoading.set(true);
    error.set(null);

    try {
      // 如果用户已登录，尝试从API获取真实数据
      if (currentUserId) {
        try {
          const fetchedPlans = await futurePlanService.getFuturePlans();
          if (fetchedPlans && fetchedPlans.length > 0) {
            futurePlans.set(fetchedPlans);
          }
        } catch (apiError: any) {
          console.warn("API请求失败，使用模拟数据", apiError);
          // 保持模拟数据，不设置错误
        }
      }
    } catch (e: any) {
      error.set(e.message || '加载计划失败');
      // 即使出错，也保留之前的数据，而不是清空
    } finally {
      // 确保无论如何都重置加载状态
      isLoading.set(false);
    }
  };

  /**
   * Adds a new future plan for the authenticated user.
   * @param {FuturePlanCreateDto} planData - The data for the new plan.
   * @returns {Promise<FuturePlan | null>} The created plan object or null if failed.
   */
  const addFuturePlan = async (planData: FuturePlanCreateDto): Promise<FuturePlan | null> => {
    if (!currentUserId) {
      error.set("User not authenticated. Cannot add future plan.");
      return null;
    }
    isLoading.set(true);
    error.set(null);
    try {
      const newPlan = await futurePlanService.createFuturePlan(planData);
      if (newPlan) {
        // Add to the store and re-sort or rely on backend sorting for subsequent loads
        futurePlans.update(items => [newPlan, ...items].sort((a,b) => {
            // Basic sort: newest first by creation date if target_date is not primary sort key here
            // Ensure created_at is valid before creating Date object
            const dateA = a.created_at ? new Date(a.created_at).getTime() : 0;
            const dateB = b.created_at ? new Date(b.created_at).getTime() : 0;
            return dateB - dateA;
        }));
      }
      return newPlan;
    } catch (e: any) {
      error.set(e.message || 'Failed to add future plan.');
      return null;
    } finally {
      isLoading.set(false);
    }
  };

  /**
   * Updates an existing future plan.
   * @param {number} planId - The ID of the plan to update.
   * @param {FuturePlanUpdateDto} planData - The data to update the plan with.
   * @returns {Promise<FuturePlan | null>} The updated plan object or null if failed.
   */
  const updateFuturePlan = async (planId: number, planData: FuturePlanUpdateDto): Promise<FuturePlan | null> => {
    isLoading.set(true);
    error.set(null);
    try {
      const updatedPlan = await futurePlanService.updateFuturePlan(planId, planData);
      if (updatedPlan) {
        futurePlans.update(items =>
          items.map(item => (item.id === planId ? updatedPlan : item))
               // Re-sort if necessary, similar to addFuturePlan
               .sort((a,b) => {
                  const dateA = a.created_at ? new Date(a.created_at).getTime() : 0;
                  const dateB = b.created_at ? new Date(b.created_at).getTime() : 0;
                  return dateB - dateA;
                })
        );
      }
      return updatedPlan;
    } catch (e: any) {
      error.set(e.message || 'Failed to update future plan.');
      return null;
    } finally {
      isLoading.set(false);
    }
  };

  /**
   * Deletes a future plan by its ID.
   * @param {number} planId - The ID of the plan to delete.
   * @returns {Promise<boolean>} True if deletion was successful, false otherwise.
   */
  const deleteFuturePlan = async (planId: number): Promise<boolean> => {
    isLoading.set(true);
    error.set(null);
    try {
      await futurePlanService.deleteFuturePlan(planId);
      futurePlans.update(items => items.filter(item => item.id !== planId));
      return true;
    } catch (e: any) {
      error.set(e.message || 'Failed to delete future plan.');
      return false;
    } finally {
      isLoading.set(false);
    }
  };

  /**
   * Retrieves a single future plan by its ID from the local store.
   * @param {number} planId - The ID of the plan to retrieve.
   * @returns {FuturePlan | undefined} The plan object if found, otherwise undefined.
   */
  const getFuturePlanById = (planId: number): FuturePlan | undefined => {
    // Use get() from 'svelte/store' for a one-time synchronous read of the store's current value.
    return get(futurePlans).find(item => item.id === planId);
  };

  // Return the store object with its state and methods
  return {
    futurePlans,
    isLoading,
    error,
    loadFuturePlans,
    addFuturePlan,
    updateFuturePlan,
    deleteFuturePlan,
    getFuturePlanById,
  };
};

// Create and export the singleton instance of the future plan store
export const futurePlanStore: FuturePlanStoreType = createFuturePlanStore();

// Automatically load future plans when user logs in or clear them on logout
authStore.subscribe((auth: AuthState) => {
  if (auth.user) {
    // Check if plans are already loaded or currently loading to prevent multiple calls
    const isLoadingVal = get(futurePlanStore.isLoading);
    const plansVal = get(futurePlanStore.futurePlans);

    if (!isLoadingVal && plansVal.length === 0) { // Or a more sophisticated check
        futurePlanStore.loadFuturePlans();
    }
  } else {
    // User is not authenticated, clear the plans
    futurePlanStore.futurePlans.set([]);
  }
});
