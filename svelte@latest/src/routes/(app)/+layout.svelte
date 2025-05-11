<script lang="ts">
  import '../../app.css';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/state'; // Updated from $app/stores to $app/state
  import { isAuthenticated } from '$lib/store/authStore';

  import Navbar from '$lib/components/layout/Navbar.svelte';
  import ArrowNav from '$lib/components/layout/ArrowNav.svelte';

  let showContent = false;
  let isAnchorPage: boolean; // To pass to Navbar

  // Determine if the current page is the anchor page or one of its potential sub-routes
  $: isAnchorPage = page.url.pathname.startsWith('/anchor');

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

{#if showContent}
  <div class="flex flex-col min-h-screen bg-light dark:bg-gray-900">
    <Navbar {isAnchorPage} />

    <main class="flex-grow flex flex-col p-4">
      {#if !isAnchorPage}
        <ArrowNav />
      {/if}

      <slot />
    </main>
  </div>
{:else}
  <div class="flex justify-center items-center min-h-screen text-2xl text-secondary-500 dark:text-secondary-400">
    <p>Loading...</p>
  </div>
{/if}
