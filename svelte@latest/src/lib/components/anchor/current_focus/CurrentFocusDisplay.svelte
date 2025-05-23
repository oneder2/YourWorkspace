<script lang="ts">
  // Import the main store for isLoading/error and the specific derived store
  import { todoStore, currentFocusTodos } from '$lib/store/todoStore';
  import type { TodoItem } from '$lib/services/todoService';
  import MainFocusEditModal from './MainFocusEditModal.svelte';

  // State for edit modal
  let isEditModalOpen = $state(false);
  let currentEditingItem = $state<TodoItem | null>(null);

  // State for loading operations
  let loadingFocusToggle = $state<Set<number>>(new Set());

  // Function to handle removing an item from focus
  async function handleRemoveFromFocus(id: number) {
    if (confirm("Remove this item from Main Focus?")) {
      loadingFocusToggle.add(id);
      loadingFocusToggle = new Set(loadingFocusToggle); // Trigger reactivity
      try {
        await todoStore.toggleCurrentFocus(id);
      } finally {
        loadingFocusToggle.delete(id);
        loadingFocusToggle = new Set(loadingFocusToggle); // Trigger reactivity
      }
    }
  }

  // Function to open the edit modal
  function openEditModal(item: TodoItem) {
    currentEditingItem = item;
    isEditModalOpen = true;
  }

  // Function to close the edit modal
  function closeEditModal() {
    isEditModalOpen = false;
    currentEditingItem = null;
  }
</script>

<div class="focus-display-container">
  {#if $todoStore.isLoading && $todoStore.todos.length === 0}
    <div class="p-4 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800 rounded-md text-center">
      <p>Loading focus items...</p>
    </div>
  {:else if $currentFocusTodos.length === 0}
    <div class="p-6 bg-amber-50/50 dark:bg-amber-900/10 text-amber-700 dark:text-amber-400 border border-dashed border-amber-300 dark:border-amber-700 rounded-md text-center">
      <p>
        No current focus set.
        <br />
        You can mark a task as "Current Focus" from the todo list!
      </p>
    </div>
  {:else}
    <div class="focus-item-container border border-amber-200 dark:border-amber-700 rounded-md overflow-hidden bg-amber-50/50 dark:bg-amber-900/10">
      {#each $currentFocusTodos as focusItem (focusItem.id)}
        <div class="focus-item p-4 border-b border-amber-200 dark:border-amber-700 last:border-b-0">
          <div class="flex items-start">
            <div class="flex-shrink-0 mr-3">
              <input
                type="checkbox"
                id="focus-status-{focusItem.id}"
                class="w-5 h-5 rounded border-amber-300 text-amber-500 focus:ring-amber-500"
                checked={focusItem.status === 'completed'}
                onchange={() => todoStore.toggleCompleteStatus(focusItem.id, focusItem.status)}
              />
            </div>
            <div class="flex-grow">
              <div class="flex items-center">
                <span class="text-yellow-500 mr-2">⭐</span>
                <h3 class="text-lg font-medium text-amber-900 dark:text-amber-100">{focusItem.title}</h3>
              </div>
              {#if focusItem.description}
                <p class="mt-1 text-sm text-amber-700 dark:text-amber-300">{focusItem.description}</p>
              {/if}
              <div class="mt-2 flex flex-wrap gap-2">
                {#if focusItem.due_date}
                  <span class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-amber-100 dark:bg-amber-800/40 text-amber-800 dark:text-amber-200 border border-amber-200 dark:border-amber-700">
                    Due: {new Date(focusItem.due_date).toLocaleDateString()}
                  </span>
                {/if}
                <span class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium
                  {focusItem.priority === 'high' ? 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800' :
                   focusItem.priority === 'medium' ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 border border-yellow-200 dark:border-yellow-800' :
                   'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800'}">
                  {focusItem.priority.charAt(0).toUpperCase() + focusItem.priority.slice(1)} Priority
                </span>
              </div>
            </div>
            <div class="flex-shrink-0 flex space-x-2 ml-4">
              <button
                class="p-1 text-amber-600 hover:text-amber-800 dark:text-amber-400 dark:hover:text-amber-300 transition-colors"
                title="Edit"
                aria-label="Edit task"
                onclick={() => {
                  const item = $todoStore.todos.find(t => t.id === focusItem.id);
                  if (item) {
                    openEditModal(item);
                  }
                }}
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
              <button
                class="p-1 text-amber-600 hover:text-blue-500 dark:text-amber-400 dark:hover:text-blue-400 transition-colors disabled:opacity-50"
                title="Remove from Main Focus"
                aria-label="Remove from Main Focus"
                onclick={() => handleRemoveFromFocus(focusItem.id)}
                disabled={loadingFocusToggle.has(focusItem.id)}
              >
                {#if loadingFocusToggle.has(focusItem.id)}
                  <div class="h-5 w-5 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                {:else}
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                {/if}
              </button>
              <button
                class="p-1 text-amber-600 hover:text-red-500 dark:text-amber-400 dark:hover:text-red-400 transition-colors"
                title="Delete"
                aria-label="Delete task"
                onclick={() => {
                  if (confirm(`Are you sure you want to delete "${focusItem.title}"?`)) {
                    todoStore.removeTodo(focusItem.id);
                  }
                }}
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}

  {#if $todoStore.error && $todoStore.todos.length === 0 && !$todoStore.isLoading}
    <div class="p-4 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800 rounded-md text-center">
      <p>Failed to load items: {$todoStore.error}</p>
    </div>
  {/if}

  {#if currentEditingItem}
    <MainFocusEditModal
      todo={currentEditingItem}
      isOpen={isEditModalOpen}
      onSaveSuccess={closeEditModal}
      onCloseRequest={closeEditModal}
    />
  {/if}
</div>
