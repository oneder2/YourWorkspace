import { writable, type Writable, get } from 'svelte/store'; // Imported get for cleaner access in authStore.subscribe
import { achievementService, type Achievement, type AchievementCreateDto, type AchievementUpdateDto } from '$lib/services/achievementService';
import { authStore, type UserProfile, type AuthState } from './authStore';

/**
 * Defines the structure of the exported achievementStore object.
 * It contains individual Svelte stores for state and methods to interact with that state.
 */
export interface AchievementStoreType {
  achievements: Writable<Achievement[]>; // The store holding the list of achievements
  isLoading: Writable<boolean>;    // The store indicating if an operation is in progress
  error: Writable<string | null>; // The store holding any error messages
  loadAchievements: () => Promise<void>;
  addAchievement: (achievementData: AchievementCreateDto) => Promise<Achievement | null>;
  updateAchievement: (id: string | number, achievementData: AchievementUpdateDto) => Promise<Achievement | null>;
  deleteAchievement: (id: string | number) => Promise<boolean>;
  getAchievementById: (id: string | number) => Achievement | undefined;
  // Note: No top-level 'subscribe' method here.
  // Consumers will subscribe to individual stores like $achievementStore.achievements
}

const createAchievementStore = (): AchievementStoreType => {
  const achievements: Writable<Achievement[]> = writable([]);
  const isLoading: Writable<boolean> = writable(false);
  const error: Writable<string | null> = writable(null);

  let currentUserId: number | null = null;
  authStore.subscribe((auth: AuthState) => {
    currentUserId = auth.user ? auth.user.id : null;
  });

  const loadAchievements = async () => {
    if (!currentUserId) {
      error.set("用户未登录，无法加载成就。");
      achievements.set([]);
      return;
    }
    isLoading.set(true);
    error.set(null);
    try {
      const fetchedAchievements = await achievementService.getAchievements();
      achievements.set(fetchedAchievements || []);
    } catch (e: any) {
      error.set(e.message || '加载成就失败。');
      achievements.set([]);
    } finally {
      isLoading.set(false);
    }
  };

  const addAchievement = async (achievementData: AchievementCreateDto): Promise<Achievement | null> => {
    if (!currentUserId) {
      error.set("用户未登录，无法添加成就。");
      return null;
    }
    isLoading.set(true);
    error.set(null);
    try {
      const newAchievement = await achievementService.createAchievement(achievementData);
      if (newAchievement) {
        achievements.update(items =>
          [newAchievement, ...items].sort((a, b) => {
            if (!a.date_achieved || !b.date_achieved) return 0;
            return new Date(b.date_achieved).getTime() - new Date(a.date_achieved).getTime();
          })
        );
      }
      return newAchievement;
    } catch (e: any) {
      error.set(e.message || '添加成就失败。');
      return null;
    } finally {
      isLoading.set(false);
    }
  };

  const updateAchievement = async (idInput: string | number, achievementData: AchievementUpdateDto): Promise<Achievement | null> => {
    const id = typeof idInput === 'string' ? parseInt(idInput, 10) : idInput;
    if (isNaN(id)) {
        error.set("无效的成就ID进行更新。");
        return null;
    }

    isLoading.set(true);
    error.set(null);
    try {
      const updatedAchievement = await achievementService.updateAchievement(id, achievementData);
      if (updatedAchievement) {
        achievements.update(items =>
          items.map(item => (item.id === id ? updatedAchievement : item))
               .sort((a, b) => {
                  if (!a.date_achieved || !b.date_achieved) return 0;
                  return new Date(b.date_achieved).getTime() - new Date(a.date_achieved).getTime();
                })
        );
      }
      return updatedAchievement;
    } catch (e: any) {
      error.set(e.message || '更新成就失败。');
      return null;
    } finally {
      isLoading.set(false);
    }
  };

  const deleteAchievement = async (idInput: string | number): Promise<boolean> => {
    const id = typeof idInput === 'string' ? parseInt(idInput, 10) : idInput;
     if (isNaN(id)) {
        error.set("无效的成就ID进行删除。");
        return false;
    }

    isLoading.set(true);
    error.set(null);
    try {
      await achievementService.deleteAchievement(id);
      achievements.update(items => items.filter(item => item.id !== id));
      return true;
    } catch (e: any) {
      error.set(e.message || '删除成就失败。');
      return false;
    } finally {
      isLoading.set(false);
    }
  };

  const getAchievementById = (idInput: string | number): Achievement | undefined => {
    const id = typeof idInput === 'string' ? parseInt(idInput, 10) : idInput;
    if (isNaN(id)) return undefined;
    // Use get() for a one-time synchronous read of the store's current value.
    // This is useful for non-reactive contexts or simple lookups.
    return get(achievements).find(item => item.id === id);
  };

  return {
    achievements, // Expose the Writable store for achievements
    isLoading,    // Expose the Writable store for loading state
    error,        // Expose the Writable store for error state
    loadAchievements,
    addAchievement,
    updateAchievement,
    deleteAchievement,
    getAchievementById,
  };
};

export const achievementStore: AchievementStoreType = createAchievementStore();

// Auto-load achievements when user logs in or logs out
authStore.subscribe((auth: AuthState) => {
  if (auth.user) {
    // Use get() for cleaner synchronous access to current store values
    const isLoadingVal = get(achievementStore.isLoading);
    const achievementsVal = get(achievementStore.achievements);

    if (!isLoadingVal && achievementsVal.length === 0) {
        achievementStore.loadAchievements();
    }
  } else {
    achievementStore.achievements.set([]); // Clear achievements if user logs out
  }
});
