<script lang="ts">
  // Import the main store for isLoading/error and the specific derived store
  import { todoStore, currentFocusTodos } from '$lib/store/todoStore';
  import type { TodoItem, TodoStatus } from '$lib/services/todoService';
</script>

<div class="focus-display-container">
  {#if $todoStore.isLoading && $todoStore.todos.length === 0}
    <div class="p-4 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800 rounded-md text-center">
      <p>Loading focus items...</p>
    </div>
  {:else if $currentFocusTodos.length === 0}
    <div class="p-6 bg-gray-50 dark:bg-gray-800/50 text-gray-600 dark:text-gray-400 border border-dashed border-gray-300 dark:border-gray-600 rounded-md text-center">
      <p>
        No current focus set.
        <br />
        You can mark a task as "Current Focus" from the todo list!
      </p>
    </div>
  {:else}
    <div class="focus-item-container border border-gray-200 dark:border-gray-700 rounded-md overflow-hidden">
      {#each $currentFocusTodos as focusItem (focusItem.id)}
        <div class="focus-item p-4 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
          <div class="flex items-start">
            <div class="flex-shrink-0 mr-3">
              <input
                type="checkbox"
                id="focus-status-{focusItem.id}"
                class="w-5 h-5 rounded border-gray-300 text-primary-500 focus:ring-primary-500"
                checked={focusItem.status === 'completed'}
                on:change={() => todoStore.toggleCompleteStatus(focusItem.id, focusItem.status)}
              />
            </div>
            <div class="flex-grow">
              <div class="flex items-center">
                <span class="text-yellow-500 mr-2">⭐</span>
                <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">{focusItem.title}</h3>
              </div>
              {#if focusItem.description}
                <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">{focusItem.description}</p>
              {/if}
              <div class="mt-2 flex flex-wrap gap-2">
                {#if focusItem.due_date}
                  <span class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300">
                    Due: {new Date(focusItem.due_date).toLocaleDateString()}
                  </span>
                {/if}
                <span class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium
                  {focusItem.priority === 'high' ? 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300' :
                   focusItem.priority === 'medium' ? 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-300' :
                   'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300'}">
                  {focusItem.priority.charAt(0).toUpperCase() + focusItem.priority.slice(1)} Priority
                </span>
              </div>
            </div>
            <div class="flex-shrink-0 flex space-x-2 ml-4">
              <button
                class="p-1 text-gray-500 hover:text-primary-500 transition-colors"
                title="Edit"
                aria-label="Edit task"
                on:click={() => {
                  const item = $todoStore.todos.find(t => t.id === focusItem.id);
                  if (item) {
                    alert(`Edit functionality will be implemented for: ${item.title}`);
                  }
                }}
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
              <button
                class="p-1 text-gray-500 hover:text-red-500 transition-colors"
                title="Delete"
                aria-label="Delete task"
                on:click={() => {
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
</div>
