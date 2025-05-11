<script lang="ts">
    import type { Achievement } from '$lib/services/achievementService';
    import { achievementStore } from '$lib/store/achievementStore';

    // Props
    let { achievement, edit } = $props<{
      achievement: Achievement;
      edit?: (achievement: Achievement) => void;
    }>();

    let isDeleting = $state(false); // Local state for delete confirmation or loading

    const handleEdit = () => {
      edit?.(achievement);
    };

    const handleDelete = async () => {
      // Optional: Add a confirmation step here, e.g., using a modal or a simple confirm()
      // For now, directly attempts deletion.
      if (!confirm(`您确定要删除成就 "${achievement.title}" 吗？此操作无法撤销。`)) {
        return;
      }

      isDeleting = true;
      try {
        await achievementStore.deleteAchievement(achievement.id);
        // Parent component (AchievementList) will react to store changes and remove this item.
        // Optionally dispatch a 'deleted' event if needed for other UI updates.
        // No need to dispatch events anymore, store changes will trigger UI updates
      } catch (e: any) {
        // Handle error display, perhaps through a global notification system or a local message
        alert(`删除失败：${e.message || '未知错误'}`);
        console.error("Error deleting achievement:", e);
      } finally {
        isDeleting = false;
      }
    };

    // Helper to format date, can be moved to a utils file
    function formatDate(dateString: string | null | undefined): string {
      if (!dateString) return '日期未指定';
      try {
        const date = new Date(dateString);
        // Adjust for potential timezone issues if dates are just YYYY-MM-DD
        // and new Date() interprets them as UTC.
        const userTimezoneOffset = date.getTimezoneOffset() * 60000;
        return new Date(date.getTime() + userTimezoneOffset).toLocaleDateString(undefined, {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        });
      } catch (e) {
        return dateString; // Return original if parsing fails
      }
    }
</script>

<div class="bg-white dark:bg-gray-800 shadow-lg rounded-xl p-6 mb-4 transition-all hover:shadow-xl border border-purple-200 dark:border-purple-800">
    <div class="flex justify-between items-start">
        <div>
        <h4 class="text-xl font-semibold text-purple-600 dark:text-purple-400 mb-1">{achievement.title}</h4>
        {#if achievement.date_achieved}
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">
            Achieved on: {formatDate(achievement.date_achieved)}
            </p>
        {/if}
        </div>
        <div class="flex space-x-2 rtl:space-x-reverse">
        <button
            onclick={handleEdit}
            aria-label="Edit achievement {achievement.title}"
            class="p-2 text-sm font-medium text-purple-600 hover:text-purple-800 dark:text-purple-400 dark:hover:text-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 rounded-md"
        >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
            <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
            </svg>
        </button>
        <button
            onclick={handleDelete}
            disabled={isDeleting}
            aria-label="Delete achievement {achievement.title}"
            class="p-2 text-sm font-medium text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 rounded-md disabled:opacity-50"
        >
            {#if isDeleting}
            <svg aria-hidden="true" role="status" class="inline w-5 h-5 text-red-500 animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0492C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
            </svg>
            {:else}
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            {/if}
        </button>
        </div>
    </div>

    {#if achievement.description}
        <p class="text-gray-700 dark:text-gray-300 mt-2 text-sm">{achievement.description}</p>
    {/if}

    {#if achievement.quantifiable_results}
        <div class="mt-3">
        <h5 class="text-sm font-semibold text-gray-600 dark:text-gray-400">可量化成果:</h5>
        <p class="text-gray-700 dark:text-gray-300 text-sm">{achievement.quantifiable_results}</p>
        </div>
    {/if}

    {#if achievement.core_skills_json && achievement.core_skills_json.length > 0}
        <div class="mt-3">
        <h5 class="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Core Skills:</h5>
        <div class="flex flex-wrap gap-2">
            {#each achievement.core_skills_json as skill}
            <span class="px-2 py-1 text-xs font-medium text-purple-700 bg-purple-100 rounded-full dark:bg-purple-900 dark:text-purple-300">
                {skill}
            </span>
            {/each}
        </div>
        </div>
    {/if}

    <div class="mt-4 pt-3 border-t border-purple-200 dark:border-purple-800 text-xs text-gray-400 dark:text-gray-500">
        ID: {achievement.id} | Created: {formatDate(achievement.created_at)}
        {#if achievement.updated_at && achievement.updated_at !== achievement.created_at}
        | Updated: {formatDate(achievement.updated_at)}
        {/if}
    </div>
</div>
