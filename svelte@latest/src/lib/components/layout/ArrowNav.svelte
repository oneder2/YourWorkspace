<script lang="ts">
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { onDestroy } from 'svelte';

  // Define the order and display names of views for navigation
  const views = [
    { path: 'done', display: 'Done' },
    { path: 'doing', display: 'Doing' },
    { path: 'plan', display: 'Plan' }
  ];

  let currentViewDisplay = '';
  let currentIndex = -1;

  const unsubscribePage = page.subscribe(currentPage => {
    const currentPathBase = currentPage.url.pathname.split('/').pop() || '';
    currentIndex = views.findIndex(v => v.path === currentPathBase);
    if (currentIndex !== -1) {
      currentViewDisplay = views[currentIndex].display;
    } else {
      currentViewDisplay = 'N/A'; // Fallback if path doesn't match
    }
  });

  onDestroy(() => {
    unsubscribePage();
  });

  function navigateTo(direction: 'prev' | 'next') {
    if (currentIndex === -1) return; // Current path not in views array

    let nextViewIndex;
    if (direction === 'prev') {
      nextViewIndex = (currentIndex - 1 + views.length) % views.length;
    } else { // next
      nextViewIndex = (currentIndex + 1) % views.length;
    }
    // Assumes routes are like /done, /doing, /plan directly under the (app) group
    goto(`/${views[nextViewIndex].path}`);
  }
</script>

<div class="py-3 px-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm mb-6">
  <div class="flex justify-between items-center w-full max-w-xl mx-auto">
    <button
      class="inline-flex items-center justify-center px-4 py-2 bg-primary-500 hover:bg-primary-600 active:bg-primary-700 text-white font-medium text-sm rounded-lg shadow-sm hover:-translate-y-0.5 active:translate-y-0 transition-all"
      on:click={() => navigateTo('prev')}
      title="Previous: {currentIndex !== -1 && currentIndex > 0 ? views[(currentIndex - 1 + views.length) % views.length].display : views[views.length - 1].display}"
      aria-label="Go to previous section"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 sm:mr-0"><polyline points="15 18 9 12 15 6"></polyline></svg>
      <span class="sm:hidden">Prev</span>
    </button>

    <div
      class="px-6 py-2 min-w-[120px] sm:min-w-[100px] text-center text-lg sm:text-base font-semibold text-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 rounded-md shadow-inner"
      aria-live="polite"
      aria-atomic="true"
    >
      {currentViewDisplay}
    </div>

    <button
      class="inline-flex items-center justify-center px-4 py-2 bg-primary-500 hover:bg-primary-600 active:bg-primary-700 text-white font-medium text-sm rounded-lg shadow-sm hover:-translate-y-0.5 active:translate-y-0 transition-all"
      on:click={() => navigateTo('next')}
      title="Next: {currentIndex !== -1 ? views[(currentIndex + 1) % views.length].display : views[0].display}"
      aria-label="Go to next section"
    >
      <span class="sm:hidden">Next</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="ml-2 sm:ml-0"><polyline points="9 18 15 12 9 6"></polyline></svg>
    </button>
  </div>
</div>
