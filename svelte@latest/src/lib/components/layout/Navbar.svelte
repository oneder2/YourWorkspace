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

<nav class={`sticky top-0 z-navbar transition-colors duration-300 ${isAnchorPage ? 'bg-gray-50 dark:bg-gray-800 shadow-sm' : 'bg-primary-500 dark:bg-primary-700 text-white shadow-md'}`}>
  <div class="flex justify-between items-center w-[90%] max-w-7xl mx-auto py-3 px-4">
    {#if isAnchorPage}
      <div class="flex-shrink-0">
        <!-- Empty div to maintain layout -->
      </div>
      <div class="flex-grow-0 mr-auto">
        <a
          href={lastWorkspacePage}
          class="inline-flex items-center px-4 py-2 rounded-md border border-gray-300 dark:border-gray-600 text-gray-800 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        >
          <span class="mr-2 text-lg" aria-hidden="true">⬅️</span>
          <span class="font-medium text-sm md:inline hidden">Back to Workspace</span>
        </a>
      </div>
      <div class="flex items-center">
        {#if currentUser}
          <button
            class="p-2 rounded-md border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            on:click={handleLogout}
            title="Logout"
            aria-label="Logout"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
          </button>
        {/if}
      </div>
    {:else}
      <div class="flex-shrink-0">
        <a href="/doing" class="flex items-center text-xl font-semibold text-white dark:text-white hover:opacity-85 transition-opacity" aria-label="Go to Dashboard">
          <span class="ml-2">Personal Workspace</span>
        </a>
      </div>
      <div class="flex-grow flex justify-center items-center">
        <a
          href="/anchor"
          class={`inline-flex items-center px-4 py-2 rounded-md bg-white/10 dark:bg-white/5 border border-white/30 dark:border-white/20 text-white font-medium text-sm transition-colors ${page.url.pathname.startsWith('/anchor') ? 'bg-white/20 dark:bg-white/10 border-white' : 'hover:bg-white/20 dark:hover:bg-white/10 hover:border-white'}`}
        >
          <span class="mr-2 text-lg" aria-hidden="true">⚓️</span>
          <span class="md:inline hidden">My Anchor</span>
        </a>
      </div>
      <div class="flex items-center">
        {#if currentUser}
          <div class="flex items-center">
            <span class="mr-5 text-sm opacity-90 hidden md:inline" title={currentUser.email || ''}>
              Hello, {currentUser.username || currentUser.email?.split('@')[0]}
            </span>
            <button
              class="inline-flex items-center px-3 py-2 rounded-md bg-transparent border border-white/50 dark:border-white/30 text-white text-sm hover:bg-white/10 dark:hover:bg-white/5 hover:border-white transition-colors"
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
              class={`inline-flex items-center px-3 py-2 rounded-md text-white text-sm transition-colors ${page.url.pathname === '/login' ? 'bg-white/20 dark:bg-white/10' : 'hover:bg-white/10 dark:hover:bg-white/5'}`}
            >
              Login
            </a>
            <a
              href="/register"
              class={`inline-flex items-center px-3 py-2 rounded-md text-white text-sm transition-colors ${page.url.pathname === '/register' ? 'bg-white/20 dark:bg-white/10' : 'hover:bg-white/10 dark:hover:bg-white/5'}`}
            >
              Register
            </a>
          </div>
        {/if}
      </div>
    {/if}
  </div>
</nav>
