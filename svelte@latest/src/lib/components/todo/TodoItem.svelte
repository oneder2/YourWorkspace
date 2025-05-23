<script lang="ts">
  // Import necessary Svelte and project modules
  import { todoStore } from '$lib/store/todoStore';
  import type { TodoItem, TodoStatus, TodoPriority } from '$lib/services/todoService';
  import { onDestroy } from 'svelte';

  // Import Edit Drawer component
  import TodoEditDrawer from './TodoEditDrawer.svelte'; // For editing the full To-Do item

  // No default export needed for Svelte 5 components

  // Component prop: the to-do item to display
  export let todo: TodoItem;

  // Event callbacks for parent communication using Svelte 5 approach
  export let onActionError = (message: string) => {};
  export let onDeleted = (id: number) => {};

  // Local loading states for different asynchronous actions
  let isLoadingToggleStatus = false;
  let isLoadingDelete = false;
  let isLoadingToggleFocus = false;

  // UI state variables
  let showDetails = false; // To toggle visibility of description and other details
  let isEditDrawerOpen = false; // State to control edit drawer visibility

  // Subscribe to relevant parts of todoStore for focus limit logic
  let currentMaxFocus: number;
  let numberOfFocusedItems: number;

  // Subscribe to the todoStore to get updates on maxFocusItems and the current number of focused items.
  // This subscription is cleaned up in onDestroy.
  const unsubscribeStore = todoStore.subscribe(storeState => {
    currentMaxFocus = storeState.maxFocusItems;
    // Calculate current number of active (not completed) focused items
    numberOfFocusedItems = storeState.todos.filter(t => t.is_current_focus && t.status !== 'completed').length;
  });

  // Lifecycle hook: clean up the store subscription when the component is destroyed
  onDestroy(() => {
    unsubscribeStore();
  });

  /**
   * Handles toggling the completion status of the to-do item.
   * It calls the todoStore to update the status and handles loading/error states.
   */
  async function handleToggleCompleteStatus() {
    if (!todo) return;
    isLoadingToggleStatus = true;
    try {
      // The toggleCompleteStatus method in the store also handles un-focusing if the item is completed.
      await todoStore.toggleCompleteStatus(todo.id, todo.status);
    } catch (error) {
      console.error(`Failed to toggle complete status for todo ${todo.id}:`, error);
      onActionError('Failed to update completion status.');
    } finally {
      isLoadingToggleStatus = false;
    }
  }

  /**
   * Handles toggling the 'is_current_focus' status of the to-do item.
   * It checks against the focus limit before attempting to set an item as focus.
   */
  async function handleToggleFocus() {
    if (!todo || todo.status === 'completed') return; // Cannot focus a completed item

    // Check if attempting to set a new item as focus would exceed the defined limit
    if (!todo.is_current_focus && numberOfFocusedItems >= currentMaxFocus) {
      alert(`You can only have up to ${currentMaxFocus} items in current focus. Please remove another item from focus first.`);
      // dispatch('focusLimitReached', { limit: currentMaxFocus }); // Alternative: dispatch event for custom notification
      return;
    }

    isLoadingToggleFocus = true;
    try {
      await todoStore.toggleCurrentFocus(todo.id);
      // The store update will reactively update the 'todo' prop if the parent list re-renders,
      // or if the item instance itself is updated in the store.
    } catch (error) {
      console.error(`Failed to toggle focus for todo ${todo.id}:`, error);
      onActionError('Failed to update focus status.');
    } finally {
      isLoadingToggleFocus = false;
    }
  }

  /**
   * Handles deleting the to-do item after user confirmation.
   */
  async function handleDelete() {
    if (!todo) return;
    // Optional: Use a more sophisticated confirmation modal instead of window.confirm
    if (!confirm(`Are you sure you want to delete "${todo.title}"?`)) {
      return;
    }
    isLoadingDelete = true;
    try {
      await todoStore.removeTodo(todo.id);
      // Item will be removed from the store, and the list will reactively update.
      onDeleted(todo.id); // Notify parent if needed (e.g., for an undo feature)
    } catch (error) {
      console.error(`Failed to delete todo ${todo.id}:`, error);
      onActionError('Failed to delete item.');
    } finally {
      isLoadingDelete = false;
    }
  }

  // Functions to control the visibility of the edit drawer
  function openEditDrawer() {
    isEditDrawerOpen = true;
  }

  function closeEditDrawer() {
    isEditDrawerOpen = false;
  }

  /**
   * Utility function to format date strings.
   * @param dateString - The date string to format (e.g., "YYYY-MM-DD").
   * @returns A formatted date string (e.g., "May 10, 2025") or "N/A".
   */
  function formatDate(dateString?: string | null): string {
    if (!dateString) return 'N/A';
    try {
      // Assuming dateString is YYYY-MM-DD. Appending T00:00:00 helps ensure it's parsed in local timezone.
      const date = new Date(dateString + 'T00:00:00');
      return new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'short', day: 'numeric' }).format(date);
    } catch (e) {
      return dateString; // Fallback if formatting fails
    }
  }

  // Reactive statement to compute Tailwind CSS classes for the item card based on its state
  $: itemClasses = `
    bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md p-5
    transition-all duration-200 ease-in-out
    hover:shadow-md hover:border-gray-300 dark:hover:border-gray-600
    ${todo.is_current_focus && todo.status !== 'completed' ? 'border-l-4 border-l-warning-500 bg-warning-50 dark:bg-warning-900/20' : 'border-l-4 border-l-transparent'}
  `;

  // Text representations for priority and status enums
  const priorityText: Record<TodoPriority, string> = { low: 'Low', medium: 'Medium', high: 'High' };
  const statusText: Record<TodoStatus, string> = { pending: 'Pending', in_progress: 'In Progress', completed: 'Completed', deferred: 'Deferred' };

  // Reactive statement to determine if the "Set as Focus" button should be disabled
  // It's disabled if the item is completed, or if trying to set focus would exceed the limit.
  $: disableSetFocusButton = todo.status === 'completed' || (!todo.is_current_focus && numberOfFocusedItems >= currentMaxFocus);

