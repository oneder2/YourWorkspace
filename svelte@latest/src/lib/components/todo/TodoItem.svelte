<script lang="ts">
  // Import necessary Svelte and project modules
  import { todoStore } from '$lib/store/todoStore';
  import type { TodoItem, TodoStatus, TodoPriority } from '$lib/services/todoService';
  import { createEventDispatcher, onDestroy, onMount } from 'svelte';

  // Import Modal and Edit Form components
  import Modal from '$lib/components/common/Modal.svelte';
  import TodoEditForm from './TodoEditForm.svelte'; // For editing the full To-Do item

  // Component prop: the to-do item to display
  export let todo: TodoItem;

  // Event dispatcher for parent communication
  const dispatch = createEventDispatcher();

  // Local loading states for different asynchronous actions
  let isLoadingToggleStatus = false;
  let isLoadingDelete = false;
  let isLoadingToggleFocus = false;
  
  // UI state variables
  let showDetails = false; // To toggle visibility of description and other details
  let isEditModalOpen = false; // State to control edit modal visibility

  // Reference to the TodoEditForm component instance (if needed for direct method calls from modal footer)
  let todoEditFormComponent: TodoEditForm; 

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
      dispatch('actionError', { message: 'Failed to update completion status.' });
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
      dispatch('actionError', { message: 'Failed to update focus status.' });
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
      dispatch('deleted', { id: todo.id }); // Notify parent if needed (e.g., for an undo feature)
    } catch (error) {
      console.error(`Failed to delete todo ${todo.id}:`, error);
      dispatch('actionError', { message: 'Failed to delete item.' });
    } finally {
      isLoadingDelete = false;
    }
  }

  // Functions to control the visibility of the edit modal
  function openEditModal() {
    isEditModalOpen = true;
  }

  function closeEditModal() {
    isEditModalOpen = false;
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

  // Reactive statement to compute CSS classes for the item card based on its state
  $: itemClasses = `
    todo-item-card
    status-${todo.status.replace('_', '-')} 
    priority-${todo.priority}
    ${showDetails ? 'details-visible' : ''}
    ${todo.is_current_focus && todo.status !== 'completed' ? 'is-current-focus' : ''} 
  `;

  // Text representations for priority and status enums
  const priorityText: Record<TodoPriority, string> = { low: 'Low', medium: 'Medium', high: 'High' };
  const statusText: Record<TodoStatus, string> = { pending: 'Pending', in_progress: 'In Progress', completed: 'Completed', deferred: 'Deferred' };

  // Reactive statement to determine if the "Set as Focus" button should be disabled
  // It's disabled if the item is completed, or if trying to set focus would exceed the limit.
  $: disableSetFocusButton = todo.status === 'completed' || (!todo.is_current_focus && numberOfFocusedItems >= currentMaxFocus);

</script>

<div class={itemClasses}>
  <div class="todo-main-info">
    <div class="todo-checkbox-area">
      <input
        type="checkbox"
        id="status-{todo.id}"
        class="status-checkbox"
        checked={todo.status === 'completed'}
        on:change={handleToggleCompleteStatus}
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
        aria-labelledby="title-{todo.id}"
      />
      <label for="status-{todo.id}" class="checkbox-label" aria-hidden="true"></label>
    </div>

    <div class="todo-title-and-meta" on:click={() => showDetails = !showDetails} role="button" tabindex="0" on:keypress={(e) => e.key === 'Enter' && (showDetails = !showDetails)}>
      {#if todo.is_current_focus && todo.status !== 'completed'}
        <span class="focus-indicator-icon" title="Current Focus Item">⭐</span>
      {/if}
      <h4 class="todo-title" id="title-{todo.id}" class:completed={todo.status === 'completed'}>
        {todo.title}
      </h4>
      <div class="todo-meta">
        {#if todo.due_date}
          <span class="meta-item due-date" title="Due Date">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            {formatDate(todo.due_date)}
          </span>
        {/if}
        <span class="meta-item priority priority-{todo.priority}" title="Priority: {priorityText[todo.priority]}">
           <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          {priorityText[todo.priority]}
        </span>
         <span class="meta-item status status-badge-{todo.status.replace('_', '-')}" title="Status: {statusText[todo.status]}">
          {statusText[todo.status]}
        </span>
      </div>
    </div>

    <div class="todo-actions">
      {#if todo.status !== 'completed'} 
        <button
          class="action-button focus-button"
          class:is-focus={todo.is_current_focus}
          on:click|stopPropagation={handleToggleFocus}
          title={todo.is_current_focus ? 'Remove from Current Focus' : 'Set as Current Focus'}
          aria-label={todo.is_current_focus ? `Remove ${todo.title} from Current Focus` : `Set ${todo.title} as Current Focus`}
          disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus || (disableSetFocusButton && !todo.is_current_focus)}
        >
          {#if isLoadingToggleFocus}
            <span class="spinner small-spinner"></span>
          {:else if todo.is_current_focus}
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="star-filled"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          {:else}
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="star-outline"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          {/if}
        </button>
      {/if}
      <button
        class="action-button edit-button"
        on:click|stopPropagation={openEditModal}
        title="Edit To-Do"
        aria-label="Edit To-Do item: {todo.title}"
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
      </button>
      <button
        class="action-button delete-button"
        on:click|stopPropagation={handleDelete}
        title="Delete To-Do"
        aria-label="Delete To-Do item: {todo.title}"
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
      >
        {#if isLoadingDelete}
          <span class="spinner small-spinner"></span>
        {:else}
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
        {/if}
      </button>
    </div>
  </div>

  {#if showDetails && todo.description}
    <div class="todo-details-content">
      <p class="description-text">{todo.description}</p>
    </div>
  {/if}
</div>

{#if isEditModalOpen}
  <Modal
    isOpen={isEditModalOpen}
    title="Edit To-Do: {todo.title}"
    on:close={closeEditModal}
    modalWidth="max-w-xl" 
  >
    <div> 
      <TodoEditForm
        bind:this={todoEditFormComponent}
        todo={todo} 
        on:saveSuccess={closeEditModal} 
        on:closeModalRequest={closeEditModal} 
      />
    </div>
    <div slot="footer" class="modal-form-actions">
      <button 
        type="button" 
        class="button secondary-button" 
        on:click={() => todoEditFormComponent.handleCancel()} 
        disabled={todoEditFormComponent?.isLoading}
      >
        Cancel
      </button>
      <button 
        type="submit" 
        class="button primary-button" 
        on:click={() => todoEditFormComponent.handleSubmit()} 
        disabled={todoEditFormComponent?.isLoading}
        form="todo-edit-form-{todo.id}"  
      >
        {#if todoEditFormComponent?.isLoading}
          Saving...
        {:else}
          Save Changes
        {/if}
      </button>
    </div>
  </Modal>
{/if}

<style>
  /* Styles for the to-do item card and its elements */
  .todo-item-card {
    background-color: #ffffff; /* Default background */
    border: 1px solid var(--border-color, #e0e0e0); /* Default border color */
    border-radius: var(--border-radius-md, 0.375rem); /* Medium border radius */
    padding: 1rem 1.25rem; /* Padding inside the card */
    transition: box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out, background-color 0.2s ease;
    display: flex;
    flex-direction: column;
    border-left: 4px solid transparent; /* Base for focus/priority indicator */
  }
  .todo-item-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Shadow on hover */
    border-color: var(--border-color-hover, #cccccc); /* Border color on hover */
  }
  .todo-item-card.is-current-focus { /* Style for items marked as current focus */
    border-left-color: var(--focus-indicator-color, #ffc107); /* Yellowish indicator for focus */
    background-color: var(--focus-item-bg, #fffbeb); /* Light yellow background for focus */
  }

  .focus-indicator-icon { /* Star icon for focused items */
    color: var(--focus-indicator-color, #ffc107); 
    margin-right: 0.5em; /* Space to the right of the star */
    font-size: 1.1em; 
    line-height: 1; 
  }
  
  .focus-button.is-focus svg { /* When item IS a focus item (button shows filled star) */
    fill: var(--focus-indicator-color, #ffc107); 
    stroke: var(--focus-indicator-color, #ffc107);
  }
  .focus-button:disabled:not(.is-focus) { /* When "Set as Focus" is disabled due to limit */
    opacity: 0.4 !important; /* Ensure it looks clearly disabled */
    cursor: not-allowed !important;
  }

  /* Spinner animation for loading states */
  @keyframes spin { to { transform: rotate(360deg); } }
  .spinner.small-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid currentColor; /* Spinner color inherits from text color */
    border-top-color: transparent; /* Makes the spinner look like a C-shape */
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    display: inline-block; /* Ensure it behaves well in button context */
  }

  /* Layout for the main information row */
  .todo-main-info { display: flex; align-items: center; width: 100%; }
  .todo-checkbox-area { margin-right: 1rem; flex-shrink: 0; display: flex; align-items: center; }
  .status-checkbox { width: 20px; height: 20px; cursor: pointer; accent-color: var(--primary-color, #007bff); }
  .status-checkbox:disabled { cursor: not-allowed; opacity: 0.6; }
  .checkbox-label { display: none; } /* Hidden label, using aria-labelledby on checkbox */
  .todo-title-and-meta { flex-grow: 1; cursor: pointer; min-width: 0; /* Prevents overflow issues with long titles */ }
  .todo-title { font-size: 1.1rem; font-weight: 600; color: var(--text-primary, #333); margin: 0 0 0.25rem 0; word-break: break-word; }
  .todo-title.completed { text-decoration: line-through; color: var(--text-secondary, #6c757d); opacity: 0.8; }
  
  /* Meta information (due date, priority, status badges) */
  .todo-meta { display: flex; flex-wrap: wrap; gap: 0.75rem; font-size: 0.8rem; color: var(--text-muted, #6c757d); }
  .meta-item { display: inline-flex; align-items: center; padding: 0.2rem 0.5rem; border-radius: var(--border-radius-sm, 0.25rem); background-color: var(--meta-item-bg, #f0f0f0); }
  .meta-item svg { margin-right: 0.3em; opacity: 0.7; }
  .priority-low { background-color: var(--priority-low-bg, #e6f4ea); color: var(--priority-low-text, #28a745); }
  .priority-medium { background-color: var(--priority-medium-bg, #fff3cd); color: var(--priority-medium-text, #ffc107); }
  .priority-high { background-color: var(--priority-high-bg, #f8d7da); color: var(--priority-high-text, #dc3545); }
  .status-badge-pending { background-color: var(--status-pending-bg, #cfe2ff); color: var(--status-pending-text, #0d6efd); }
  .status-badge-in-progress { background-color: var(--status-inprogress-bg, #fff3cd); color: var(--status-inprogress-text, #ffc107); }
  .status-badge-completed { background-color: var(--status-completed-bg, #d1e7dd); color: var(--status-completed-text, #198754); }
  .status-badge-deferred { background-color: var(--status-deferred-bg, #e2e3e5); color: var(--status-deferred-text, #6c757d); }
  
  /* Action buttons (focus, edit, delete) */
  .todo-actions { display: flex; align-items: center; margin-left: 1rem; /* Space between title/meta and actions */ }
  .action-button { background: none; border: none; color: var(--text-secondary, #6c757d); padding: 0.4rem; border-radius: 50%; /* Circular buttons */ cursor: pointer; display: inline-flex; align-items: center; justify-content: center; transition: background-color 0.2s ease, color 0.2s ease; margin-left: 0.5rem; /* Space between action buttons */ }
  .action-button:hover:not(:disabled) { background-color: var(--button-hover-bg, #f0f0f0); }
  .action-button:disabled { opacity: 0.5; cursor: not-allowed; }
  .edit-button:hover:not(:disabled) { color: var(--info-color, #0dcaf0); /* Example: light blue for edit */ }
  .delete-button:hover:not(:disabled) { color: var(--danger-color, #dc3545); /* Example: red for delete */ }
  
  /* Collapsible details section */
  .todo-details-content { padding-top: 0.75rem; margin-top: 0.75rem; border-top: 1px dashed var(--border-color-light, #e9ecef); font-size: 0.9rem; color: var(--text-secondary, #555); }
  .description-text { white-space: pre-wrap; /* Preserve line breaks and spaces */ word-break: break-word; }
  
  /* Styles for buttons within the modal's footer */
  .modal-form-actions .button { padding: 0.6rem 1.2rem; font-size: 0.9rem; font-weight: 500; border-radius: var(--border-radius, 0.375rem); cursor: pointer; transition: background-color 0.2s ease, border-color 0.2s ease; }
  .modal-form-actions .primary-button { background-color: var(--primary-color, #007bff); color: white; border: 1px solid var(--primary-color, #007bff); }
  .modal-form-actions .primary-button:hover:not(:disabled) { background-color: #0056b3; border-color: #0056b3; }
  .modal-form-actions .primary-button:disabled { background-color: var(--secondary-color, #6c757d); border-color: var(--secondary-color, #6c757d); opacity: 0.65; }
  .modal-form-actions .secondary-button { background-color: var(--button-secondary-bg, #6c757d); color: white; border: 1px solid var(--button-secondary-bg, #6c757d); }
  .modal-form-actions .secondary-button:hover:not(:disabled) { background-color: #5a6268; border-color: #545b62; }
  .modal-form-actions .secondary-button:disabled { opacity: 0.65; }
</style>
