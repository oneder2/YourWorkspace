<script lang="ts">
    import { authStore, type UserProfile } from '$lib/store/authStore';
    import { onMount } from 'svelte';
  
    let currentUser: UserProfile | null = null;
  
    onMount(() => {
      const unsubscribe = authStore.subscribe(value => {
        currentUser = value.user;
      });
      return unsubscribe;
    });
  </script>
  
  <div class="doing-page-container">
    <h1>Currently Doing</h1>
    <p>This is your main workspace for ongoing tasks and focus items.</p>
  
    {#if currentUser}
      <p>Welcome, {currentUser.username || currentUser.email}!</p>
    {/if}
  
    <section class="focus-section">
      <h2>Current Focus</h2>
      <p><em>Current focus items will be displayed here.</em></p>
    </section>
  
    <section class="todo-section">
      <h2>Smart To-Do List</h2>
      <p><em>Your active to-do items will be displayed here.</em></p>
    </section>
  </div>
  
  <style>
    .doing-page-container {
      padding: 1rem;
      /* Add any specific styles for the "doing" page */
    }
  
    .doing-page-container h1 {
      color: var(--text-primary, #212529);
      margin-bottom: 1rem;
    }
  
    .focus-section, .todo-section {
      margin-top: 2rem;
      padding: 1.5rem;
      background-color: #ffffff;
      border-radius: var(--border-radius, 0.375rem);
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
  
    .focus-section h2, .todo-section h2 {
      color: var(--text-primary, #333);
      margin-bottom: 1rem;
      font-size: 1.5rem; /* h2 size from global.css */
    }
  </style>
  