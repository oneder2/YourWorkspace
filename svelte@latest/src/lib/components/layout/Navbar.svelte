<script lang="ts">
  import { authService } from '$lib/services/authService';
  import { authStore, type UserProfile, isAuthenticated } from '$lib/store/authStore';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';
  import { ThemeToggle, BackgroundUploader } from '$lib/components/ui';

  // Props using $props rune for Svelte 5
  let {
    isAnchorPage = false,
    currentViewDisplay = 'N/A'
  } = $props<{
    isAnchorPage?: boolean;
    currentViewDisplay?: string;
  }>();

  let currentUser = $state<UserProfile | null>(null);
  let lastWorkspacePage = $state('/doing');

  // Subscribe to the auth store to get the current user
  authStore.subscribe(value => {
    currentUser = value.user;
  });

  // Update lastWorkspacePage when isAnchorPage changes
  $effect(() => {
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
  });

  async function handleLogout() {
    try {
      console.log('Navbar: Starting logout process');
      await authService.logoutUser();
      console.log('Navbar: Logout successful');

      // 确保重定向到登录页面
      try {
        await goto('/login');
      } catch (gotoError) {
        console.error('Navbar: Error redirecting after logout:', gotoError);
        // 如果 goto 失败，使用直接导航
        window.location.href = '/login';
      }
    } catch (error) {
      console.error('Navbar: Failed to logout:', error);

      // 确保用户在前端被登出
      if (get(isAuthenticated)) {
        console.log('Navbar: Forcing client-side logout');
        authStore.logout();
      }

      // 确保重定向到登录页面
      try {
        await goto('/login');
      } catch (gotoError) {
        console.error('Navbar: Error redirecting after failed logout:', gotoError);
        // 如果 goto 失败，使用直接导航
        window.location.href = '/login';
      }
    }
  }

</script>

<nav class="sticky top-0 z-navbar bg-indigo-50 dark:bg-indigo-900 border-b border-indigo-200 dark:border-indigo-700 shadow-sm">
  <div class="flex justify-between items-center w-full px-4 py-3">
    <!-- Main workspace navigation - always shown -->
    <div class="flex-shrink-0">
      <a href="/doing" class="flex items-center text-2xl font-bold text-indigo-900 dark:text-indigo-100 hover:opacity-85 transition-opacity" aria-label="Go to Dashboard">
        Personal Workspace
      </a>
    </div>

    <!-- Current page display in center -->
    <div class="flex-grow flex justify-center items-center">
      {#if isAnchorPage}
        <div class="px-6 py-2 min-w-[120px] text-center text-2xl font-bold text-indigo-900 dark:text-indigo-100">
          My Anchor
        </div>
      {:else}
        <div class="px-6 py-2 min-w-[120px] text-center text-2xl font-bold text-indigo-900 dark:text-indigo-100">
          {currentViewDisplay}
        </div>
      {/if}
    </div>

    <div class="flex items-center">
      <!-- Theme Toggle Button -->
      <div class="mr-3">
        <ThemeToggle size="sm" />
      </div>

      <!-- Background Uploader -->
      <div class="mr-4">
        <BackgroundUploader />
      </div>

      {#if currentUser}
        <div class="flex items-center">
          <span class="mr-3 text-base font-medium text-indigo-700 dark:text-indigo-300" title={currentUser.email || ''}>
            Hello, {currentUser.username || currentUser.email?.split('@')[0]}!
          </span>
          <button
            class="inline-flex items-center px-3 py-2 rounded-md bg-indigo-100 dark:bg-indigo-800 border border-indigo-300 dark:border-indigo-600 text-indigo-700 dark:text-indigo-300 hover:bg-indigo-200 dark:hover:bg-indigo-700 transition-colors"
            onclick={handleLogout}
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
  </div>
</nav>
