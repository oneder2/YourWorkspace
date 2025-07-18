<script lang="ts">
    // Import necessary Svelte components and types
    import FuturePlanList from '$lib/components/anchor/future_plans/FuturePlanList.svelte';
    import FuturePlanForm from '$lib/components/anchor/future_plans/FuturePlanForm.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import type { FuturePlan } from '$lib/services/futurePlanService';
    import { futurePlanStore } from '$lib/store/futurePlanStore';
    import {
      pageContainer,
      colorSchemes,
      layouts,
      columnSpans,
      headings,
      scrollArea,
      cardBase,
      combineClasses
    } from '$lib/styles/pageStyles';

    // 获取当前页面的颜色方案
    const pageStyle = colorSchemes.plan;

    // State variables
    let isModalOpen = $state(false);
    let currentEditingFuturePlan = $state<FuturePlan | null>(null);
    let selectedPlan = $state<FuturePlan | null>(null);
    let isViewMode = $state(false);
    let isDeleting = $state(false);
    let operationFeedback = $state<{type: 'success' | 'error', message: string} | null>(null);

    /**
     * Opens the modal in 'create' mode for adding a new future plan.
     */
    function openCreateModal() {
      currentEditingFuturePlan = null;
      isModalOpen = true;
      isViewMode = false;
    }

    /**
     * Opens the modal in 'edit' mode for an existing future plan.
     * @param {FuturePlan} plan - The future plan to edit.
     */
    function openEditModal(plan: FuturePlan) {
      currentEditingFuturePlan = plan;
      isModalOpen = true;
      isViewMode = false;
    }

    /**
     * Selects a plan to view its details
     * @param {FuturePlan} plan - The future plan to view.
     */
    function selectPlan(plan: FuturePlan) {
      selectedPlan = plan;
      isViewMode = true;
      currentEditingFuturePlan = null;
    }

    /**
     * Closes the modal and resets the editing state.
     */
    function closeModal() {
      isModalOpen = false;
      currentEditingFuturePlan = null;
    }

    /**
     * Handles the save callback from FuturePlanForm.
     * Closes the modal after a successful save. The list will update reactively.
     * @param {FuturePlan} plan - The saved future plan.
     */
    function handleFormSave(plan: FuturePlan) {
      closeModal();
      // If we were editing the currently selected plan, update the selected plan
      if (selectedPlan && selectedPlan.id === plan.id) {
        selectedPlan = plan;
      }

      // If this was a new plan, select it for viewing
      if (!currentEditingFuturePlan) {
        selectedPlan = plan;
        isViewMode = true;
      }
    }

    /**
     * Handles the cancel callback from FuturePlanForm.
     * Closes the modal without saving.
     */
    function handleFormCancel() {
      closeModal();
    }

    /**
     * Deletes the currently selected future plan
     */
    async function deleteSelectedPlan() {
      if (!selectedPlan) return;

      if (!confirm(`Are you sure you want to delete "${selectedPlan.title}"? This action cannot be undone.`)) {
        return;
      }

      isDeleting = true;
      operationFeedback = null;

      try {
        const success = await futurePlanStore.deleteFuturePlan(selectedPlan.id);
        if (success) {
          operationFeedback = {
            type: 'success',
            message: `Successfully deleted "${selectedPlan.title}"`
          };
          selectedPlan = null;
          isViewMode = false;

          // Auto-hide success message after 3 seconds
          setTimeout(() => {
            operationFeedback = null;
          }, 3000);
        } else {
          operationFeedback = {
            type: 'error',
            message: 'Failed to delete plan. Please try again.'
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

    /**
     * Format a date string to a more readable format
     * @param {string | null | undefined} dateString - The date string to format
     * @returns {string} The formatted date string
     */
    function formatDate(dateString: string | null | undefined): string {
      if (!dateString) return 'Not set';
      try {
        const date = new Date(dateString + 'T00:00:00');
        return new Intl.DateTimeFormat('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        }).format(date);
      } catch (e) {
        return dateString;
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
        <!-- Left sidebar - Plans list -->
        <div class={combineClasses(columnSpans.oneFourth, "h-full flex flex-col")}>
          <div class={combineClasses(cardBase, pageStyle.border, "h-full flex flex-col")}>
            <!-- Header with title and add button -->
            <div class="p-4 border-b border-gray-200 dark:border-gray-700">
              <div class="flex justify-between items-center">
                <h2 class={combineClasses(headings.h3, pageStyle.text)}>
                  <svg xmlns="http://www.w3.org/2000/svg" class={combineClasses("h-5 w-5 mr-2 inline", pageStyle.icon)} viewBox="0 0 448 512" fill="currentColor">
                    <path d="M64 80c-8.8 0-16 7.2-16 16l0 320c0 8.8 7.2 16 16 16l224 0 0-80c0-17.7 14.3-32 32-32l80 0 0-224c0-8.8-7.2-16-16-16L64 80zM288 480L64 480c-35.3 0-64-28.7-64-64L0 96C0 60.7 28.7 32 64 32l320 0c35.3 0 64 28.7 64 64l0 224 0 5.5c0 17-6.7 33.3-18.7 45.3l-90.5 90.5c-12 12-28.3 18.7-45.3 18.7l-5.5 0z"/>
                  </svg>
                  Plans
                </h2>
                <button
                  onclick={openCreateModal}
                  class={combineClasses("p-1 text-sm rounded-md focus:outline-none focus:ring-2", pageStyle.text, pageStyle.hover)}
                  aria-label="Add new plan"
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
                <FuturePlanList
                  onAddNewFuturePlan={openCreateModal}
                  onEditFuturePlan={(plan: FuturePlan) => openEditModal(plan)}
                  onSelectPlan={(plan: FuturePlan) => selectPlan(plan)}
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Main content - Plan details -->
        <div class={combineClasses(columnSpans.threeFourths, "h-full flex flex-col")}>
          <div class={combineClasses(cardBase, pageStyle.border, "h-full flex flex-col")}>
            <div class="flex-grow overflow-hidden">
              <div class="h-full overflow-y-auto p-6">
              {#if selectedPlan && isViewMode}
                <!-- Detailed view of the selected plan -->
                <div>
                  <div class="flex justify-between items-center mb-6">
                    <h1 class={combineClasses(headings.h1, pageStyle.text)}>
                      {selectedPlan.title || 'Plan Details'}
                    </h1>
                    <div class="flex space-x-2">
                      <button
                        onclick={() => selectedPlan && openEditModal(selectedPlan)}
                        class={combineClasses("p-2 rounded-md focus:outline-none focus:ring-2", pageStyle.text, pageStyle.hover)}
                        aria-label="Edit plan"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                      </button>
                      <button
                        onclick={deleteSelectedPlan}
                        disabled={isDeleting}
                        class="p-2 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                        aria-label="Delete plan"
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

                  <!-- Status -->
                  <div class="mb-6">
                    <h3 class={combineClasses("text-lg font-semibold mb-2", pageStyle.text)}>Status</h3>
                    <div class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium
                      {selectedPlan.status === 'active' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' :
                       selectedPlan.status === 'achieved' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300' :
                       selectedPlan.status === 'deferred' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300' :
                       'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'}">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <path d="M12 6v6l4 2"></path>
                      </svg>
                      Status: {selectedPlan.status.charAt(0).toUpperCase() + selectedPlan.status.slice(1)}
                    </div>
                  </div>

                  <!-- Target Date -->
                  {#if selectedPlan.target_date}
                    <div class="mb-6">
                      <h3 class={combineClasses("text-lg font-semibold mb-2", pageStyle.text)}>Target Date</h3>
                      <div class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                          <line x1="16" y1="2" x2="16" y2="6"></line>
                          <line x1="8" y1="2" x2="8" y2="6"></line>
                          <line x1="3" y1="10" x2="21" y2="10"></line>
                        </svg>
                        Target Date: {formatDate(selectedPlan.target_date)}
                      </div>
                    </div>
                  {/if}

                  <!-- Goal Type -->
                  {#if selectedPlan.goal_type}
                    <div class="mb-6">
                      <h3 class={combineClasses("text-lg font-semibold mb-2", pageStyle.text)}>Goal Type</h3>
                      <div class="flex flex-wrap gap-2">
                        <span class="px-3 py-1 text-sm font-medium text-green-700 bg-green-100 rounded-full dark:bg-green-900 dark:text-green-300">
                          {selectedPlan.goal_type}
                        </span>
                      </div>
                    </div>
                  {/if}

                  <!-- Description -->
                  {#if selectedPlan.description}
                    <div class="mb-6">
                      <h3 class={combineClasses("text-lg font-semibold mb-2", pageStyle.text)}>Description</h3>
                      <div class="bg-white dark:bg-gray-700 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-600">
                        <p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{selectedPlan.description}</p>
                      </div>
                    </div>
                  {/if}

                  <!-- Metadata -->
                  <div class="mt-8 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <div class="flex justify-between text-sm text-gray-500 dark:text-gray-400">
                      <span>ID: {selectedPlan.id}</span>
                      <span>
                        Created: {formatDate(selectedPlan.created_at)}
                        {#if selectedPlan.updated_at && selectedPlan.updated_at !== selectedPlan.created_at}
                          <span class="ml-2">(Updated: {formatDate(selectedPlan.updated_at)})</span>
                        {/if}
                      </span>
                    </div>
                  </div>
                </div>
              {:else}
                <!-- Empty state when no plan is selected -->
                <div class="flex flex-col items-center justify-center h-full">
                  <svg xmlns="http://www.w3.org/2000/svg" class={combineClasses("h-16 w-16 mb-4", pageStyle.icon)} viewBox="0 0 448 512" fill="currentColor">
                    <path d="M64 80c-8.8 0-16 7.2-16 16l0 320c0 8.8 7.2 16 16 16l224 0 0-80c0-17.7 14.3-32 32-32l80 0 0-224c0-8.8-7.2-16-16-16L64 80zM288 480L64 480c-35.3 0-64-28.7-64-64L0 96C0 60.7 28.7 32 64 32l320 0c35.3 0 64 28.7 64 64l0 224 0 5.5c0 17-6.7 33.3-18.7 45.3l-90.5 90.5c-12 12-28.3 18.7-45.3 18.7l-5.5 0z"/>
                  </svg>
                  <h3 class={combineClasses("text-xl font-medium mb-2", pageStyle.text)}>Select a Plan</h3>
                  <p class="text-gray-600 dark:text-gray-400 text-center max-w-md">
                    Select a plan from the list to view details, or click the "+" button to create a new plan.
                  </p>
                </div>
              {/if}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    {#if isModalOpen}
      <Modal
        isOpen={isModalOpen}
        close={closeModal}
        title={currentEditingFuturePlan ? 'Edit Future Plan' : 'Add New Future Plan'}
        modalWidth="max-w-xl">
        <FuturePlanForm
          futurePlan={currentEditingFuturePlan}
          onSave={handleFormSave}
          onCancel={handleFormCancel}
        />
      </Modal>
    {/if}
  </div>
