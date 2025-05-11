<script lang="ts">
  import { authService } from '$lib/services/authService';
  import { authStore, type UserProfile, isAuthenticated } from '$lib/store/authStore';
  import { goto } from '$app/navigation';
  import { page } from '$app/state'; // Updated from $app/stores to $app/state
  import { get } from 'svelte/store';

  export let isAnchorPage: boolean = false; // New prop

  let currentUser: UserProfile | null = null;
  let lastWorkspacePage: string = '/doing';

  let previousPageBeforeAnchor: string | null = null;

  // Use reactive statement instead of subscribe since page is not a store in Svelte 5
  $: {
    const path = page.url.pathname;
    if (!path.startsWith('/anchor') && (path.startsWith('/done') || path.startsWith('/doing') || path.startsWith('/plan'))) {
      previousPageBeforeAnchor = path;
    }
    if (path.startsWith('/anchor') && previousPageBeforeAnchor) {
        lastWorkspacePage = previousPageBeforeAnchor;
    } else if (path.startsWith('/anchor') && !previousPageBeforeAnchor) {
        lastWorkspacePage = '/doing';
    }
  }

  authStore.subscribe(value => {
    currentUser = value.user;
  });

  async function handleLogout() {
    try {
      await authService.logoutUser();
    } catch (error) {
      console.error('Failed to logout from navbar:', error);
      if (get(isAuthenticated)) {
          authStore.logout();
      }
      await goto('/login');
    }
  }

</script>

<nav class="sticky top-0 z-navbar bg-indigo-50 dark:bg-indigo-900 border-b border-indigo-200 dark:border-indigo-700 shadow-sm">
  <div class="flex justify-between items-center w-full px-4 py-3">
    {#if isAnchorPage}
      <!-- Anchor page navigation -->
      <div class="flex-shrink-0">
        <a
          href={lastWorkspacePage}
          class="inline-flex items-center px-4 py-2 rounded-md border border-indigo-300 dark:border-indigo-600 text-indigo-800 dark:text-indigo-200 hover:bg-indigo-100 dark:hover:bg-indigo-800 transition-colors"
        >
          <span class="mr-2 text-lg" aria-hidden="true">⬅️</span>
          <span class="font-medium text-sm md:inline hidden">Back to Workspace</span>
        </a>
      </div>
      <div class="flex items-center">
        {#if currentUser}
          <button
            class="p-2 rounded-md border border-indigo-300 dark:border-indigo-600 text-indigo-700 dark:text-indigo-300 hover:bg-indigo-100 dark:hover:bg-indigo-800 transition-colors"
            on:click={handleLogout}
            title="Logout"
            aria-label="Logout"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
          </button>
        {/if}
      </div>
    {:else}
      <!-- Main workspace navigation -->
      <div class="flex-shrink-0">
        <a href="/doing" class="flex items-center text-2xl font-bold text-indigo-900 dark:text-indigo-100 hover:opacity-85 transition-opacity" aria-label="Go to Dashboard">
          Personal Workspace
        </a>
      </div>
      <div class="flex-grow flex justify-center items-center">
        <a
          href="/anchor"
          class="inline-flex items-center px-4 py-2 rounded-md bg-amber-100 dark:bg-amber-800 border border-amber-300 dark:border-amber-600 text-amber-800 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-amber-700 transition-colors"
        >
          <span class="mr-2 text-lg" aria-hidden="true">⚓️</span>
          <span class="font-medium">My Anchor</span>
        </a>
      </div>
      <div class="flex items-center">
        {#if currentUser}
          <div class="flex items-center">
            <span class="mr-3 text-base font-medium text-indigo-700 dark:text-indigo-300" title={currentUser.email || ''}>
              Hello, {currentUser.username || currentUser.email?.split('@')[0]}!
            </span>
            <button
              class="inline-flex items-center px-3 py-2 rounded-md bg-indigo-100 dark:bg-indigo-800 border border-indigo-300 dark:border-indigo-600 text-indigo-700 dark:text-indigo-300 hover:bg-indigo-200 dark:hover:bg-indigo-700 transition-colors"
              on:click={handleLogout}
              title="Logout"
              aria-label="Logout"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
              <span>Logout</span>
            </button>
          </div>
        {:else}
          <div class="flex items-center space-x-2">
            <a
              href="/login"
              class="inline-flex items-center px-3 py-2 rounded-md bg-indigo-100 dark:bg-indigo-800 text-indigo-700 dark:text-indigo-300 hover:bg-indigo-200 dark:hover:bg-indigo-700 transition-colors"
            >
              Login
            </a>
            <a
              href="/register"
              class="inline-flex items-center px-3 py-2 rounded-md bg-indigo-100 dark:bg-indigo-800 text-indigo-700 dark:text-indigo-300 hover:bg-indigo-200 dark:hover:bg-indigo-700 transition-colors"
            >
              Register
            </a>
          </div>
        {/if}
      </div>
    {/if}
  </div>
</nav>