</script>

<div class={itemClasses}>
  <div class="flex items-center w-full">
    <div class="mr-4 flex-shrink-0 flex items-center">
      <input
        type="checkbox"
        id="status-{todo.id}"
        class="w-5 h-5 cursor-pointer accent-primary-500 disabled:cursor-not-allowed disabled:opacity-60"
        checked={todo.status === 'completed'}
        on:change={handleToggleCompleteStatus}
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
        aria-labelledby="title-{todo.id}"
      />
      <label for="status-{todo.id}" class="sr-only" aria-hidden="true"></label>
    </div>

    <div
      class="flex-grow cursor-pointer min-w-0"
      on:click={() => showDetails = !showDetails}
      role="button"
      tabindex="0"
      on:keypress={(e) => e.key === 'Enter' && (showDetails = !showDetails)}
    >
      {#if todo.is_current_focus && todo.status !== 'completed'}
        <span class="text-warning-500 mr-2 text-lg leading-none" title="Current Focus Item">⭐</span>
      {/if}
      <h4
        id="title-{todo.id}"
        class="text-lg font-semibold text-gray-900 dark:text-white mb-1 break-words {todo.status === 'completed' ? 'line-through text-gray-500 dark:text-gray-400 opacity-80' : ''}"
      >
        {todo.title}
      </h4>
      <div class="flex flex-wrap gap-3 text-sm text-gray-600 dark:text-gray-400">
        {#if todo.due_date}
          <span
            class="inline-flex items-center px-2 py-1 rounded-md bg-gray-100 dark:bg-gray-700"
            title="Due Date"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1 opacity-70"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            {formatDate(todo.due_date)}
          </span>
        {/if}

        <!-- Priority badge with color based on priority -->
        <span
          class={`inline-flex items-center px-2 py-1 rounded-md ${
            todo.priority === 'high'
              ? 'bg-danger-50 text-danger-700 dark:bg-danger-900/30 dark:text-danger-300'
              : todo.priority === 'medium'
                ? 'bg-warning-50 text-warning-700 dark:bg-warning-900/30 dark:text-warning-300'
                : 'bg-success-50 text-success-700 dark:bg-success-900/30 dark:text-success-300'
          }`}
          title="Priority: {priorityText[todo.priority]}"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-1 opacity-70"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          {priorityText[todo.priority]}
        </span>

        <!-- Status badge with color based on status -->
        <span
          class={`inline-flex items-center px-2 py-1 rounded-md ${
            todo.status === 'completed'
              ? 'bg-success-50 text-success-700 dark:bg-success-900/30 dark:text-success-300'
              : todo.status === 'in_progress'
                ? 'bg-warning-50 text-warning-700 dark:bg-warning-900/30 dark:text-warning-300'
                : todo.status === 'pending'
                  ? 'bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
                  : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
          }`}
          title="Status: {statusText[todo.status]}"
        >
          {statusText[todo.status]}
        </span>
      </div>
    </div>

    <div class="flex items-center ml-4">
      {#if todo.status !== 'completed'}
        <button
          class={`p-2 rounded-full bg-transparent border-none text-gray-600 dark:text-gray-400
            hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed
            ${todo.is_current_focus ? 'text-warning-500 dark:text-warning-400' : ''}`}
          on:click|stopPropagation={handleToggleFocus}
          title={todo.is_current_focus ? 'Remove from Current Focus' : 'Set as Current Focus'}
          aria-label={todo.is_current_focus ? `Remove ${todo.title} from Current Focus` : `Set ${todo.title} as Current Focus`}
          disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus || (disableSetFocusButton && !todo.is_current_focus)}
        >
          {#if isLoadingToggleFocus}
            <span class="inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
          {:else if todo.is_current_focus}
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          {:else}
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          {/if}
        </button>
      {/if}
      <button
        class="p-2 rounded-full bg-transparent border-none text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-info-500 dark:hover:text-info-400 disabled:opacity-50 disabled:cursor-not-allowed ml-2"
        on:click|stopPropagation={openEditDrawer}
        title="Edit To-Do"
        aria-label="Edit To-Do item: {todo.title}"
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
      </button>
      <button
        class="p-2 rounded-full bg-transparent border-none text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-danger-500 dark:hover:text-danger-400 disabled:opacity-50 disabled:cursor-not-allowed ml-2"
        on:click|stopPropagation={handleDelete}
        title="Delete To-Do"
        aria-label="Delete To-Do item: {todo.title}"
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
      >
        {#if isLoadingDelete}
          <span class="inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
        {:else}
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
        {/if}
      </button>
    </div>
  </div>

  {#if showDetails && todo.description}
    <div class="pt-3 mt-3 border-t border-dashed border-gray-200 dark:border-gray-700 text-sm text-gray-700 dark:text-gray-300">
      <p class="whitespace-pre-wrap break-words">{todo.description}</p>
    </div>
  {/if}
</div>

<TodoEditDrawer
  todo={todo}
  isOpen={isEditDrawerOpen}
  onSaveSuccess={closeEditDrawer}
  onCloseRequest={closeEditDrawer}
/>
