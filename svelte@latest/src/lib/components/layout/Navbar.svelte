<script lang="ts">
  import { authService } from '$lib/services/authService';
  import { authStore, type UserProfile, isAuthenticated } from '$lib/store/authStore';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { get } from 'svelte/store';

  export let isAnchorPage: boolean = false; // New prop

  let currentUser: UserProfile | null = null;
  let lastWorkspacePage: string = '/doing'; 

  let previousPageBeforeAnchor: string | null = null;
  page.subscribe(currentPage => {
    const path = currentPage.url.pathname;
    if (!path.startsWith('/anchor') && (path.startsWith('/done') || path.startsWith('/doing') || path.startsWith('/plan'))) {
      previousPageBeforeAnchor = path;
    }
    if (path.startsWith('/anchor') && previousPageBeforeAnchor) {
        lastWorkspacePage = previousPageBeforeAnchor;
    } else if (path.startsWith('/anchor') && !previousPageBeforeAnchor) {
        lastWorkspacePage = '/doing'; 
    }
  });


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

<nav class="app-navbar" class:anchor-mode={isAnchorPage}>
  <div class="navbar-container">
    {#if isAnchorPage}
      <div class="navbar-brand">
         </div>
      <div class="navbar-main-links anchor-page-nav">
        <a href={lastWorkspacePage} class="nav-link back-to-workspace-link">
          <span class="icon" aria-hidden="true">⬅️</span>
          <span class="link-text">Back to Workspace</span>
        </a>
      </div>
      <div class="navbar-menu">
        {#if currentUser}
          <button 
            class="logout-button minimal-logout" 
            on:click={handleLogout} 
            title="Logout"
            aria-label="Logout" 
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="logout-icon"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
            </button>
        {/if}
      </div>
    {:else}
      <div class="navbar-brand">
        <a href="/doing" class="brand-link" aria-label="Go to Dashboard">
          <span class="brand-text">Personal Workspace</span>
        </a>
      </div>
      <div class="navbar-main-links">
        <a href="/anchor" class="nav-link anchor-link" class:active={$page.url.pathname.startsWith('/anchor')}>
          <span class="icon" aria-hidden="true">⚓️</span>
          <span class="link-text">My Anchor</span>
        </a>
      </div>
      <div class="navbar-menu">
        {#if currentUser}
          <div class="user-session">
            <span class="user-greeting" title={currentUser.email || ''}>
              Hello, {currentUser.username || currentUser.email?.split('@')[0]}
            </span>
            <button class="logout-button" on:click={handleLogout} title="Logout" aria-label="Logout">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="logout-icon"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
              <span class="logout-text">Logout</span>
            </button>
          </div>
        {:else}
          <div class="auth-links">
            <a href="/login" class="nav-link" class:active={$page.url.pathname === '/login'}>Login</a>
            <a href="/register" class="nav-link" class:active={$page.url.pathname === '/register'}>Register</a>
          </div>
        {/if}
      </div>
    {/if}
  </div>
</nav>

<style>
  .app-navbar {
    background-color: var(--navbar-bg, var(--primary-color, #007bff));
    color: var(--navbar-text-color, white);
    padding: 0.75rem 0;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
    transition: background-color 0.3s ease;
  }

  .app-navbar.anchor-mode {
    background-color: var(--anchor-navbar-bg, #f8f9fa); 
    box-shadow: var(--anchor-navbar-shadow, 0 1px 3px rgba(0,0,0,0.05));
  }
  .app-navbar.anchor-mode .nav-link,
  .app-navbar.anchor-mode .logout-button {
    color: var(--anchor-navbar-text-color, var(--text-primary, #212529));
    border-color: var(--anchor-navbar-border-color, #ced4da);
  }
  .app-navbar.anchor-mode .nav-link:hover,
  .app-navbar.anchor-mode .logout-button:hover {
    background-color: var(--anchor-navbar-hover-bg, #e9ecef);
    border-color: var(--anchor-navbar-hover-border-color, #adb5bd);
  }

  .navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  .navbar-brand .brand-link {
    display: flex;
    align-items: center;
    font-size: 1.4rem;
    font-weight: 600;
    color: var(--navbar-text-color, white); 
    text-decoration: none;
    transition: opacity 0.2s ease;
  }
  .app-navbar.anchor-mode .navbar-brand .brand-link {
    color: var(--anchor-navbar-text-color, var(--text-primary, #212529));
  }
  .navbar-brand .brand-link:hover {
    opacity: 0.85;
  }
  .brand-text {
    margin-left: 0.5rem;
  }

  .navbar-main-links {
    flex-grow: 1;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .navbar-main-links.anchor-page-nav { 
    justify-content: flex-start; 
    flex-grow: 0; 
    margin-right: auto; 
  }
  
  .nav-link {
    display: inline-flex;
    align-items: center;
    padding: 0.6rem 1rem;
    color: var(--navbar-link-color, white);
    text-decoration: none;
    border-radius: var(--border-radius-md, 0.375rem);
    transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
    font-size: 0.95rem;
    font-weight: 500;
  }

  .nav-link .icon {
    margin-right: 0.5em;
    font-size: 1.2em; 
  }
  
  .nav-link.anchor-link {
    padding: 0.7rem 1.2rem;
    background-color: var(--anchor-link-bg, rgba(255, 255, 255, 0.1));
    border: 1px solid var(--anchor-link-border, rgba(255, 255, 255, 0.3));
  }
  .nav-link.back-to-workspace-link { 
    padding: 0.7rem 1.2rem;
    background-color: var(--anchor-back-link-bg, transparent);
    border: 1px solid var(--anchor-back-link-border, #ced4da);
  }
  
  .nav-link.anchor-link:hover,
  .nav-link.anchor-link.active,
  .nav-link.back-to-workspace-link:hover {
    background-color: var(--anchor-link-hover-bg, rgba(255, 255, 255, 0.2));
    border-color: var(--anchor-link-hover-border, white);
  }
  .app-navbar.anchor-mode .nav-link.back-to-workspace-link:hover {
     background-color: var(--anchor-navbar-hover-bg, #e9ecef);
     border-color: var(--anchor-navbar-hover-border-color, #adb5bd);
  }
  
  .navbar-menu {
    display: flex;
    align-items: center;
  }

  .user-session {
    display: flex;
    align-items: center;
  }

  .user-greeting {
    margin-right: 1.25rem;
    font-size: 0.9rem;
    opacity: 0.9;
  }

  .logout-button {
    display: inline-flex;
    align-items: center;
    background-color: transparent;
    color: var(--navbar-text-color, white);
    border: 1px solid var(--navbar-border-color, rgba(255, 255, 255, 0.5));
    padding: 0.5rem 1rem;
    border-radius: var(--border-radius, 0.375rem);
    text-decoration: none;
    cursor: pointer;
    font-size: 0.875rem;
    margin-left: 0.75rem;
    transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
  }
  .logout-button.minimal-logout {
    padding: 0.5rem; 
    /* The .logout-text span is not rendered in this mode, so no CSS to hide it is needed */
  }
  /* REMOVED: .logout-button.minimal-logout .logout-text { display: none; } */


  .logout-button:hover {
    background-color: var(--navbar-hover-bg, rgba(255, 255, 255, 0.1));
    border-color: var(--navbar-hover-border-color, white);
  }
  
  .logout-icon {
    margin-right: 0.5em;
  }
  .logout-button.minimal-logout .logout-icon { /* Ensure icon is visible if text span was removed */
    margin-right: 0; 
  }
  
  @media (max-width: 768px) {
    .user-greeting {
      display: none;
    }
    .navbar-main-links .link-text { 
        display: none; 
    }
    .nav-link.anchor-link, .nav-link.back-to-workspace-link {
        padding: 0.7rem; 
    }
    .nav-link.anchor-link .icon, .nav-link.back-to-workspace-link .icon {
        margin-right: 0;
    }
    .brand-text {
        font-size: 1.2rem;
    }
    /* If the normal logout button's text should also hide on small screens: */
    /* .logout-button .logout-text { display: none; } */
    /* .logout-button .logout-icon { margin-right: 0; } */
    /* .logout-button { padding: 0.5rem; } */
  }
</style>
