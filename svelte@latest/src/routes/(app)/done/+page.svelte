<script lang="ts">
    // Import necessary Svelte components and types
    import AchievementList from '$lib/components/anchor/achievements/AchievementList.svelte';
    import AchievementForm from '$lib/components/anchor/achievements/AchievementForm.svelte';
    import Modal from '$lib/components/common/Modal.svelte'; // Assuming Modal component path is correct
    import type { Achievement } from '$lib/services/achievementService';
    // achievementStore might be used here for specific actions if needed, but list updates are reactive
    // import { achievementStore } from '$lib/store/achievementStore';
    // import { onMount, get } from 'svelte'; // get is from svelte/store if you need to read store value once

    // State variable to control the visibility of the modal
    let isModalOpen = false;
    // State variable to hold the achievement being edited. Null for creating a new one.
    let currentEditingAchievement: Achievement | null = null;

    /*
    // onMount(() => {
    //   // Initial data loading can be triggered here or within AchievementList.
    //   // AchievementList currently handles its own initial loading in its onMount.
    //   // If achievements are not loaded and not currently loading, trigger load:
    //   // if (get(achievementStore.achievements).length === 0 && !get(achievementStore.isLoading)) {
    //   //   achievementStore.loadAchievements();
    //   // }
    // });
    */

    /**
     * Opens the modal in 'create' mode for adding a new achievement.
     * This function is called when AchievementList dispatches 'addNewAchievement'.
     */
    function openCreateModal() {
      currentEditingAchievement = null; // Ensure form is in create mode
      isModalOpen = true; // Open the modal
    }

    /**
     * Opens the modal in 'edit' mode for an existing achievement.
     * This function is called as a callback prop from AchievementList.
     * @param {Achievement} achievement - The achievement to edit.
     */
    function openEditModal(achievement: Achievement) {
      currentEditingAchievement = achievement; // Set the achievement to be edited
      isModalOpen = true; // Open the modal
    }

    /**
     * Closes the modal and resets the editing state.
     * This function is called by the Modal component (on:close event) or after form actions.
     */
    function closeModal() {
      isModalOpen = false; // Close the modal
      currentEditingAchievement = null; // Clear any achievement being edited
    }

    /**
     * Handles the save action from AchievementForm.
     * Closes the modal after a successful save. The list will update reactively.
     * @param {Achievement} achievement - The saved achievement.
     */
    function handleFormSave(achievement: Achievement) {
      closeModal();
      // Optional: Display a success notification (e.g., using a toast message system)
      console.log('Achievement saved successfully:', achievement);
    }

    /**
     * Handles the 'cancel' event dispatched by AchievementForm.
     * Closes the modal without saving.
     */
    function handleFormCancel() {
      closeModal();
    }
  </script>

  <div class="max-w-7xl mx-auto p-4 md:p-8">
    <AchievementList
      addNewAchievement={openCreateModal}
      editAchievement={openEditModal}
    />

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
