<script lang="ts">
  import '../../app.css';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/state'; // Updated from $app/stores to $app/state
  import { isAuthenticated } from '$lib/store/authStore';

  import Navbar from '$lib/components/layout/Navbar.svelte';
  import ArrowNav from '$lib/components/layout/ArrowNav.svelte';
  import PageLoadingIndicator from '$lib/components/layout/PageLoadingIndicator.svelte';

  let showContent = false;
  let isAnchorPage: boolean; // To pass to Navbar

  // Determine if the current page is the anchor page or one of its potential sub-routes
  $: isAnchorPage = page.url.pathname.startsWith('/anchor');

  // Force re-render when the URL changes
  $: page.url.pathname;

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
    {#if !isAnchorPage}
      <ArrowNav />
      <Navbar {isAnchorPage} currentViewDisplay={page.url.pathname === '/done' ? 'Done' : page.url.pathname === '/doing' ? 'Doing' : page.url.pathname === '/plan' ? 'Plan' : 'N/A'} />
    {:else}
      <Navbar {isAnchorPage} />
    {/if}

    <main class="flex-grow flex flex-col p-4">

      <div>
        <slot />
      </div>
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
