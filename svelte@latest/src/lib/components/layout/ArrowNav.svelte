<script lang="ts">
  import { page } from '$app/state'; // Updated from $app/stores to $app/state
  import { onMount } from 'svelte';

  // Define the order and display names of views for navigation
  const views = [
    { path: 'done', display: 'Done' },
    { path: 'doing', display: 'Doing' },
    { path: 'plan', display: 'Plan' }
  ];

  // Use $props rune for Svelte 5 with bindable property
  let { currentViewDisplay = $bindable('N/A') } = $props<{
    currentViewDisplay?: string;
  }>();
  let currentIndex = $state(-1);

  // Update the current view based on the pathname
  function updateCurrentView(pathname: string) {
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
  $effect(() => {
    updateCurrentView(page.url.pathname);
  });

  function navigateTo(direction: 'prev' | 'next') {
    try {
      // Calculate the next view index
      let nextViewIndex;

      // Handle special cases for Done and Plan pages
      if (currentViewDisplay === 'Done' && direction === 'prev') {
        console.log('Already at the first page (Done), cannot go previous');
        return;
      }

      if (currentViewDisplay === 'Plan' && direction === 'next') {
        console.log('Already at the last page (Plan), cannot go next');
        return;
      }

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

      // Use try-catch to ensure navigation doesn't block the UI even if it fails
      try {
        // Use window.location for direct navigation
        window.location.href = targetPath;
      } catch (navError) {
        console.error('Navigation error:', navError);
        // If navigation fails, try using the history API
        window.history.pushState({}, '', targetPath);
        // Trigger a popstate event to let the SvelteKit router know the URL has changed
        window.dispatchEvent(new Event('popstate'));
      }
    } catch (error) {
      console.error('Error in navigateTo function:', error);
      // Fallback: directly set location.href
      window.location.href = direction === 'next' ? '/doing' : '/done';
    }
  }
</script>

<style>
  @keyframes pulse-left {
    0% { transform: translateX(0); }
    50% { transform: translateX(-5px); }
    100% { transform: translateX(0); }
  }

  @keyframes pulse-right {
    0% { transform: translateX(0); }
    50% { transform: translateX(5px); }
    100% { transform: translateX(0); }
  }

  .arrow-left:hover svg {
    animation: pulse-left 1.5s ease-in-out infinite;
  }

  .arrow-right:hover svg {
    animation: pulse-right 1.5s ease-in-out infinite;
  }

  .arrow-button {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .arrow-button:hover {
    transform: scale(1.1);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }

  .arrow-button:active {
    transform: scale(0.95);
  }
</style>

<!-- No children rendering needed anymore -->

<!-- Left arrow button (fixed position) - hidden on /done page -->
{#if !(currentViewDisplay === 'Done')}
  <div class="fixed left-8 top-1/2 transform -translate-y-1/2 z-40">
    <button
      class="arrow-button arrow-left inline-flex items-center justify-center p-5 bg-gray-500/30 hover:bg-gray-600/70 active:bg-gray-700/80 dark:bg-gray-700/30 dark:hover:bg-gray-600/70 dark:active:bg-gray-500/80 text-gray-700 hover:text-white dark:text-gray-300 dark:hover:text-white font-medium rounded-full border border-gray-400/30 dark:border-gray-500/30 shadow-lg"
      onclick={() => navigateTo('prev')}
      title="Previous: {currentIndex !== -1 && currentIndex > 0 ? views[(currentIndex - 1 + views.length) % views.length].display : views[views.length - 1].display}"
      aria-label="Go to previous section"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </button>
  </div>
{/if}

<!-- Right arrow button (fixed position) - hidden on /plan page -->
{#if !(currentViewDisplay === 'Plan')}
  <div class="fixed right-8 top-1/2 transform -translate-y-1/2 z-40">
    <button
      class="arrow-button arrow-right inline-flex items-center justify-center p-5 bg-gray-500/30 hover:bg-gray-600/70 active:bg-gray-700/80 dark:bg-gray-700/30 dark:hover:bg-gray-600/70 dark:active:bg-gray-500/80 text-gray-700 hover:text-white dark:text-gray-300 dark:hover:text-white font-medium rounded-full border border-gray-400/30 dark:border-gray-500/30 shadow-lg"
      onclick={() => navigateTo('next')}
      title="Next: {currentIndex !== -1 ? views[(currentIndex + 1) % views.length].display : views[0].display}"
      aria-label="Go to next section"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
    </button>
  </div>
{/if}
