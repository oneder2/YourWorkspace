<script lang="ts">
  import '../../app.css'; // 假设 app.css 在 src 目录下
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { isAuthenticated } from '$lib/store/authStore';

  import Navbar from '$lib/components/layout/Navbar.svelte';
  import ArrowNav from '$lib/components/layout/ArrowNav.svelte';

  let showContent = false;
  let isAnchorPage: boolean; // To pass to Navbar

  // Determine if the current page is the anchor page or one of its potential sub-routes
  $: isAnchorPage = $page.url.pathname.startsWith('/anchor');

  onMount(() => {
    const unsubscribe = isAuthenticated.subscribe(authenticated => {
      if (!authenticated) {
        // Only redirect if not already on a public auth page (though this layout shouldn't cover them)
        if ($page.route.id !== '/login' && $page.route.id !== '/register') {
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
        if ($page.route.id !== '/login' && $page.route.id !== '/register') {
          goto('/login');
        }
    }

    return () => {
      unsubscribe();
    };
  });

</script>

{#if showContent}
  <div class="app-layout">
    <Navbar {isAnchorPage} />

    <main class="app-main-content">
      {#if !isAnchorPage}
        <ArrowNav />
      {/if}
      
      <slot />
    </main>
  </div>
{:else}
  <div class="auth-check-loader">
    <p>Loading...</p>
  </div>
{/if}

<style>
  .app-layout {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: var(--light-color, #f8f9fa);
  }

  .app-main-content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    padding: 1rem;
  }

  .auth-check-loader {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-size: 1.5rem;
    color: var(--text-secondary, #6c757d);
  }
</style>
