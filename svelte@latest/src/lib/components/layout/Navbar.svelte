<script lang="ts">
  import { authService } from '$lib/services/authService';
  import { authStore, type UserProfile, isAuthenticated } from '$lib/store/authStore';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';
  import { ThemeToggle, BackgroundUploader } from '$lib/components/ui';

  export let isAnchorPage: boolean = false; // New prop

  let currentUser: UserProfile | null = null;
  let lastWorkspacePage = '/doing';

  // Subscribe to the auth store to get the current user
  authStore.subscribe(value => {
    currentUser = value.user;
  });

  // Update lastWorkspacePage when isAnchorPage changes
  $: {
    try {
      if (!isAnchorPage) {
        // 我们不在 anchor 页面上，存储当前页面
        const currentPath = window.location.pathname;
        if (currentPath !== '/anchor') {
          // 确保路径是有效的工作区页面
          if (currentPath === '/doing' || currentPath === '/done' || currentPath === '/plan') {
            lastWorkspacePage = currentPath;
            sessionStorage.setItem('lastWorkspacePage', lastWorkspacePage);
            console.log('Stored lastWorkspacePage:', lastWorkspacePage);
          } else {
            // 如果不是有效的工作区页面，使用默认值
            lastWorkspacePage = '/doing';
          }
        }
      } else {
        // 我们在 anchor 页面上，获取上次的工作区页面
        const storedLastWorkspacePage = sessionStorage.getItem('lastWorkspacePage');
        if (storedLastWorkspacePage) {
          lastWorkspacePage = storedLastWorkspacePage;
          console.log('Retrieved lastWorkspacePage:', lastWorkspacePage);
        } else {
          // 如果没有存储的页面，使用默认值
          lastWorkspacePage = '/doing';
          console.log('No stored lastWorkspacePage, using default:', lastWorkspacePage);
        }
      }
    } catch (error) {
      console.error('Error updating lastWorkspacePage:', error);
      // 出错时使用默认值
      lastWorkspacePage = '/doing';
    }
  }

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
    <div class="flex-grow flex justify-center items-center">
      {#if isAnchorPage}
        <!-- Back button when on Anchor page -->
        <a
          href={lastWorkspacePage}
          id="anchor-button"
          class="inline-flex items-center px-4 py-2 rounded-md bg-indigo-100 dark:bg-indigo-800 border border-indigo-300 dark:border-indigo-600 text-indigo-800 dark:text-indigo-200 hover:bg-indigo-200 dark:hover:bg-indigo-700 transition-colors"
        >
          <span class="mr-2 text-lg" aria-hidden="true">⬅️</span>
          <span class="font-medium">Back</span>
        </a>
      {:else}
        <!-- Anchor button when not on Anchor page -->
        <a
          href="/anchor"
          id="anchor-button"
          class="inline-flex items-center px-4 py-2 rounded-md bg-amber-100 dark:bg-amber-800 border border-amber-300 dark:border-amber-600 text-amber-800 dark:text-amber-200 hover:bg-amber-200 dark:hover:bg-amber-700 transition-colors"
        >
          <span class="mr-2 text-lg" aria-hidden="true">⚓️</span>
          <span class="font-medium">My Anchor</span>
        </a>
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
