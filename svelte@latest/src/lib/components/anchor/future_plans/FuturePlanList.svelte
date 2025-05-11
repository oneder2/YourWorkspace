<script lang="ts">
    // Import necessary Svelte and project modules
    import { onMount } from 'svelte';
    import { futurePlanStore } from '$lib/store/futurePlanStore'; // Main store for future plans
    import FuturePlanItem from './FuturePlanItem.svelte'; // Component to display a single future plan

    // Component Props using $props rune
    let {
      onAddNewFuturePlan = () => {},
      onEditFuturePlan = (plan: any) => {}
    } = $props<{
      onAddNewFuturePlan?: () => void;
      onEditFuturePlan?: (plan: any) => void;
    }>();

    // Subscribe to reactive stores from futurePlanStore
    // These will automatically update the component when their values change.
    const futurePlans = futurePlanStore.futurePlans; // Writable<FuturePlan[]>
    const isLoading = futurePlanStore.isLoading;     // Writable<boolean>
    const error = futurePlanStore.error;             // Writable<string | null>

    // Lifecycle hook: Called after the component has been mounted to the DOM.
    onMount(() => {
      // Attempt to load future plans if the list is currently empty,
      // not already loading, and there's no existing error.
      // This ensures data is fetched when the component first loads.
      // The store itself also has logic to load on auth change, this is an additional trigger.
      if ($futurePlans.length === 0 && !$isLoading && !$error) {
        futurePlanStore.loadFuturePlans();
      }
    });

    // Direct dispatch from FuturePlanItem to parent page is now handled inline

    /**
     * Handles the click event for the "Add New Future Plan" button.
     * It calls the onAddNewFuturePlan callback for the parent page to handle (e.g., open a modal).
     */
    function handleAddNewRequest() {
      onAddNewFuturePlan();
    }
  </script>

  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-800 dark:text-white">我的未来计划</h2>
      <button
        onclick={handleAddNewRequest}
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition ease-in-out duration-150"
        aria-label="Add a new future plan"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block mr-2 -mt-0.5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        添加新计划
      </button>
    </div>

    {#if $isLoading && $futurePlans.length === 0}
      <div class="text-center py-10">
        <div role="status" class="flex justify-center items-center">
            <svg aria-hidden="true" class="w-10 h-10 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0492C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="lightgray"/>
            </svg>
            <span class="sr-only">Loading...</span>
        </div>
        <p class="mt-2 text-gray-600 dark:text-gray-400">正在加载未来计划...</p>
      </div>
    {:else if $error}
      <div class="p-4 mb-4 text-sm text-red-700 bg-red-100 rounded-lg dark:bg-red-200 dark:text-red-800 text-center" role="alert">
        <span class="font-medium">加载错误：</span> {$error}
        <button
          onclick={() => futurePlanStore.loadFuturePlans()}
          class="ml-4 px-3 py-1.5 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
        >
          重试
        </button>
      </div>
    {:else if $futurePlans.length === 0}
      <div class="text-center py-10">
        <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-2 text-lg font-medium text-gray-900 dark:text-white">暂无未来计划</h3>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">开始规划您的未来吧！</p>
      </div>
    {:else}
      <div class="space-y-4">
        {#each $futurePlans as plan (plan.id)}
          <FuturePlanItem futurePlan={plan} onEdit={(plan) => onEditFuturePlan(plan)} />
        {/each}
      </div>
    {/if}
  </div>
