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

<div class="max-w-7xl mx-auto px-4 py-4">
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <!-- Main Focus Section - Takes up 2/3 of the width on medium screens and up -->
    <div class="md:col-span-2">
      <section id="current-focus-section" class="mb-6 p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Main Focus:</h2>
        <CurrentFocusDisplay />
      </section>
    </div>

    <!-- Todo Section - Takes up 1/3 of the width on medium screens and up -->
    <div class="md:col-span-1">
      <section id="todo-section" class="mb-6 p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Todo</h2>
        <div>
          <div class="mb-4">
            <TodoForm />
          </div>
          <div>
            <TodoList todos={$otherActiveTodos} listTitle="Active Tasks" />
          </div>
          <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">PAST</h3>
            <!-- Past tasks could be added here -->
          </div>
        </div>
      </section>
    </div>
  </div>
</div>
