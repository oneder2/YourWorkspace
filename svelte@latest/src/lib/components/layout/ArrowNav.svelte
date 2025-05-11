<script lang="ts">
  import { page } from '$app/state'; // Updated from $app/stores to $app/state
  import { onMount } from 'svelte';

  // Define the order and display names of views for navigation
  const views = [
    { path: 'done', display: 'Done' },
    { path: 'doing', display: 'Doing' },
    { path: 'plan', display: 'Plan' }
  ];

  let currentViewDisplay = 'N/A';
  let currentIndex = -1;
  let currentPath = '';

  // Update the current view based on the pathname
  function updateCurrentView(pathname: string) {
    currentPath = pathname;
    console.log("Current path:", pathname);

    // Try exact match first
    for (let i = 0; i < views.length; i++) {
      if (pathname === `/${views[i].path}`) {
        currentIndex = i;
        currentViewDisplay = views[i].display;
        console.log(`Exact match found: ${views[i].path}, index: ${i}`);
        return;
      }
    }

    // Try includes match if exact match fails
    for (let i = 0; i < views.length; i++) {
      if (pathname.includes(`/${views[i].path}`)) {
        currentIndex = i;
        currentViewDisplay = views[i].display;
        console.log(`Partial match found: ${views[i].path}, index: ${i}`);
        return;
      }
    }

    // No match found
    currentIndex = -1;
    currentViewDisplay = 'N/A';
    console.log("No match found");
  }

  // Initial update on mount
  onMount(() => {
    updateCurrentView(page.url.pathname);
  });

  // Update when page changes
  $: updateCurrentView(page.url.pathname);

  function navigateTo(direction: 'prev' | 'next') {
    // Calculate the next view index
    let nextViewIndex;

    if (currentIndex === -1) {
      // If current path is not in views array, default to first view for next, last view for prev
      nextViewIndex = direction === 'next' ? 0 : views.length - 1;
    } else {
      if (direction === 'prev') {
        nextViewIndex = (currentIndex - 1 + views.length) % views.length;
      } else { // next
        nextViewIndex = (currentIndex + 1) % views.length;
      }
    }

    // Navigate to the selected view
    const targetPath = `/${views[nextViewIndex].path}`;
    console.log(`Navigating to: ${targetPath}`);

    // Use window.location for direct navigation to ensure it works
    window.location.href = targetPath;
  }
</script>

<div class="py-2 px-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
  <div class="flex justify-between items-center w-full max-w-3xl mx-auto">
    <button
      class="inline-flex items-center justify-center px-4 py-2 bg-gray-100 hover:bg-gray-200 active:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 dark:active:bg-gray-500 text-gray-700 dark:text-gray-200 font-medium text-sm rounded-md border border-gray-300 dark:border-gray-600 transition-colors"
      on:click={() => navigateTo('prev')}
      title="Previous: {currentIndex !== -1 && currentIndex > 0 ? views[(currentIndex - 1 + views.length) % views.length].display : views[views.length - 1].display}"
      aria-label="Go to previous section"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><polyline points="15 18 9 12 15 6"></polyline></svg>
      <span>Prev</span>
    </button>

    <div
      class="px-6 py-2 min-w-[120px] text-center text-lg font-bold text-gray-800 dark:text-gray-200 bg-white dark:bg-gray-800"
      aria-live="polite"
      aria-atomic="true"
    >
      {currentViewDisplay}
    </div>

    <button
      class="inline-flex items-center justify-center px-4 py-2 bg-gray-100 hover:bg-gray-200 active:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 dark:active:bg-gray-500 text-gray-700 dark:text-gray-200 font-medium text-sm rounded-md border border-gray-300 dark:border-gray-600 transition-colors"
      on:click={() => navigateTo('next')}
      title="Next: {currentIndex !== -1 ? views[(currentIndex + 1) % views.length].display : views[0].display}"
      aria-label="Go to next section"
    >
      <span>Next</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="ml-2"><polyline points="9 18 15 12 9 6"></polyline></svg>
    </button>
  </div>
</div>
