<script lang="ts">
  import { authService } from '$lib/services/authService';
  import { authStore, type UserProfile, isAuthenticated } from '$lib/store/authStore';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';
  import { onMount } from 'svelte';
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
  let isDropdownOpen = $state(false);

  // Page thumbnails configuration
  const pageViews = [
    { path: '/done', display: 'Done', icon: '✓', description: 'View your completed tasks and achievements' },
    { path: '/doing', display: 'Doing', icon: '⚡', description: 'Manage your current tasks and focus' },
    { path: '/plan', display: 'Plan', icon: '📝', description: 'Plan your future tasks and projects' }
  ];

  // Toggle dropdown menu
  function toggleDropdown() {
    isDropdownOpen = !isDropdownOpen;
  }

  // Close dropdown when clicking outside
  function handleClickOutside(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (isDropdownOpen && !target.closest('.page-dropdown-container')) {
      isDropdownOpen = false;
    }
  }

  // Navigate to selected page
  function navigateTo(path: string) {
    isDropdownOpen = false;
    window.location.href = path;
  }

  // Subscribe to the auth store to get the current user
  authStore.subscribe(value => {
    currentUser = value.user;
  });

  // Set up click outside handler
  onMount(() => {
    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
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

<style>
  /* Fallback animation for browsers that don't support Tailwind's animate-dropdown */
  @keyframes dropdown {
    0% {
      opacity: 0;
      transform: translateY(-10px) translateX(-50%);
    }
    100% {
      opacity: 1;
      transform: translateY(0) translateX(-50%);
    }
  }

  .animate-dropdown {
    animation: dropdown 0.3s ease-out forwards;
  }
</style>

<nav class="sticky top-0 z-navbar bg-indigo-50 dark:bg-indigo-900 border-b border-indigo-200 dark:border-indigo-700 shadow-sm">
  <div class="flex justify-between items-center w-full px-4 py-3">
    <!-- Main workspace navigation - always shown -->
    <div class="flex-shrink-0">
      <a href="/doing" class="flex items-center text-2xl font-bold text-indigo-900 dark:text-indigo-100 hover:opacity-85 transition-opacity" aria-label="Go to Dashboard">
        Personal Workspace
      </a>
    </div>

    <!-- Current page display in center with enhanced styling and dropdown -->
    <div class="flex-grow flex justify-center items-center">
      <div class="page-dropdown-container relative">
        {#if isAnchorPage}
          <div class="px-6 py-2 min-w-[180px] text-center text-3xl font-extrabold text-indigo-900 dark:text-indigo-100 tracking-wide relative group">
            <span class="relative z-10">My Anchor</span>
            <span class="absolute inset-0 bg-indigo-200 dark:bg-indigo-800 rounded-lg transform scale-95 opacity-20 group-hover:scale-100 group-hover:opacity-30 transition-all duration-300"></span>
          </div>
        {:else}
          <!-- Clickable current page display that toggles dropdown -->
          <button
            type="button"
            class="px-6 py-2 min-w-[180px] text-center text-3xl font-extrabold text-indigo-900 dark:text-indigo-100 tracking-wide relative group cursor-pointer bg-transparent border-0"
            onclick={toggleDropdown}
            aria-haspopup="true"
            aria-expanded={isDropdownOpen}
          >
            <span class="relative z-10 flex items-center justify-center">
              {currentViewDisplay}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 ml-2 transform transition-transform duration-300 {isDropdownOpen ? 'rotate-180' : ''}"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </span>
            <span class="absolute inset-0 bg-indigo-200 dark:bg-indigo-800 rounded-lg transform scale-95 opacity-20 group-hover:scale-100 group-hover:opacity-30 transition-all duration-300"></span>
          </button>

          <!-- Dropdown menu with page thumbnails -->
          {#if isDropdownOpen}
            <div class="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 w-[600px] bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50 overflow-hidden animate-dropdown">
              <div class="flex p-4 justify-around">
                {#each pageViews as page}
                  <button
                    type="button"
                    class="flex flex-col items-center p-3 rounded-lg hover:bg-indigo-50 dark:hover:bg-indigo-900/30 transition-colors cursor-pointer {page.path === window.location.pathname ? 'bg-indigo-100 dark:bg-indigo-800/50' : ''} bg-transparent border-0 w-full"
                    onclick={() => navigateTo(page.path)}
                    aria-label="Navigate to {page.display} page"
                  >
                    <!-- Page thumbnail/icon -->
                    <div class="w-32 h-24 mb-2 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center text-4xl shadow-inner overflow-hidden relative">
                      <div class="absolute inset-0 bg-gradient-to-br from-transparent to-gray-200 dark:to-gray-600 opacity-50"></div>
                      <span class="relative z-10 transform transition-transform duration-300 group-hover:scale-110">{page.icon}</span>
                    </div>
                    <!-- Page name -->
                    <div class="font-bold text-indigo-900 dark:text-indigo-100">
                      {page.display}
                    </div>
                    <!-- Page description -->
                    <div class="text-xs text-gray-600 dark:text-gray-400 text-center mt-1 max-w-[150px]">
                      {page.description}
                    </div>
                  </button>
                {/each}
              </div>
            </div>
          {/if}
        {/if}
      </div>
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
