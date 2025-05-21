<script lang="ts">
    // Import necessary Svelte components and types
    import AchievementList from '$lib/components/working_page/done/AchievementList.svelte';
    import AchievementForm from '$lib/components/working_page/done/AchievementForm.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import type { Achievement } from '$lib/services/achievementService';
    import { achievementStore } from '$lib/store/achievementStore';
    import {
      pageContainer,
      colorSchemes,
      layouts,
      columnSpans,
      headings,
      cardBase,
      scrollArea,
      combineClasses
    } from '$lib/styles/pageStyles';

    // 获取当前页面的颜色方案
    const pageStyle = colorSchemes.done;

    // State variables
    let isModalOpen = $state(false);
    let currentEditingAchievement = $state<Achievement | null>(null);
    let selectedAchievement = $state<Achievement | null>(null);
    let isViewMode = $state(false);
    let isDeleting = $state(false);
    let operationFeedback = $state<{type: 'success' | 'error', message: string} | null>(null);

    /**
     * Opens the modal in 'create' mode for adding a new achievement.
     */
    function openCreateModal() {
      currentEditingAchievement = null;
      isModalOpen = true;
      isViewMode = false;
    }

    /**
     * Opens the modal in 'edit' mode for an existing achievement.
     * @param {Achievement} achievement - The achievement to edit.
     */
    function openEditModal(achievement: Achievement) {
      currentEditingAchievement = achievement;
      isModalOpen = true;
      isViewMode = false;
    }

    /**
     * Selects an achievement to view its details
     * @param {Achievement} achievement - The achievement to view.
     */
    function selectAchievement(achievement: Achievement) {
      selectedAchievement = achievement;
      isViewMode = true;
      currentEditingAchievement = null;
      isModalOpen = false;
    }

    /**
     * Closes the modal and resets the editing state.
     */
    function closeModal() {
      isModalOpen = false;
      currentEditingAchievement = null;
    }

    /**
     * Handles the save action from AchievementForm.
     * @param {Achievement} achievement - The saved achievement.
     */
    function handleFormSave(achievement: Achievement) {
      closeModal();
      // If we were viewing the achievement that was just edited, update the selected achievement
      if (selectedAchievement && selectedAchievement.id === achievement.id) {
        selectedAchievement = achievement;
      }

      // If this was a new achievement, select it for viewing
      if (!currentEditingAchievement) {
        selectedAchievement = achievement;
        isViewMode = true;
      }
    }

    /**
     * Handles the 'cancel' event dispatched by AchievementForm.
     */
    function handleFormCancel() {
      closeModal();
    }

    /**
     * Deletes the currently selected achievement
     */
    async function deleteSelectedAchievement() {
      if (!selectedAchievement) return;

      if (!confirm(`Are you sure you want to delete "${selectedAchievement.title}"? This action cannot be undone.`)) {
        return;
      }

      isDeleting = true;
      operationFeedback = null;

      try {
        const success = await achievementStore.deleteAchievement(selectedAchievement.id);
        if (success) {
          operationFeedback = {
            type: 'success',
            message: `Successfully deleted "${selectedAchievement.title}"`
          };
          selectedAchievement = null;
          isViewMode = false;

          // Auto-hide success message after 3 seconds
          setTimeout(() => {
            operationFeedback = null;
          }, 3000);
        } else {
          operationFeedback = {
            type: 'error',
            message: 'Failed to delete achievement. Please try again.'
          };
        }
      } catch (e: any) {
        operationFeedback = {
          type: 'error',
          message: `Failed to delete: ${e.message || 'Unknown error'}`
        };
      } finally {
        isDeleting = false;
      }
    }

    // Helper to format date
    function formatDate(dateString: string | null | undefined): string {
      if (!dateString) return 'Date not specified';
      try {
        const date = new Date(dateString);
        // Adjust for potential timezone issues if dates are just YYYY-MM-DD
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

  <div class={combineClasses(pageContainer, "h-[calc(100vh-180px)] flex flex-col")}>
    <!-- Operation feedback message -->
    {#if operationFeedback}
      <div class="mb-4 p-4 rounded-md {operationFeedback.type === 'success' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'}" role="alert">
        <div class="flex">
          <div class="flex-shrink-0">
            {#if operationFeedback.type === 'success'}
              <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            {:else}
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            {/if}
          </div>
          <div class="ml-3">
            <p class="text-sm font-medium">{operationFeedback.message}</p>
          </div>
          <div class="ml-auto pl-3">
            <div class="-mx-1.5 -my-1.5">
              <button
                onclick={() => operationFeedback = null}
                class="inline-flex rounded-md p-1.5 {operationFeedback.type === 'success' ? 'text-green-500 hover:bg-green-100 dark:text-green-300 dark:hover:bg-green-900/50' : 'text-red-500 hover:bg-red-100 dark:text-red-300 dark:hover:bg-red-900/50'} focus:outline-none focus:ring-2 focus:ring-offset-2 {operationFeedback.type === 'success' ? 'focus:ring-green-500' : 'focus:ring-red-500'}"
              >
                <span class="sr-only">Dismiss</span>
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    {/if}

    <!-- Main content container with fixed height -->
    <div class="flex-grow overflow-hidden">
      <!-- Two-column layout with fixed height -->
      <div class={combineClasses(layouts.twoColumnOneThree, "h-full")}>
        <!-- Left sidebar - Achievements list -->
        <div class={combineClasses(columnSpans.oneFourth, "h-full flex flex-col")}>
          <div class={combineClasses(cardBase, pageStyle.border, "h-full flex flex-col")}>
            <!-- Header with title and add button -->
            <div class="p-4 border-b border-gray-200 dark:border-gray-700">
              <div class="flex justify-between items-center">
                <h2 class={combineClasses(headings.h3, pageStyle.text)}>
                  <svg xmlns="http://www.w3.org/2000/svg" class={combineClasses("h-5 w-5 mr-2 inline", pageStyle.icon)} viewBox="0 0 512 512" fill="currentColor">
                    <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z"/>
                  </svg>
                  Achievements
                </h2>
                <button
                  onclick={openCreateModal}
                  class={combineClasses("p-1 text-sm rounded-md focus:outline-none focus:ring-2", pageStyle.text, pageStyle.hover)}
                  aria-label="Add new achievement"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Scrollable container with scrollbar indicator -->
            <div class={combineClasses(scrollArea.container, "flex-grow relative")}>
              <!-- Scrollbar indicator on the left -->
              <div class={combineClasses(scrollArea.indicator, "left-0", pageStyle.scrollbar)}></div>

              <!-- Scrollable content with fixed height and internal scrolling -->
              <div class={combineClasses("pl-3", "absolute inset-0 overflow-y-auto pr-2")}>
                <AchievementList
                  addNewAchievement={openCreateModal}
                  editAchievement={openEditModal}
                  onSelectAchievement={selectAchievement}
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Main content - Achievement details -->
        <div class={combineClasses(columnSpans.threeFourths, "h-full flex flex-col")}>
          <div class={combineClasses(cardBase, pageStyle.border, "h-full flex flex-col")}>
            <div class="p-6 flex-grow overflow-auto">
              {#if selectedAchievement && isViewMode}
                <!-- Detailed view of the selected achievement -->
                <div>
                  <div class="flex justify-between items-center mb-6">
                    <h2 class={combineClasses(headings.h2, pageStyle.text)}>
                      {selectedAchievement.title}
                    </h2>
                    <div class="flex space-x-2">
                      <button
                        onclick={() => selectedAchievement && openEditModal(selectedAchievement)}
                        class={combineClasses("p-2 rounded-md focus:outline-none focus:ring-2", pageStyle.text, pageStyle.hover)}
                        aria-label="Edit achievement"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                      </button>
                      <button
                        onclick={deleteSelectedAchievement}
                        disabled={isDeleting}
                        class="p-2 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                        aria-label="Delete achievement"
                      >
                        {#if isDeleting}
                          <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                        {:else}
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M3 6h18"></path>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path>
                            <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                            <line x1="10" y1="11" x2="10" y2="17"></line>
                            <line x1="14" y1="11" x2="14" y2="17"></line>
                          </svg>
                        {/if}
                      </button>
                    </div>
                  </div>

                  <!-- Achievement date -->
                  {#if selectedAchievement.date_achieved}
                    <div class="mb-6">
                      <div class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                          <line x1="16" y1="2" x2="16" y2="6"></line>
                          <line x1="8" y1="2" x2="8" y2="6"></line>
                          <line x1="3" y1="10" x2="21" y2="10"></line>
                        </svg>
                        Achieved on: {formatDate(selectedAchievement.date_achieved)}
                      </div>
                    </div>
                  {/if}

                  <!-- Core Skills -->
                  {#if selectedAchievement.core_skills_json && selectedAchievement.core_skills_json.length > 0}
                    <div class="mb-6">
                      <h3 class={combineClasses("text-lg font-semibold mb-2", pageStyle.text)}>Core Skills</h3>
                      <div class="flex flex-wrap gap-2">
                        {#each selectedAchievement.core_skills_json as skill}
                          <span class="px-3 py-1 text-sm font-medium text-purple-700 bg-purple-100 rounded-full dark:bg-purple-900 dark:text-purple-300">
                            {skill}
                          </span>
                        {/each}
                      </div>
                    </div>
                  {/if}

                  <!-- Description -->
                  {#if selectedAchievement.description}
                    <div class="mb-6">
                      <h3 class={combineClasses("text-lg font-semibold mb-2", pageStyle.text)}>Description</h3>
                      <div class="bg-white dark:bg-gray-700 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-600">
                        <p class="text-gray-700 dark:text-gray-300">{selectedAchievement.description}</p>
                      </div>
                    </div>
                  {/if}

                  <!-- Quantifiable Results -->
                  {#if selectedAchievement.quantifiable_results}
                    <div class="mb-6">
                      <h3 class={combineClasses("text-lg font-semibold mb-2", pageStyle.text)}>Quantifiable Results</h3>
                      <div class="bg-white dark:bg-gray-700 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-600">
                        <p class="text-gray-700 dark:text-gray-300">{selectedAchievement.quantifiable_results}</p>
                      </div>
                    </div>
                  {/if}

                  <!-- Metadata -->
                  <div class="mt-8 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <div class="flex justify-between text-sm text-gray-500 dark:text-gray-400">
                      <span>ID: {selectedAchievement.id}</span>
                      <span>
                        Created: {formatDate(selectedAchievement.created_at)}
                        {#if selectedAchievement.updated_at && selectedAchievement.updated_at !== selectedAchievement.created_at}
                          <span class="ml-2">(Updated: {formatDate(selectedAchievement.updated_at)})</span>
                        {/if}
                      </span>
                    </div>
                  </div>
                </div>
              {:else}
                <!-- Empty state when no achievement is selected -->
                <div class="flex flex-col items-center justify-center h-full">
                  <svg xmlns="http://www.w3.org/2000/svg" class={combineClasses("h-16 w-16 mb-4", pageStyle.icon)} viewBox="0 0 512 512" fill="currentColor">
                    <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z"/>
                  </svg>
                  <h3 class={combineClasses("text-xl font-medium mb-2", pageStyle.text)}>Select an Achievement</h3>
                  <p class="text-gray-600 dark:text-gray-400 text-center max-w-md">
                    Select an achievement from the list to view details, or click the "+" button to add a new achievement.
                  </p>
                </div>
              {/if}
            </div>
          </div>
        </div>
      </div>
    </div>

    {#if isModalOpen}
      <Modal
        isOpen={isModalOpen}
        close={closeModal}
        title={currentEditingAchievement ? 'Edit Achievement' : 'Add New Achievement'}
        modalWidth="max-w-xl"
      >
        <AchievementForm
          achievement={currentEditingAchievement}
          save={handleFormSave}
          cancel={handleFormCancel}
        />
      </Modal>
    {/if}
  </div>
