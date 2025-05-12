<script lang="ts">
    import { onMount } from 'svelte';
    import { achievementStore } from '$lib/store/achievementStore'; // Main store for achievements
    import type { Achievement } from '$lib/services/achievementService';
    import AchievementItem from './AchievementItem.svelte'; // Component to display a single achievement

    // Define callback props to replace event dispatching
    let {
      editAchievement,
      addNewAchievement,
      onSelectAchievement = (_achievement: any) => {}
    } = $props<{
      editAchievement?: (achievement: Achievement) => void;
      addNewAchievement?: () => void;
      onSelectAchievement?: (achievement: Achievement) => void;
    }>();

    // Subscribe to reactive stores from achievementStore
    // These will automatically update the component when their values change.
    const achievements = achievementStore.achievements; // Writable<Achievement[]>
    const isLoading = achievementStore.isLoading;     // Writable<boolean>
    const error = achievementStore.error;             // Writable<string | null>

    // Lifecycle hook: Called after the component has been mounted to the DOM.
    onMount(() => {
      // Attempt to load achievements if the list is currently empty,
      // not already loading, and there's no existing error.
      // This ensures data is fetched when the component first loads.
      // The store itself also has logic to load on auth change, this is an additional trigger.
      if ($achievements.length === 0 && !$isLoading && !$error) {
        achievementStore.loadAchievements();
      }
    });

    /**
     * Handles the edit request from an AchievementItem.
     * It calls the editAchievement callback prop with the achievement to be edited.
     * @param {Achievement} achievement - The achievement to be edited.
     */
    function handleEditRequest(achievement: Achievement) {
      editAchievement?.(achievement);
    }

    /**
     * Handles the click event for the "Add New Achievement" button.
     * It calls the addNewAchievement callback prop to handle (e.g., open a modal).
     */
    function handleAddNewRequest() {
      addNewAchievement?.();
    }
  </script>

  <div class="flex flex-col h-full py-2">
    <!-- Main content area -->
    <div class="flex-grow">
      {#if $isLoading && $achievements.length === 0}
        <div class="text-center py-6">
          <div role="status" class="flex justify-center items-center">
              <svg aria-hidden="true" class="w-10 h-10 text-purple-200 animate-spin dark:text-purple-700 fill-purple-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                  <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0492C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="lightgray"/>
              </svg>
              <span class="sr-only">Loading...</span>
          </div>
          <p class="mt-2 text-purple-600 dark:text-purple-400">Loading achievements...</p>
        </div>
      {:else if $error}
        <div class="p-4 mx-2 mb-4 text-sm text-red-700 bg-red-100 rounded-lg dark:bg-red-200 dark:text-red-800 text-center" role="alert">
          <span class="font-medium">Loading error:</span> {$error}
          <button
            onclick={() => achievementStore.loadAchievements()}
            class="ml-4 px-3 py-1.5 text-sm font-medium text-white bg-purple-600 rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            Retry
          </button>
        </div>
      {:else if $achievements.length === 0}
        <div class="text-center py-6">
          <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16l3.5-2 3.5 2 3.5-2 3.5 2zM12 11v2m0-4h.01" />
          </svg>
          <h3 class="mt-2 text-lg font-medium text-purple-900 dark:text-purple-100">No achievements yet</h3>
          <p class="mt-1 text-sm text-purple-600 dark:text-purple-400">Start adding your first achievement!</p>
        </div>
      {:else}
        <div class="space-y-4 px-2">
          {#each $achievements as achievement (achievement.id)}
            <AchievementItem
              {achievement}
              edit={handleEditRequest}
              onClick={() => onSelectAchievement(achievement)}
            />
          {/each}
        </div>
      {/if}
    </div>
  </div>
