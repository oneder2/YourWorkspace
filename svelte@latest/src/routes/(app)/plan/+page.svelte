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
     * @param {FuturePlan} plan - The future plan to edit.
     */
    function openEditModal(plan: FuturePlan) {
      currentEditingFuturePlan = plan;
      isModalOpen = true;
      isViewMode = false;
    }

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

  <div class={pageContainer}>
    <div class="mb-6">
      <h1 class={combineClasses(headings.h1, pageStyle.text)}>
        <span class={combineClasses(pageStyle.icon, "mr-2")}>🚀</span>
        Future Plan
      </h1>

      <!-- Main content with two-column layout -->
      <div class={layouts.twoColumnOneThree}>
        <!-- Left sidebar - List of plans -->
        <div class={combineClasses(columnSpans.oneFourth, cardBase, "bg-white dark:bg-gray-800", pageStyle.border)}>
          <div class="p-4 border-b border-gray-200 dark:border-gray-700">
            <div class="flex justify-between items-center">
              <h3 class={headings.h3}>Plans</h3>
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
          <div class={scrollArea.container}>
            <!-- Scrollbar indicator on the left -->
            <div class={combineClasses("absolute left-0 top-0 bottom-0 w-1 opacity-50", pageStyle.scrollbar)}></div>

            <!-- Scrollable content -->
            <div class={combineClasses("pl-3", scrollArea.content)}>
              <FuturePlanList
                onAddNewFuturePlan={openCreateModal}
                onEditFuturePlan={(plan: FuturePlan) => openEditModal(plan)}
                onSelectPlan={(plan: FuturePlan) => selectPlan(plan)}
              />
            </div>
          </div>
        </div>

        <!-- Main content - Plan details or form -->
        <div class={combineClasses(columnSpans.threeFourths, cardBase, "bg-white dark:bg-gray-800", pageStyle.border)}>
          <div class="p-6">
            {#if currentEditingFuturePlan}
              <h2 class={combineClasses(headings.h2, pageStyle.text)}>
                Edit Plan
              </h2>
              <FuturePlanForm
                futurePlan={currentEditingFuturePlan}
                onSave={handleFormSave}
                onCancel={handleFormCancel}
              />
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
                      class="px-3 py-1 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
                      aria-label="Edit plan"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
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
                      class="px-3 py-1 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
                      aria-label="Delete plan"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
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
              <div class="flex flex-col items-center justify-center h-[calc(100vh-400px)]">
                <svg xmlns="http://www.w3.org/2000/svg" class={combineClasses("h-16 w-16 mb-4", pageStyle.icon)} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
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
