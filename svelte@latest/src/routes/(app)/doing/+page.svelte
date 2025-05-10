<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { authStore, type UserProfile } from '$lib/store/authStore';
  // Import main store and specific derived stores
  import { todoStore, otherActiveTodos, completedTodos } from '$lib/store/todoStore';

  import TodoForm from '$lib/components/todo/TodoForm.svelte';
  import TodoList from '$lib/components/todo/TodoList.svelte';

  import CurrentFocusDisplay from '$lib/components/anchor/current_focus/CurrentFocusDisplay.svelte';

  let currentUser: UserProfile | null = null;
  let authUnsubscribe: () => void;

  onMount(async () => {
    authUnsubscribe = authStore.subscribe(value => {
      currentUser = value.user;
    });

    // Access main store state for the condition
    if ($todoStore.todos.length === 0 && !$todoStore.isLoading && !$todoStore.error) {
      await todoStore.loadAllTodos();
    }
  });

  onDestroy(() => {
    if (authUnsubscribe) {
      authUnsubscribe();
    }
  });
</script>

<div class="doing-page-container">
  <header class="page-header">
    <h1>当前进行中 (Currently Doing)</h1>
    {#if currentUser}
      <p class="welcome-message">
        欢迎回来, {currentUser.username || currentUser.email?.split('@')[0]}！在这里管理您当前的任务和焦点。
      </p>
    {/if}
  </header>

  <section id="current-focus-section" class="app-section current-focus-module">
    <h2 class="section-title">⭐ 当前焦点</h2>
    <CurrentFocusDisplay /> 
  </section>

  <section id="todo-section" class="app-section todo-module">
    <h2 class="section-title">活动中的任务 (Active Tasks)</h2>
    <div class="todo-content">
      <div class="todo-form-wrapper">
        <TodoForm />
      </div>
      <div class="todo-list-wrapper">
        <TodoList todos={$otherActiveTodos} listTitle="其他活动任务" />
      </div>
    </div>
  </section>

  </div>

<style>
  /* Styles remain the same */
  .doing-page-container {
    padding: 1rem 1.5rem;
    max-width: 1100px;
    margin: 0 auto;
  }
  .page-header { margin-bottom: 2.5rem; text-align: center; }
  .page-header h1 { font-size: 2.25rem; color: var(--text-primary, #212529); margin-bottom: 0.5rem; }
  .welcome-message { font-size: 1rem; color: var(--text-secondary, #6c757d); }
  .app-section { margin-bottom: 2.5rem; padding: 2rem; background-color: var(--section-bg, #fff); border-radius: var(--border-radius-xl, 0.75rem); box-shadow: var(--shadow-lg, 0 8px 16px rgba(0,0,0,0.07)); }
  .current-focus-module { background-color: var(--focus-section-bg, #fffbeb); border: 1px solid var(--focus-indicator-color, #ffeeba); }
  .section-title { font-size: 1.6rem; color: var(--text-heading, #1a202c); margin-bottom: 1.5rem; padding-bottom: 0.75rem; border-bottom: 1px solid var(--border-color-light, #e0e0e0); text-align: left; }
  .todo-form-wrapper { margin-bottom: 2rem; }
</style>
