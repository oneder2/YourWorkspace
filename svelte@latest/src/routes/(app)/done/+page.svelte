<script lang="ts">
    // Import necessary Svelte components and types
    import AchievementList from '$lib/components/anchor/achievements/AchievementList.svelte';
    import AchievementForm from '$lib/components/anchor/achievements/AchievementForm.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import type { Achievement } from '$lib/services/achievementService';
    import { authStore } from '$lib/store/authStore';
    import { profileService, type ProfileUpdateDto } from '$lib/services/profileService';
    import { onMount } from 'svelte';
    import {
      pageContainer,
      colorSchemes,
      layouts,
      columnSpans,
      headings,
      scrollArea,
      cardBase,
      formElements,
      buttons,
      combineClasses
    } from '$lib/styles/pageStyles';

    // 获取当前页面的颜色方案
    const pageStyle = colorSchemes.done;

    // State variables for user profile
    let skill = $state('');
    let summary = $state('');
    let isEditingProfile = $state(false);

    // State variable to control the visibility of the modal
    let isModalOpen = $state(false);
    // State variable to hold the achievement being edited. Null for creating a new one.
    let currentEditingAchievement: Achievement | null = $state(null);

    // Subscribe to auth store to get user profile data
    onMount(() => {
      const unsubscribe = authStore.subscribe(state => {
        if (state.user) {
          skill = state.user.skill || '';
          summary = state.user.summary || '';
        }
      });

      return unsubscribe;
    });

    /**
     * Opens the modal in 'create' mode for adding a new achievement.
     */
    function openCreateModal() {
      currentEditingAchievement = null;
      isModalOpen = true;
    }

    /**
     * Opens the modal in 'edit' mode for an existing achievement.
     * @param {Achievement} achievement - The achievement to edit.
     */
    function openEditModal(achievement: Achievement) {
      currentEditingAchievement = achievement;
      isModalOpen = true;
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
     * @param {Achievement} _achievement - The saved achievement (unused as store handles updates).
     */
    function handleFormSave(_achievement: Achievement) {
      closeModal();
      // The achievement store will handle updating the UI automatically
      // since the AchievementForm component already updates the store
    }

    /**
     * Handles the 'cancel' event dispatched by AchievementForm.
     */
    function handleFormCancel() {
      closeModal();
    }

    /**
     * Toggles the profile editing state
     */
    function toggleProfileEdit() {
      isEditingProfile = !isEditingProfile;
    }

    /**
     * Saves the user profile data
     */
    async function saveProfile() {
      try {
        // Create profile update data
        const profileData: ProfileUpdateDto = {
          skill,
          summary
        };

        // Call the profile service to update the profile
        const updatedProfile = await profileService.updateProfile(profileData);

        // Get current auth state
        let currentUser: any = null;
        const unsubscribe = authStore.subscribe(state => {
          currentUser = state.user;
        });
        unsubscribe();

        // Update the auth store with the new profile data
        authStore.setUserProfile({
          ...updatedProfile,
          id: currentUser?.id || null,
          username: currentUser?.username || null,
          email: currentUser?.email || null
        });

        console.log('Profile updated successfully:', updatedProfile);
        isEditingProfile = false;
      } catch (error) {
        console.error('Error saving profile:', error);
        alert('Failed to save profile. Please try again.');
      }
    }
  </script>

  <div class={pageContainer}>
    <!-- Two-column layout -->
    <div class={layouts.twoColumnOneThree}>
      <!-- Left sidebar - User profile information -->
      <div class={columnSpans.oneFourth}>
        <div class={combineClasses(cardBase, "bg-white dark:bg-gray-800", pageStyle.border)}>
          <!-- Skill section -->
          <div class="p-4 border-b border-gray-200 dark:border-gray-700">
            <div class="flex justify-between items-center mb-2">
              <h3 class={headings.h3}>Skill:</h3>
              {#if !isEditingProfile}
                <button
                  onclick={toggleProfileEdit}
                  class={combineClasses("text-sm", pageStyle.text, pageStyle.hover)}
                >
                  Edit
                </button>
              {/if}
            </div>

            {#if isEditingProfile}
              <textarea
                bind:value={skill}
                class={formElements.textarea}
                rows="4"
                placeholder="Enter your skills here..."
              ></textarea>
            {:else}
              <p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                {skill || 'No skills added yet.'}
              </p>
            {/if}
          </div>

          <!-- Summary section -->
          <div class="p-4">
            <h3 class={headings.h3}>Summary:</h3>

            {#if isEditingProfile}
              <textarea
                bind:value={summary}
                class={formElements.textarea}
                rows="6"
                placeholder="Enter your summary here..."
              ></textarea>

              <div class="flex justify-end mt-4 space-x-2">
                <button
                  onclick={toggleProfileEdit}
                  class={combineClasses(buttons.small, pageStyle.button.secondary)}
                >
                  Cancel
                </button>
                <button
                  onclick={saveProfile}
                  class={combineClasses(buttons.small, pageStyle.button.primary)}
                >
                  Save
                </button>
              </div>
            {:else}
              <p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                {summary || 'No summary added yet.'}
              </p>
            {/if}
          </div>
        </div>
      </div>

      <!-- Main content - Achievements -->
      <div class={columnSpans.threeFourths}>
        <div class={combineClasses(cardBase, "bg-white dark:bg-gray-800", pageStyle.border)}>
          <div class="p-6">
            <h2 class={combineClasses(headings.h2, pageStyle.text)}>
              <span class={combineClasses(pageStyle.icon, "mr-2")}>🏆</span>
              My Achievements
            </h2>

            <!-- Scrollable container with fixed height -->
            <div class={scrollArea.container}>
              <!-- Scrollbar indicator on the right -->
              <div class={combineClasses("absolute right-0 top-0 bottom-0 w-1 opacity-50", pageStyle.scrollbar)}></div>

              <!-- Scrollable content -->
              <div class={combineClasses("pr-3", scrollArea.content)}>
                <AchievementList
                  addNewAchievement={openCreateModal}
                  editAchievement={openEditModal}
                />
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
