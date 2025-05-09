<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores'; // To check current path and avoid redirect loops if on login
    import { isAuthenticated } from '$lib/store/authStore';
  
    // Import placeholder/actual components for the app shell
    // We will create these components in subsequent steps.
    import Navbar from '$lib/components/layout/Navbar.svelte';
    import ArrowNav from '$lib/components/layout/ArrowNav.svelte';
    // import PageTransition from '$lib/components/layout/PageTransition.svelte'; // As per phase1frame.txt
  
    let showContent = false; // Controls rendering of the slot to prevent flash of content before redirect
  
    onMount(() => {
      const unsubscribe = isAuthenticated.subscribe(authenticated => {
        // Check if current page is part of the auth flow to prevent redirect loops
        // Although, being inside (app) group, this layout shouldn't apply to /login or /register
        if (!authenticated) {
          if ($page.route.id !== '/login' && $page.route.id !== '/register') {
            goto('/login');
          }
        } else {
          showContent = true; // User is authenticated, show content
        }
      });
  
      // Initial check in case the store is already set (e.g. from localStorage)
      // and the subscription might fire too late for the very first paint.
      if (getIsAuthenticated()) { // Helper to get current value, or use derived store logic
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
  
    // Helper function to get the current value of a readable store
    // Svelte's `get` utility is usually imported: import { get } from 'svelte/store'
    // but for this specific onMount, a direct subscription check is often done.
    // Let's assume `get` is available or simplify.
    function getIsAuthenticated(): boolean {
      let authenticated = false;
      const unsub = isAuthenticated.subscribe(value => authenticated = value);
      unsub(); // Immediately unsubscribe after getting the value
      return authenticated;
    }
  
  </script>
  
  {#if showContent}
    <div class="app-layout">
      <Navbar />
  
      <main class="app-main-content">
        <ArrowNav />
        
        <slot />
        </main>
  
      </div>
  {:else}
    <div class="auth-check-loader">
      <p>Loading...</p> </div>
  {/if}
  
  <style>
    .app-layout {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      background-color: var(--light-color, #f8f9fa); /* Consistent background */
    }
  
    .app-main-content {
      flex-grow: 1; /* Allows main content to take up available space */
      display: flex;
      flex-direction: column; /* Ensures ArrowNav and slot stack vertically */
      padding: 1rem; /* Add some padding around the content area */
      /* max-width: 1200px; /* Optional: constrain width of main content */
      /* margin: 0 auto; /* Center if max-width is set */
    }
  
    /* Basic styling for the loader, can be improved with a real spinner */
    .auth-check-loader {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      font-size: 1.5rem;
      color: var(--text-secondary, #6c757d);
    }
  
    /* Ensure global styles are applied if not already via app.html or root layout */
    /* @import '../../static/global.css'; */ /* Path might need adjustment */
    /* It's better to import global.css in the root +layout.svelte or app.html */
  </style>
  