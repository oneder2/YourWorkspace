<script lang="ts">
    // Import necessary Svelte components and types
    import FuturePlanList from '$lib/components/anchor/future_plans/FuturePlanList.svelte';
    import FuturePlanForm from '$lib/components/anchor/future_plans/FuturePlanForm.svelte';
    import Modal from '$lib/components/common/Modal.svelte'; // Assuming Modal component path is correct
    import type { FuturePlan } from '$lib/services/futurePlanService';
    // futurePlanStore might be used here for specific actions if needed, but list updates are reactive
    // import { futurePlanStore } from '$lib/store/futurePlanStore';
    // import { onMount, get } from 'svelte/store'; // get is from svelte/store if you need to read store value once


    // State variable to control the visibility of the modal
    let isModalOpen = false;
    // State variable to hold the future plan being edited. Null for creating a new one.
    let currentEditingFuturePlan: FuturePlan | null = null;

    /*
    // onMount(() => {
    //   // Initial data loading can be triggered here or within FuturePlanList.
    //   // FuturePlanList currently handles its own initial loading in its onMount.
    // });
    */

    /**
     * Opens the modal in 'create' mode for adding a new future plan.
     * This function is called when FuturePlanList dispatches 'addNewFuturePlan'.
     */
    function openCreateModal() {
      currentEditingFuturePlan = null; // Ensure form is in create mode
      isModalOpen = true; // Open the modal
    }

    /**
     * Opens the modal in 'edit' mode for an existing future plan.
     * This function is called when FuturePlanList dispatches 'editFuturePlan'.
     * @param {CustomEvent<FuturePlan>} event - The event containing the future plan to edit.
     */
    function openEditModal(event: CustomEvent<FuturePlan>) {
      currentEditingFuturePlan = event.detail; // Set the future plan to be edited
      isModalOpen = true; // Open the modal
    }

    /**
     * Closes the modal and resets the editing state.
     * This function is called by the Modal component (on:close event) or after form actions.
     */
    function closeModal() {
      isModalOpen = false; // Close the modal
      currentEditingFuturePlan = null; // Clear any future plan being edited
    }

    /**
     * Handles the save callback from FuturePlanForm.
     * Closes the modal after a successful save. The list will update reactively.
     * @param {FuturePlan} _plan - The saved future plan (unused).
     */
    function handleFormSave(_plan: FuturePlan) {
      closeModal();
      // Optional: Display a success notification (e.g., using a toast message system)
      // console.log('Future Plan saved successfully:', _plan);
    }

    /**
     * Handles the cancel callback from FuturePlanForm.
     * Closes the modal without saving.
     */
    function handleFormCancel() {
      closeModal();
    }
  </script>

  <div class="max-w-7xl mx-auto px-4 py-4">
    <div class="p-6 bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800 rounded-lg shadow mb-6">
      <h2 class="text-xl font-semibold text-green-900 dark:text-green-100 mb-4 flex items-center">
        <span class="text-green-500 mr-2">🚀</span>
        Future Plans
      </h2>

      <FuturePlanList
        onAddNewFuturePlan={openCreateModal}
        onEditFuturePlan={openEditModal}
      />
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
