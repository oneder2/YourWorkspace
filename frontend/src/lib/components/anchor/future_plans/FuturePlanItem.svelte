<script lang="ts">
    // Import necessary Svelte and project modules
    import type { FuturePlan } from '$lib/services/futurePlanService';
    import { futurePlanStore } from '$lib/store/futurePlanStore'; // To call deleteFuturePlan

    // Component props
    let {
      futurePlan,
      onEdit = () => {}, // Event handler prop for Svelte 5
      onClick = () => {} // Event handler for clicking on the item to view details
    } = $props<{
      futurePlan: FuturePlan;
      onEdit?: (plan: FuturePlan) => void;
      onClick?: (plan: FuturePlan) => void;
    }>();

    // Local state for delete operation loading status
    let isDeleting = $state(false);

    // No longer needed as we call onEdit directly from the button

    /**
     * Handles the deletion of the future plan.
     * It shows a confirmation dialog and then calls the store's delete method.
     */
    async function handleDelete() {
      // User confirmation before deleting
      if (!confirm(`Are you sure you want to delete the plan: "${futurePlan.title}"? This action cannot be undone.`)) {
        return;
      }

      isDeleting = true;
      try {
        await futurePlanStore.deleteFuturePlan(futurePlan.id);
        // The list will reactively update as the store changes.
        // Optionally, dispatch a 'deleted' event if the parent needs to know.
        // dispatch('deleted', futurePlan.id);
      } catch (e: any) {
        // Display an alert for error (a more sophisticated notification system could be used)
        alert(`Failed to delete plan: ${e.message || 'Unknown error'}`);
        console.error("Error deleting future plan:", e);
      } finally {
        isDeleting = false;
      }
    }

    /**
     * Utility function to format date strings (e.g., YYYY-MM-DD to a more readable format).
     * @param dateString - The date string to format.
     * @returns A formatted date string or a fallback string.
     */
    function formatDate(dateString: string | null | undefined): string {
      if (!dateString) return 'Not set';
      try {
        // Appending 'T00:00:00' helps ensure the date is parsed in the local timezone
        // rather than UTC, which can sometimes shift the day depending on the user's timezone.
        const date = new Date(dateString + 'T00:00:00');
        return new Intl.DateTimeFormat('en-US', { // Using 'en-US' for a common format, adjust as needed
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        }).format(date);
      } catch (e) {
        return dateString; // Return original string if parsing or formatting fails
      }
    }

    /**
     * Provides a user-friendly text representation for the plan status.
     * @param status - The status key.
     * @returns A capitalized, readable status string.
     */
    function formatStatus(status: 'active' | 'achieved' | 'deferred' | 'abandoned'): string {
      if (!status) return 'N/A';
      return status.charAt(0).toUpperCase() + status.slice(1);
    }

    // Status classes for badge styling
    const statusClasses = {
      active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
      achieved: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
      deferred: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
      abandoned: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
    };

  </script>

<div
    class="bg-white dark:bg-gray-800 shadow-md rounded-lg border border-green-200 dark:border-green-800 overflow-hidden cursor-pointer hover:shadow-lg transition-shadow mb-3"
    onclick={() => onClick(futurePlan)}
    onkeydown={(e) => e.key === 'Enter' && onClick(futurePlan)}
    role="button"
    tabindex="0"
    aria-label="View details for plan: {futurePlan.title}"
>
    <!-- Header with title and action buttons -->
    <div class="border-b border-green-100 dark:border-green-800 p-4">
        <div class="flex justify-between items-center">
            <h4 class="text-lg font-semibold text-green-700 dark:text-green-300">{futurePlan.title}</h4>
            <div class="flex space-x-1">
                <button
                    onclick={(e) => { e.stopPropagation(); onEdit(futurePlan); }}
                    aria-label="Edit plan: {futurePlan.title}"
                    class="p-1.5 text-sm font-medium text-green-600 hover:text-green-800 dark:text-green-400 dark:hover:text-green-300 focus:outline-none focus:ring-2 focus:ring-green-500 rounded-md"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
                        <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
                    </svg>
                </button>
                <button
                    onclick={(e) => { e.stopPropagation(); handleDelete(); }}
                    disabled={isDeleting}
                    aria-label="Delete plan: {futurePlan.title}"
                    class="p-1.5 text-sm font-medium text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-500 rounded-md disabled:opacity-50"
                >
                    {#if isDeleting}
                        <svg aria-hidden="true" role="status" class="inline w-4 h-4 text-red-500 animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                            <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0492C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
                        </svg>
                    {:else}
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                        </svg>
                    {/if}
                </button>
            </div>
        </div>

        {#if futurePlan.target_date}
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Target date: {formatDate(futurePlan.target_date)}
            </p>
        {/if}
    </div>

    <!-- Content section -->
    <div class="p-4">
        <!-- Status -->
        <div class="mb-3">
            <h5 class="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Status:</h5>
            <span class="px-2 py-0.5 text-xs font-medium rounded-full {statusClasses[futurePlan.status as keyof typeof statusClasses] || 'bg-gray-100 text-gray-800 dark:bg-gray-800/80 dark:text-gray-300'}">
                {formatStatus(futurePlan.status)}
            </span>
        </div>

        <!-- Goal Type -->
        {#if futurePlan.goal_type}
            <div class="mb-3">
                <h5 class="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Goal Type:</h5>
                <span class="px-2 py-0.5 text-xs font-medium text-green-700 bg-green-100 rounded-full dark:bg-green-900 dark:text-green-300">
                    {futurePlan.goal_type}
                </span>
            </div>
        {/if}
    </div>

    <!-- Footer with metadata -->
    <div class="px-4 py-2 bg-green-50 dark:bg-green-900/20 text-xs text-gray-500 dark:text-gray-400 border-t border-green-100 dark:border-green-800">
        <div class="flex justify-between">
            <span>ID: {futurePlan.id}</span>
            <span>
                {formatDate(futurePlan.created_at)}
                {#if futurePlan.updated_at && futurePlan.updated_at !== futurePlan.created_at}
                    (Updated: {formatDate(futurePlan.updated_at)})
                {/if}
            </span>
        </div>
    </div>
</div>
