<script lang="ts">
  import '../../app.css';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/state'; // Updated from $app/stores to $app/state
  import { isAuthenticated } from '$lib/store/authStore';

  import Navbar from '$lib/components/layout/Navbar.svelte';
  import ArrowNav from '$lib/components/layout/ArrowNav.svelte';
  import AnchorButton from '$lib/components/layout/AnchorButton.svelte';
  import PageLoadingIndicator from '$lib/components/layout/PageLoadingIndicator.svelte';

  let { children } = $props<{ children?: any }>();

  let showContent = $state(false);
  let isAnchorPage = $state(false);
  let currentViewDisplay = $state('N/A');

  // Determine if the current page is the anchor page or one of its potential sub-routes
  $effect(() => {
    isAnchorPage = page.url.pathname.startsWith('/anchor');
  });

  // Force re-render when the URL changes
  $effect(() => {
    // This will re-run when page.url.pathname changes
    const path = page.url.pathname;
    console.log('Current path changed:', path);
  });

  onMount(() => {
    console.log('(app)/+layout.svelte: onMount called');

    // 简化认证状态检查逻辑
    const unsubscribe = isAuthenticated.subscribe(authenticated => {
      console.log('(app)/+layout.svelte: Authentication state changed:', authenticated);

      // 添加延迟，确保认证状态已经稳定
      setTimeout(() => {
        console.log('(app)/+layout.svelte: Setting showContent to:', authenticated);
        showContent = authenticated; // 直接根据认证状态设置显示内容

        if (!authenticated) {
          // 如果未认证，重定向到登录页面
          console.log('(app)/+layout.svelte: User not authenticated, redirecting to login');
          goto('/login');
        } else {
          console.log('(app)/+layout.svelte: User is authenticated, showing content');
        }
      }, 500);
    });

    return () => {
      console.log('(app)/+layout.svelte: Unsubscribing from isAuthenticated');
      unsubscribe();
    };
  });

</script>

<!-- Page loading indicator -->
<PageLoadingIndicator />

{#if showContent}
  <div class="flex flex-col min-h-screen dark:bg-transparent">
    <Navbar {isAnchorPage} {currentViewDisplay} />

    <main class="flex-grow flex flex-col p-4">
      {#if !isAnchorPage}
        <ArrowNav bind:currentViewDisplay />
      {/if}

      <div>
        {children}
      </div>

      <!-- Anchor Button (fixed position) -->
      <AnchorButton {isAnchorPage} />
    </main>
  </div>
{:else}
  <div class="flex justify-center items-center min-h-screen text-2xl text-secondary-500 dark:text-secondary-400">
    <div class="flex flex-col items-center">
      <div class="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mb-4"></div>
      <p>Loading...</p>

      <!-- 调试按钮 - 仅在开发环境中显示 -->
      {#if import.meta.env.DEV}
        <div class="mt-8 p-4 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
          <h3 class="text-lg font-semibold mb-2">Debug Controls</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">页面卡在加载状态，可能是认证问题导致的。</p>
          <div class="flex space-x-2">
            <button
              class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md text-sm"
              onclick={() => {
                // 手动设置认证状态为 true
                showContent = true;
                console.log('手动设置 showContent = true');
              }}
            >
              强制显示内容
            </button>
            <button
              class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-md text-sm"
              onclick={() => {
                // 重定向到登录页面
                window.location.href = '/login';
              }}
            >
              返回登录页面
            </button>
          </div>
        </div>
      {/if}
    </div>
  </div>
{/if}
