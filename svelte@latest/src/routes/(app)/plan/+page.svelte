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
     * This function is kept for potential future use with modal editing.
     * @param {FuturePlan} plan - The future plan to edit.
     */
    // function openEditModal(plan: FuturePlan) {
    //   currentEditingFuturePlan = plan;
    //   isModalOpen = true;
    //   isViewMode = false;
    // }

    /**
     * Opens the edit form in the main content area for an existing future plan.
     * @param {FuturePlan} plan - The future plan to edit.
     */
    function openEditInline(plan: FuturePlan) {
      currentEditingFuturePlan = plan;
      isViewMode = false;
      isModalOpen = false; // Ensure modal is closed
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
    }

    /**
     * Handles the cancel callback from FuturePlanForm.
     * Closes the modal without saving.
     */
    function handleFormCancel() {
      closeModal();
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
                  onEditFuturePlan={(plan: FuturePlan) => openEditInline(plan)}
                  onSelectPlan={(plan: FuturePlan) => selectPlan(plan)}
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Main content - Plan details -->
        <div class={combineClasses(columnSpans.threeFourths, "h-full flex flex-col")}>
          <div class={combineClasses(cardBase, pageStyle.border, "h-full flex flex-col")}>
            <div class="p-6 flex-grow overflow-auto">
              {#if currentEditingFuturePlan}
                <!-- Edit form for the selected plan -->
                <div>
                  <div class="flex justify-between items-center mb-6">
                    <h2 class={combineClasses(headings.h2, pageStyle.text)}>
                      {currentEditingFuturePlan ? 'Edit Plan' : 'Add New Plan'}
                    </h2>
                  </div>

                  <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
                    <FuturePlanForm
                      futurePlan={currentEditingFuturePlan}
                      onSave={handleFormSave}
                      onCancel={handleFormCancel}
                    />
                  </div>
                </div>
              {:else if selectedPlan && isViewMode}
                <!-- Detailed view of the selected plan -->
                <div>
                  <div class="flex justify-between items-center mb-6">
                    <h2 class={combineClasses(headings.h2, pageStyle.text)}>
                      {selectedPlan.description || 'Plan Details'}
                    </h2>
                    <div class="flex space-x-2">
                      <button
                        onclick={() => selectedPlan && openEditInline(selectedPlan)}
                        class={combineClasses("p-2 rounded-md focus:outline-none focus:ring-2", pageStyle.text, pageStyle.hover)}
                        aria-label="Edit plan"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                      </button>
                      <button
                        onclick={() => {
                          if (selectedPlan && confirm('Are you sure you want to delete this plan?')) {
                            futurePlanStore.deleteFuturePlan(selectedPlan.id);
                            selectedPlan = null;
                            isViewMode = false;
                          }
                        }}
                        class="p-2 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
                        aria-label="Delete plan"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M3 6h18"></path>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path>
                          <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                          <line x1="10" y1="11" x2="10" y2="17"></line>
                          <line x1="14" y1="11" x2="14" y2="17"></line>
                        </svg>
                      </button>
                    </div>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Left column - Basic information -->
                    <div>
                      <div class="mb-4">
                        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Status</h3>
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium
                          {selectedPlan.status === 'active' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' :
                           selectedPlan.status === 'achieved' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300' :
                           selectedPlan.status === 'deferred' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300' :
                           'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'}">
                          {selectedPlan.status.charAt(0).toUpperCase() + selectedPlan.status.slice(1)}
                        </span>
                      </div>

                      {#if selectedPlan.target_date}
                        <div class="mb-4">
                          <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Target Date</h3>
                          <p class="text-gray-900 dark:text-white">{formatDate(selectedPlan.target_date)}</p>
                        </div>
                      {/if}

                      {#if selectedPlan.goal_type}
                        <div class="mb-4">
                          <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Goal Type</h3>
                          <p class="text-gray-900 dark:text-white">{selectedPlan.goal_type}</p>
                        </div>
                      {/if}
                    </div>

                    <!-- Right column - Description and additional info -->
                    <div>
                      <div class="mb-4">
                        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Description</h3>
                        <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg border border-gray-200 dark:border-gray-600">
                          <p class="text-gray-900 dark:text-white whitespace-pre-wrap">{selectedPlan.description}</p>
                        </div>
                      </div>

                      <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-4">
                        <span>Created: {formatDate(selectedPlan.created_at)}</span>
                        {#if selectedPlan.updated_at && selectedPlan.updated_at !== selectedPlan.created_at}
                          <span>Updated: {formatDate(selectedPlan.updated_at)}</span>
                        {/if}
                      </div>
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

    {#if isModalOpen}
      <Modal
        isOpen={isModalOpen}
        close={closeModal}
        title={currentEditingFuturePlan ? 'Edit Future Plan' : 'Add New Future Plan'}
        modalWidth="max-w-xl" >
        <FuturePlanForm
          futurePlan={currentEditingFuturePlan}
          onSave={handleFormSave}
          onCancel={handleFormCancel}
        />
      </Modal>
    {/if}
  </div>
