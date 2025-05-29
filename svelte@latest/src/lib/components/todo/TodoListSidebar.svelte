<script lang="ts">
  import { onMount } from 'svelte';
  import { todoStore } from '$lib/store/todoStore'; // Store for loading state and errors
  import type { TodoItem } from '$lib/services/todoService';

  import TodoAddModal from './TodoAddModal.svelte';
  import TodoEditModal from './TodoEditModal.svelte';

  // State for showing/hiding the add modal
  let isAddModalOpen = $state(false);

  // State for editing
  let editingTodo: TodoItem | null = $state(null);
  let isEditModalOpen = $state(false);

  // Functions to handle todo actions
  async function handleToggleStatus(todo: TodoItem) {
    try {
      await todoStore.toggleCompleteStatus(todo.id, todo.status);
    } catch (error) {
      console.error('Failed to toggle todo status:', error);
    }
  }

  function handleEdit(todo: TodoItem) {
    editingTodo = { ...todo };
    isEditModalOpen = true;
  }

  function handleEditSave(updatedTodo: TodoItem) {
    // This will be called when the edit is successful
    console.log('Edit successful for todo:', updatedTodo.title);
    isEditModalOpen = false;
    editingTodo = null;
  }

  function handleEditCancel() {
    isEditModalOpen = false;
    editingTodo = null;
  }

  async function handleDelete(todo: TodoItem) {
    if (confirm(`Are you sure you want to delete "${todo.title}"?`)) {
      try {
        await todoStore.removeTodo(todo.id);
      } catch (error) {
        console.error('Failed to delete todo:', error);
      }
    }
  }

  function toggleAddForm() {
    isAddModalOpen = true;
  }

  function handleAddSuccess() {
    isAddModalOpen = false;
  }

  function handleAddCancel() {
    isAddModalOpen = false;
  }

  // State for loading operations
  let loadingFocusToggle = $state<Set<number>>(new Set());

  async function handleSetAsFocus(todo: TodoItem) {
    if (todo.is_current_focus) {
      if (confirm(`Remove "${todo.title}" from Main Focus?`)) {
        loadingFocusToggle.add(todo.id);
        loadingFocusToggle = new Set(loadingFocusToggle);
        try {
          await todoStore.toggleCurrentFocus(todo.id);
        } finally {
          loadingFocusToggle.delete(todo.id);
          loadingFocusToggle = new Set(loadingFocusToggle);
        }
      }
    } else {
      loadingFocusToggle.add(todo.id);
      loadingFocusToggle = new Set(loadingFocusToggle);
      try {
        await todoStore.toggleCurrentFocus(todo.id);
      } finally {
        loadingFocusToggle.delete(todo.id);
        loadingFocusToggle = new Set(loadingFocusToggle);
      }
    }
  }

  // Props using $props rune
  let {
    todos = [],
    listTitle = "",
    addButtonId = "add-todo-button"
  } = $props<{
    todos: TodoItem[];
    listTitle?: string;
    addButtonId?: string;
  }>();

  // Expose the toggleAddForm function to parent components
  export function triggerAddForm() {
    toggleAddForm();
  }

  onMount(() => {
    // Set up a global function that can be called by parent components
    // This is a more reliable way than DOM event listeners
    if (typeof window !== 'undefined') {
      (window as any)[`toggleAddForm_${addButtonId}`] = toggleAddForm;
    }

    return () => {
      // Clean up global function
      if (typeof window !== 'undefined') {
        delete (window as any)[`toggleAddForm_${addButtonId}`];
      }
    };
  });
</script>

<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm py-2">
  <TodoAddModal
    isOpen={isAddModalOpen}
    onAddSuccess={handleAddSuccess}
    onCloseRequest={handleAddCancel}
  />

  {#if editingTodo}
    <TodoEditModal
      todo={editingTodo}
      isOpen={isEditModalOpen}
      onSaveSuccess={handleEditSave}
      onCloseRequest={handleEditCancel}
    />
  {/if}

  {#if $todoStore.isLoading && todos.length === 0 && $todoStore.todos.length === 0}
    <div class="p-3 rounded-md bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800 mx-2 my-2 text-center text-sm">
      <p>Loading tasks...</p>
    </div>
  {:else if $todoStore.error && todos.length === 0 && $todoStore.todos.length === 0}
    <div class="p-3 rounded-md bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800 mx-2 my-2 text-center text-sm">
      <p class="mb-1">Failed to load tasks: {$todoStore.error}</p>
      <button
        onclick={() => todoStore.loadAllTodos()}
        class="px-3 py-1 text-xs font-medium text-white bg-primary-500 hover:bg-primary-600 rounded-md transition-colors"
      >
        Retry
      </button>
    </div>
  {:else if todos.length === 0}
    <div class="p-4 rounded-md bg-gray-50 dark:bg-gray-700/30 text-gray-600 dark:text-gray-400 border border-dashed border-gray-300 dark:border-gray-600 mx-2 my-2 text-center text-sm">
      <p>No tasks in this list.</p>
      {#if listTitle.toLowerCase().includes("active")}
        <p class="text-xs mt-1">All tasks are completed or set as current focus!</p>
      {/if}
    </div>
  {:else}
    <ul class="space-y-2 px-2">
      {#each todos as todo (todo.id)}
        <li class="border border-blue-200 dark:border-blue-700 rounded-md p-3 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors {todo.is_current_focus ? 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-700' : ''}">
          <div class="flex items-center">
            <input
              type="checkbox"
              class="w-4 h-4 mr-3 rounded border-blue-300 text-blue-500 focus:ring-blue-500"
              checked={todo.status === 'completed'}
              onchange={() => handleToggleStatus(todo)}
            />
            <div class="flex-grow">
              <div class="flex items-center">
                <span class="font-medium text-blue-900 dark:text-blue-100 {todo.status === 'completed' ? 'line-through text-blue-500/70 dark:text-blue-400/70' : ''}">{todo.title}</span>
                {#if todo.priority === 'high'}
                  <span class="ml-2 text-xs px-1.5 py-0.5 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-full">High</span>
                {:else if todo.priority === 'medium'}
                  <span class="ml-2 text-xs px-1.5 py-0.5 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 rounded-full">Medium</span>
                {/if}
              </div>
              {#if todo.due_date}
                <p class="text-xs text-blue-600 dark:text-blue-400 mt-1">Due: {new Date(todo.due_date).toLocaleDateString()}</p>
              {/if}
            </div>
            <div class="flex space-x-1">
              <button
                class="p-1 {todo.is_current_focus ? 'text-yellow-500 hover:text-yellow-600' : 'text-gray-400 hover:text-yellow-500'} transition-colors {loadingFocusToggle.has(todo.id) ? 'opacity-50 cursor-not-allowed' : ''}"
                title={todo.is_current_focus ? "Remove from Main Focus" : "Set as Main Focus"}
                aria-label={todo.is_current_focus ? "Remove from Main Focus" : "Set as Main Focus"}
                onclick={() => handleSetAsFocus(todo)}
                disabled={loadingFocusToggle.has(todo.id)}
              >
                {#if loadingFocusToggle.has(todo.id)}
                  <div class="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                {:else}
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                {/if}
              </button>
              <button
                class="p-1 text-gray-400 hover:text-blue-500 transition-colors"
                title="Edit"
                aria-label="Edit task"
                onclick={() => handleEdit(todo)}
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
              <button
                class="p-1 text-gray-400 hover:text-red-500 transition-colors"
                title="Delete"
                aria-label="Delete task"
                onclick={() => handleDelete(todo)}
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </li>
      {/each}
    </ul>
  {/if}
</div>
