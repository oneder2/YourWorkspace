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
     * Handles the 'save' event dispatched by FuturePlanForm.
     * Closes the modal after a successful save. The list will update reactively.
     * @param {CustomEvent<FuturePlan>} event - The event containing the saved future plan.
     */
    function handleFormSave(event: CustomEvent<FuturePlan>) {
      closeModal();
      // Optional: Display a success notification (e.g., using a toast message system)
      // console.log('Future Plan saved successfully:', event.detail);
    }
  
    /**
     * Handles the 'cancel' event dispatched by FuturePlanForm.
     * Closes the modal without saving.
     */
    function handleFormCancel() {
      closeModal();
    }
  </script>
  
  <div class="page-container p-4 md:p-8">
    <FuturePlanList
      on:addNewFuturePlan={openCreateModal}
      on:editFuturePlan={openEditModal}
    />
  
    {#if isModalOpen}
      <Modal 
        isOpen={isModalOpen} 
        on:close={closeModal} 
        title={currentEditingFuturePlan ? 'Edit Future Plan' : 'Add New Future Plan'}
        modalWidth="max-w-xl" >
        <FuturePlanForm
          futurePlan={currentEditingFuturePlan}
          on:save={handleFormSave}
          on:cancel={handleFormCancel}
        />
        </Modal>
    {/if}
  </div>
  
  <style>
    /* Page-specific styles can be added here if necessary */
    .page-container {
      max-width: 1200px; /* Example: Limit the maximum width of the page content */
      margin-left: auto;
      margin-right: auto;
    }
    /* Example: If you were to use a shared button style from a global CSS or a utility component */
    /* .button { padding: 0.5rem 1rem; border-radius: 0.25rem; } */
    /* .primary { background-color: blue; color: white; } */
    /* .secondary { background-color: gray; color: white; } */
  </style>
  