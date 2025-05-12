<script lang="ts">
    // Import necessary Svelte components and types
    import AchievementList from '$lib/components/anchor/achievements/AchievementList.svelte';
    import AchievementForm from '$lib/components/anchor/achievements/AchievementForm.svelte';
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

      try {
        await achievementStore.deleteAchievement(selectedAchievement.id);
        selectedAchievement = null;
        isViewMode = false;
      } catch (e: any) {
        alert(`Failed to delete: ${e.message || 'Unknown error'}`);
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
                <h3 class={headings.h3}>Achievements</h3>
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
            <div class={combineClasses(scrollArea.container, "flex-grow")}>
              <!-- Scrollbar indicator on the left -->
              <div class={combineClasses(scrollArea.indicator, "left-0", pageStyle.scrollbar)}></div>

              <!-- Scrollable content -->
              <div class={combineClasses("pl-3", "h-full overflow-y-auto")}>
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
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
                          <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
                        </svg>
                      </button>
                      <button
                        onclick={deleteSelectedAchievement}
                        class="p-2 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
                        aria-label="Delete achievement"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  <!-- Achievement date -->
                  {#if selectedAchievement.date_achieved}
                    <div class="mb-6">
                      <div class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
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
                  <svg xmlns="http://www.w3.org/2000/svg" class={combineClasses("h-16 w-16 mb-4", pageStyle.icon)} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
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
        <div>
          <AchievementForm
            achievement={currentEditingAchievement}
            save={handleFormSave}
            cancel={handleFormCancel}
          />
        </div>
      </Modal>
    {/if}
  </div>
