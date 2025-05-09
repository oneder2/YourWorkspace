<script lang="ts">
    import { authService } from '$lib/services/authService';
    import { authStore, type UserProfile } from '$lib/store/authStore';
    import { goto } from '$app/navigation';
  
    let currentUser: UserProfile | null = null;
  
    authStore.subscribe(value => {
      currentUser = value.user;
    });
  
    async function handleLogout() {
      try {
        await authService.logoutUser();
        // authStore.logout() will clear the store,
        // and the layout guard should redirect to /login.
        // If not, explicitly redirect:
        // await goto('/login');
      } catch (error) {
        console.error('Failed to logout from navbar:', error);
        // Still attempt to clear client-side store as a fallback
        authStore.logout();
        await goto('/login'); // Ensure redirection even if server logout fails
      }
    }
  </script>
  
  <nav class="app-navbar">
    <div class="navbar-brand">
      <a href="/doing" class="brand-link">Personal Workspace</a>
    </div>
    <div class="navbar-menu">
      {#if currentUser}
        <span class="user-greeting">Hello, {currentUser.username || currentUser.email}</span>
        <button class="logout-button" on:click={handleLogout}>Logout</button>
      {:else}
        <a href="/login" class="nav-link">Login</a>
        <a href="/register" class="nav-link">Register</a>
      {/if}
    </div>
  </nav>
  
  <style>
    .app-navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.75rem 1.5rem;
      background-color: var(--primary-color, #007bff);
      color: white;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
  
    .navbar-brand .brand-link {
      font-size: 1.5rem;
      font-weight: 600;
      color: white;
      text-decoration: none;
    }
  
    .navbar-menu {
      display: flex;
      align-items: center;
    }
  
    .user-greeting {
      margin-right: 1rem;
      font-size: 0.9rem;
    }
  
    .logout-button, .nav-link {
      background-color: transparent;
      color: white;
      border: 1px solid white;
      padding: 0.5rem 1rem;
      border-radius: var(--border-radius, 0.375rem);
      text-decoration: none;
      cursor: pointer;
      font-size: 0.9rem;
      margin-left: 0.75rem;
      transition: background-color 0.2s ease, color 0.2s ease;
    }
  
    .logout-button:hover, .nav-link:hover {
      background-color: white;
      color: var(--primary-color, #007bff);
    }
  </style>
  