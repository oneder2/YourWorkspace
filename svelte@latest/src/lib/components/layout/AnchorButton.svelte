<script lang="ts">
  import { onMount } from 'svelte';

  export let isAnchorPage: boolean = false;
  let lastWorkspacePage = '/doing';

  // Update lastWorkspacePage when isAnchorPage changes
  $: {
    try {
      if (!isAnchorPage) {
        // We're not on the anchor page, store the current page
        const currentPath = window.location.pathname;
        if (currentPath !== '/anchor') {
          // Ensure the path is a valid workspace page
          if (currentPath === '/doing' || currentPath === '/done' || currentPath === '/plan') {
            lastWorkspacePage = currentPath;
            sessionStorage.setItem('lastWorkspacePage', lastWorkspacePage);
            console.log('Stored lastWorkspacePage:', lastWorkspacePage);
          } else {
            // If not a valid workspace page, use default
            lastWorkspacePage = '/doing';
          }
        }
      } else {
        // We're on the anchor page, get the last workspace page
        const storedLastWorkspacePage = sessionStorage.getItem('lastWorkspacePage');
        if (storedLastWorkspacePage) {
          lastWorkspacePage = storedLastWorkspacePage;
          console.log('Retrieved lastWorkspacePage:', lastWorkspacePage);
        } else {
          // If no stored page, use default
          lastWorkspacePage = '/doing';
          console.log('No stored lastWorkspacePage, using default:', lastWorkspacePage);
        }
      }
    } catch (error) {
      console.error('Error updating lastWorkspacePage:', error);
      // Use default on error
      lastWorkspacePage = '/doing';
    }
  }
</script>

<div class="fixed bottom-8 left-8 z-50">
  {#if isAnchorPage}
    <!-- Back button when on Anchor page -->
    <a
      href={lastWorkspacePage}
      id="anchor-button"
      class="inline-flex items-center justify-center p-4 rounded-full bg-indigo-100 dark:bg-indigo-800 border border-indigo-300 dark:border-indigo-600 text-indigo-800 dark:text-indigo-200 hover:bg-indigo-200 dark:hover:bg-indigo-700 transition-colors shadow-lg"
      aria-label="Back to workspace"
    >
      <span class="text-2xl" aria-hidden="true">⬅️</span>
    </a>
  {:else}
    <!-- Anchor button when not on Anchor page -->
    <a
      href="/anchor"
      id="anchor-button"
      class="inline-flex items-center justify-center p-4 rounded-full bg-amber-100 dark:bg-amber-800 border border-amber-300 dark:border-amber-600 text-amber-800 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-amber-700 transition-colors shadow-lg"
      aria-label="Go to My Anchor"
    >
      <span class="text-2xl" aria-hidden="true">⚓️</span>
    </a>
  {/if}
</div>
