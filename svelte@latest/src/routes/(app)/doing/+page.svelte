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

  // State to toggle between active and completed tasks
  let showCompletedTasks = false;

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

<div class="max-w-7xl mx-auto px-4 py-4">
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <!-- Main Focus Section - Takes up 2/3 of the width on medium screens and up -->
    <div class="md:col-span-2">
      <section id="current-focus-section" class="mb-6 p-6 bg-amber-50 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-800 rounded-lg shadow">
        <h2 class="text-xl font-semibold text-amber-900 dark:text-amber-100 mb-4 flex items-center">
          <span class="text-yellow-500 mr-2">⭐</span>
          Main Focus:
        </h2>
        <CurrentFocusDisplay />
      </section>
    </div>

    <!-- Todo Section - Takes up 1/3 of the width on medium screens and up -->
    <div class="md:col-span-1">
      <section id="todo-section" class="mb-6 p-6 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 rounded-lg shadow">
        <h2 class="text-xl font-semibold text-blue-900 dark:text-blue-100 mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-600 dark:text-blue-400" viewBox="0 0 20 20" fill="currentColor">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
          </svg>
          Todo
        </h2>
        <div>
          <div class="mb-4">
            <TodoForm />
          </div>
          <div>
            {#if !showCompletedTasks}
              <TodoList todos={$otherActiveTodos} listTitle="Active Tasks" />
            {:else}
              <TodoList todos={$completedTodos} listTitle="Completed Tasks" />
            {/if}
          </div>
          <div class="mt-4 pt-4 border-t border-blue-200 dark:border-blue-700">
            <button
              class="flex items-center justify-between w-full text-left p-2 rounded-md hover:bg-blue-100 dark:hover:bg-blue-800/50 transition-colors"
              on:click={() => showCompletedTasks = !showCompletedTasks}
            >
              <h3 class="text-lg font-medium text-blue-800 dark:text-blue-200">
                {showCompletedTasks ? "ACTIVE" : "PAST"}
              </h3>
              <span class="text-sm text-blue-600 dark:text-blue-400">
                {showCompletedTasks ? "Show active tasks" : "Show completed tasks"}
              </span>
            </button>
          </div>
        </div>
      </section>
    </div>
  </div>
</div>
