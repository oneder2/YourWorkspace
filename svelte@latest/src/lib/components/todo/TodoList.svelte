<script lang="ts">
    import { onMount } from 'svelte';
    import { todoStore } from '$lib/store/todoStore';
    // Corrected import for TodoItem type from todoService.ts
    import type { TodoItem } from '$lib/services/todoService';
    import TodoItemComponent from './TodoItem.svelte'; // We'll create this next
  
    onMount(async () => {
      if ($todoStore.todos.length === 0 && !$todoStore.isLoading && !$todoStore.error) {
        await todoStore.fetchAllTodos();
      }
    });
  </script>
  
  <div class="todo-list-container">
    <h3 class="list-title">Your To-Do Items</h3>
  
    {#if $todoStore.isLoading && $todoStore.todos.length === 0}
      <div class="message loading-message">
        <p>Loading your to-dos...</p>
      </div>
    {:else if $todoStore.error}
      <div class="message error-message">
        <p>Error loading to-dos: {$todoStore.error}</p>
        <button on:click={() => todoStore.fetchAllTodos()} class="retry-button">Try Again</button>
      </div>
    {:else if $todoStore.todos.length === 0}
      <div class="message empty-list-message">
        <p>No to-do items yet. Add one using the form above!</p>
      </div>
    {:else}
      <ul class="todo-list">
        {#each $todoStore.todos as todo (todo.id)}
          <li class="todo-list-item-wrapper">
            <TodoItemComponent {todo} />
          </li>
        {/each}
      </ul>
    {/if}
  </div>
  
  <style>
    .todo-list-container {
      background-color: var(--list-bg, #f9f9f9);
      padding: 1.5rem 2rem;
      border-radius: var(--border-radius-lg, 0.5rem);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
      margin-top: 2rem;
      max-width: 700px;
      margin-left: auto;
      margin-right: auto;
    }
  
    .list-title {
      font-size: 1.5rem;
      font-weight: 600;
      color: var(--text-primary, #212529);
      margin-bottom: 1.5rem;
      text-align: center;
      border-bottom: 1px solid var(--border-color-light, #e0e0e0);
      padding-bottom: 0.75rem;
    }
  
    .message {
      padding: 1rem 1.5rem;
      border-radius: var(--border-radius, 0.375rem);
      margin: 1rem 0;
      text-align: center;
      font-size: 1rem;
    }
    .message p {
      margin: 0 0 0.5rem 0;
    }
  
    .loading-message {
      background-color: var(--info-bg-light, rgba(23, 162, 184, 0.1));
      color: var(--info-color, #17a2b8);
      border: 1px solid var(--info-border-light, rgba(23, 162, 184, 0.2));
    }
  
    .error-message {
      background-color: var(--danger-bg-light, rgba(220, 53, 69, 0.1));
      color: var(--danger-color, #dc3545);
      border: 1px solid var(--danger-border-light, rgba(220, 53, 69, 0.2));
    }
  
    .empty-list-message {
      background-color: var(--secondary-bg-light, rgba(108, 117, 125, 0.05));
      color: var(--text-secondary, #6c757d);
      border: 1px solid var(--secondary-border-light, rgba(108, 117, 125, 0.1));
    }
    
    .retry-button {
      padding: 0.5rem 1rem;
      font-size: 0.9rem;
      color: #fff;
      background-color: var(--primary-color, #007bff);
      border: none;
      border-radius: var(--border-radius, 0.375rem);
      cursor: pointer;
      transition: background-color 0.2s ease-in-out;
      margin-top: 0.5rem;
    }
  
    .retry-button:hover {
      background-color: #0056b3;
    }
  
    .todo-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }
  
    .todo-list-item-wrapper {
      margin-bottom: 0.75rem;
    }
  
    .todo-list-item-wrapper:last-child {
      margin-bottom: 0;
    }
  </style>
  