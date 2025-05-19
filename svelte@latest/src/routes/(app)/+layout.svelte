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
    const unsubscribe = isAuthenticated.subscribe(authenticated => {
      if (!authenticated) {
        // Only redirect if not already on a public auth page (though this layout shouldn't cover them)
        if (page.route.id !== '/login' && page.route.id !== '/register') {
          goto('/login');
        }
      } else {
        showContent = true;
      }
    });

    // Initial check
    let initialAuth = false;
    const tempUnsub = isAuthenticated.subscribe(val => initialAuth = val);
    tempUnsub();

    if (initialAuth) {
        showContent = true;
    } else {
        if (page.route.id !== '/login' && page.route.id !== '/register') {
          goto('/login');
        }
    }

    return () => {
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
    </div>
  </div>
{/if}
