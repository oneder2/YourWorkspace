<script lang="ts">
    // Import necessary Svelte and project modules
    import { get } from 'svelte/store'; // To read store values imperatively
    import type { FuturePlan, FuturePlanCreateDto, FuturePlanUpdateDto } from '$lib/services/futurePlanService';
    import { futurePlanStore } from '$lib/store/futurePlanStore'; // The store for future plans

    // Component Props using $props rune
    let {
      futurePlan = null,
      onSave = (plan: FuturePlan) => {},
      onCancel = () => {}
    } = $props<{
      futurePlan: FuturePlan | null;
      onSave?: (plan: FuturePlan) => void;
      onCancel?: () => void;
    }>();

    // Local state for form fields, initialized from `futurePlan` prop if in edit mode
    let title = $state(futurePlan?.title || '');
    let description = $state(futurePlan?.description || '');
    let goal_type = $state(futurePlan?.goal_type || '');
    let target_date = $state(futurePlan?.target_date || ''); // Expected format: YYYY-MM-DD
    let status = $state<'active' | 'achieved' | 'deferred' | 'abandoned'>(futurePlan?.status || 'active');

    // Local state for form feedback and loading status
    let formError = $state<string | null>(null);
    let formSuccess = $state<string | null>(null);
    let internalIsLoading = $state(false); // For form-specific loading state

    // Available statuses for the select dropdown
    const statuses: Array<'active' | 'achieved' | 'deferred' | 'abandoned'> = [
      'active',
      'achieved',
      'deferred',
      'abandoned',
    ];

    // Explicitly get the isLoading store from futurePlanStore
    const isLoadingStore = futurePlanStore.isLoading;
    // Reactive subscription to the store's global loading state for the submit button
    let storeIsLoading = $derived($isLoadingStore);

    // Update form fields when futurePlan prop changes
    $effect(() => {
      if (futurePlan) {
        title = futurePlan.title || '';
        description = futurePlan.description || '';
        goal_type = futurePlan.goal_type || '';
        target_date = futurePlan.target_date || '';
        status = futurePlan.status || 'active';
        formError = null; // Clear previous errors when plan changes
        formSuccess = null;
      } else {
        // Reset for create mode if futurePlan becomes null or is initially null
        title = '';
        description = '';
        goal_type = '';
        target_date = '';
        status = 'active';
      }
    });

    /**
     * Handles the form submission for creating or updating a future plan.
     */
    async function handleSubmit() {
      formError = null;
      formSuccess = null;
      internalIsLoading = true;

      // Basic validation: title and description are required
      if (!title.trim()) {
        formError = 'Title cannot be empty.';
        internalIsLoading = false;
        return;
      }

      if (!description.trim()) {
        formError = 'Description cannot be empty.';
        internalIsLoading = false;
        return;
      }

      if (futurePlan && futurePlan.id) {
        // Edit mode: Prepare update DTO
        const planData: FuturePlanUpdateDto = {
          title: title.trim(),
          description: description.trim(),
          goal_type: goal_type.trim() || null,
          target_date: target_date || null,
          status: status,
        };
        try {
          const updated = await futurePlanStore.updateFuturePlan(futurePlan.id, planData);
          if (updated) {
            formSuccess = 'Future plan updated successfully!';
            onSave(updated); // Call the callback prop instead of dispatching an event
          } else {
            // Read error from store if update failed at store/service level
            formError = get(futurePlanStore.error) || 'Failed to update future plan.';
          }
        } catch (e: any) {
          formError = e.message || 'An unknown error occurred while updating.';
        }
      } else {
        // Create mode: Prepare create DTO
        const planData: FuturePlanCreateDto = {
          title: title.trim(),
          description: description.trim(),
          goal_type: goal_type.trim() || undefined, // Send undefined if empty, API might treat null/undefined differently
          target_date: target_date || undefined,
          status: status,
        };
        try {
          const created = await futurePlanStore.addFuturePlan(planData);
          if (created) {
            formSuccess = 'Future plan added successfully!';
            onSave(created); // Call the callback prop instead of dispatching an event
            resetForm(); // Reset form fields after successful creation
          } else {
            // Read error from store if creation failed
            formError = get(futurePlanStore.error) || 'Failed to add future plan.';
          }
        } catch (e: any) {
          formError = e.message || 'An unknown error occurred while adding.';
        }
      }
      internalIsLoading = false;
    }

    /**
     * Resets the form fields to their initial (empty or default) state.
     * Typically used after successful creation or when explicitly cancelled in create mode.
     */
    function resetForm() {
      title = '';
      description = '';
      goal_type = '';
      target_date = '';
      status = 'active';
      formError = null;
      // formSuccess = null; // Optionally clear success message on reset, or let it persist briefly
    }

    /**
     * Handles the cancel action.
     * If editing, calls the onCancel callback (for a modal to handle).
     * If creating, resets the form.
     */
    function handleCancel() {
      if (futurePlan) { // If in edit mode
        onCancel();
      } else { // If in create mode
        resetForm();
        formSuccess = null; // Clear any success message on cancel
      }
    }

  </script>

  <form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="space-y-6">
    {#if formError}
      <div class="p-3 mb-4 text-sm text-red-700 bg-red-100 rounded-lg dark:bg-red-200 dark:text-red-800" role="alert">
        <span class="font-medium">Error:</span> {formError}
      </div>
    {/if}
    {#if formSuccess}
      <div class="p-3 mb-4 text-sm text-green-700 bg-green-100 rounded-lg dark:bg-green-200 dark:text-green-800" role="alert">
        <span class="font-medium">Success:</span> {formSuccess}
      </div>
    {/if}

    <div class="mb-6">
      <label for="fp-title" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
        Title <span class="text-red-500">*</span>
      </label>
      <input
        type="text"
        id="fp-title"
        bind:value={title}
        required
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500"
        placeholder="Enter a title for your future plan..."
      />
    </div>

    <div class="mb-6">
      <label for="fp-description" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
        Description <span class="text-red-500">*</span>
      </label>
      <textarea
        id="fp-description"
        bind:value={description}
        rows="4"
        required
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500"
        placeholder="Describe your future plan or goal in detail..."
      ></textarea>
    </div>

    <div class="mb-6">
      <label for="fp-status" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
        Status
      </label>
      <select
        id="fp-status"
        bind:value={status}
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500"
      >
        {#each statuses as s}
          <option value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
        {/each}
      </select>
    </div>

    <div class="mb-6">
      <label for="fp-goal_type" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
        Goal Type (Optional)
      </label>
      <input
        type="text"
        id="fp-goal_type"
        bind:value={goal_type}
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500"
        placeholder="e.g., Career, Personal, Financial"
      />
    </div>

    <div class="mb-6">
      <label for="fp-target_date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
        Target Date (Optional)
      </label>
      <input
        type="date"
        id="fp-target_date"
        bind:value={target_date}
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500"
      />
    </div>

    <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
      <button
        type="button"
        onclick={handleCancel}
        class="py-2.5 px-5 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-green-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
      >
        {futurePlan ? 'Cancel' : 'Reset'}
      </button>
      <button
        type="submit"
        disabled={internalIsLoading || storeIsLoading}
        class="text-white bg-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800 disabled:opacity-50"
      >
        {#if internalIsLoading || storeIsLoading}
          <svg aria-hidden="true" role="status" class="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
            <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0492C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
          </svg>
          Processing...
        {:else}
          {futurePlan ? 'Save Changes' : 'Add Plan'}
        {/if}
      </button>
    </div>
  </form>
