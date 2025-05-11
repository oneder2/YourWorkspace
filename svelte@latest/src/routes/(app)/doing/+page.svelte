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

<div class="max-w-7xl mx-auto px-4 py-6 md:px-6">
  <header class="mb-10 text-center">
    <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-2">当前进行中 (Currently Doing)</h1>
    {#if currentUser}
      <p class="text-base text-gray-600 dark:text-gray-400">
        欢迎回来, {currentUser.username || currentUser.email?.split('@')[0]}！在这里管理您当前的任务和焦点。
      </p>
    {/if}
  </header>

  <section id="current-focus-section" class="mb-10 p-8 bg-warning-50 dark:bg-warning-900/20 border border-warning-200 dark:border-warning-800 rounded-xl shadow-lg">
    <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-6 pb-3 border-b border-gray-200 dark:border-gray-700">⭐ 当前焦点</h2>
    <CurrentFocusDisplay />
  </section>

  <section id="todo-section" class="mb-10 p-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg">
    <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-6 pb-3 border-b border-gray-200 dark:border-gray-700">活动中的任务 (Active Tasks)</h2>
    <div>
      <div class="mb-8">
        <TodoForm />
      </div>
      <div>
        <TodoList todos={$otherActiveTodos} listTitle="其他活动任务" />
      </div>
    </div>
  </section>
</div>
