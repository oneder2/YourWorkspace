<script lang="ts">
  // This component displays a To-Do item that is marked as a "Current Focus".
  // It's similar to TodoItem.svelte but tailored for the Current Focus section.

  import { todoStore } from '$lib/store/todoStore';
  import type { TodoItem, TodoStatus, TodoPriority } from '$lib/services/todoService';
  import { createEventDispatcher, onDestroy, onMount } from 'svelte';

  import Modal from '$lib/components/common/Modal.svelte';
  import TodoEditForm from '$lib/components/todo/TodoEditForm.svelte'; // Reusing the main edit form

  export let item: TodoItem; // Prop: The To-Do item to display (assumed to be is_current_focus: true)

  const dispatch = createEventDispatcher();

  // Local loading states
  let isLoadingToggleStatus = false;
  let isLoadingDelete = false;
  let isLoadingToggleFocus = false; // Specifically for the "Remove from Focus" action
  
  let showDetails = false;
  let isEditModalOpen = false;

  let todoEditFormComponent: TodoEditForm;

  // Handler for toggling completion status (inherited from TodoItem logic)
  async function handleToggleCompleteStatus() {
    if (!item) return;
    isLoadingToggleStatus = true;
    try {
      await todoStore.toggleCompleteStatus(item.id, item.status);
      // If item is completed, it should automatically be un-focused by the store logic
      // and will disappear from this CurrentFocusDisplay list.
    } catch (error) {
      console.error(`Failed to toggle complete status for focus item ${item.id}:`, error);
      dispatch('actionError', { message: 'Failed to update completion status.' });
    } finally {
      isLoadingToggleStatus = false;
    }
  }

  // Handler specifically to "Remove from Focus"
  async function handleRemoveFromFocus() {
    if (!item || !item.is_current_focus) return; // Should only be called on focused items

    isLoadingToggleFocus = true;
    try {
      await todoStore.toggleCurrentFocus(item.id); // This will set is_current_focus to false
      // The item will then be filtered out from the currentFocusTodos derived store
      // and disappear from this display area.
    } catch (error) {
      console.error(`Failed to remove from focus for item ${item.id}:`, error);
      dispatch('actionError', { message: 'Failed to update focus status.' });
    } finally {
      isLoadingToggleFocus = false;
    }
  }

  // Handler for deleting the to-do item
  async function handleDelete() {
    if (!item) return;
    if (!confirm(`Are you sure you want to delete this focused item: "${item.title}"?`)) {
      return;
    }
    isLoadingDelete = true;
    try {
      await todoStore.removeTodo(item.id);
      dispatch('deleted', { id: item.id });
    } catch (error) {
      console.error(`Failed to delete focus item ${item.id}:`, error);
      dispatch('actionError', { message: 'Failed to delete item.' });
    } finally {
      isLoadingDelete = false;
    }
  }

  // Edit modal functions
  function openEditModal() {
    isEditModalOpen = true;
  }
  function closeEditModal() {
    isEditModalOpen = false;
  }

  function formatDate(dateString?: string | null): string {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString + 'T00:00:00');
      return new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'short', day: 'numeric' }).format(date);
    } catch (e) { return dateString; }
  }

  // CSS classes for the item card
  $: itemClasses = `
    focus-display-item-card
    status-${item.status.replace('_', '-')}
    priority-${item.priority}
    ${showDetails ? 'details-visible' : ''}
  `; // No 'is-current-focus' class needed here as all items in this list are focused

  const priorityText: Record<TodoPriority, string> = { low: 'Low', medium: 'Medium', high: 'High' };
  const statusText: Record<TodoStatus, string> = { pending: 'Pending', in_progress: 'In Progress', completed: 'Completed', deferred: 'Deferred' };

</script>

<div class={itemClasses}>
  <div class="focus-item-main-info">
    <div class="focus-item-checkbox-area">
      <input
        type="checkbox"
        id="focus-status-{item.id}"
        class="status-checkbox"
        checked={item.status === 'completed'}
        on:change={handleToggleCompleteStatus}
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
        aria-labelledby="focus-title-{item.id}"
      />
      <label for="focus-status-{item.id}" class="checkbox-label" aria-hidden="true"></label>
    </div>

    <div class="focus-item-title-and-meta" on:click={() => showDetails = !showDetails} role="button" tabindex="0" on:keypress={(e) => e.key === 'Enter' && (showDetails = !showDetails)}>
      <span class="focus-indicator-main" title="Current Focus Item">⭐</span>
      <h4 class="focus-item-title" id="focus-title-{item.id}" class:completed={item.status === 'completed'}>
        {item.title}
      </h4>
      <div class="focus-item-meta">
        {#if item.due_date}
          <span class="meta-item due-date" title="Due Date">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            {formatDate(item.due_date)}
          </span>
        {/if}
        <span class="meta-item priority priority-{item.priority}" title="Priority: {priorityText[item.priority]}">
           <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          {priorityText[item.priority]}
        </span>
         <span class="meta-item status status-badge-{item.status.replace('_', '-')}" title="Status: {statusText[item.status]}">
          {statusText[item.status]}
        </span>
      </div>
    </div>

    <div class="focus-item-actions">
      {#if item.status !== 'completed'}
      <button
        class="action-button unfocus-button"
        on:click|stopPropagation={handleRemoveFromFocus}
        title="Remove from Current Focus"
        aria-label="Remove {item.title} from Current Focus"
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
      >
        {#if isLoadingToggleFocus}
          <span class="spinner small-spinner"></span>
        {:else}
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="unfocus-icon"><line x1="12" y1="2" x2="12" y2="6"></line><line x1="12" y1="18" x2="12" y2="22"></line><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line><line x1="2" y1="12" x2="6" y2="12"></line><line x1="18" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line></svg>
        {/if}
      </button>
      {/if}
      <button
        class="action-button edit-button"
        on:click|stopPropagation={openEditModal}
        title="Edit Focused Item"
        aria-label="Edit focused item: {item.title}"
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
      </button>
      <button
        class="action-button delete-button"
        on:click|stopPropagation={handleDelete}
        title="Delete Focused Item"
        aria-label="Delete focused item: {item.title}"
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

  {#if showDetails && item.description}
    <div class="focus-item-details-content">
      <p class="description-text">{item.description}</p>
    </div>
  {/if}
</div>

{#if isEditModalOpen}
  <Modal
    isOpen={isEditModalOpen}
    title="Edit Focus Item: {item.title}"
    on:close={closeEditModal}
    modalWidth="max-w-xl"
  >
    <div slot="body">
      <TodoEditForm
        bind:this={todoEditFormComponent}
        todo={item} on:saveSuccess={closeEditModal}
        on:closeModalRequest={closeEditModal}
      />
    </div>
    <div slot="footer" class="modal-form-actions">
      <button type="button" class="button secondary-button" on:click={() => todoEditFormComponent.handleCancel()} disabled={todoEditFormComponent?.isLoading}>
        Cancel
      </button>
      <button type="submit" class="button primary-button" on:click={() => todoEditFormComponent.handleSubmit()} disabled={todoEditFormComponent?.isLoading} form="todo-edit-form-{item.id}">
        {#if todoEditFormComponent?.isLoading} Saving... {:else} Save Changes {/if}
      </button>
    </div>
  </Modal>
{/if}

<style>
  .focus-display-item-card {
    background-color: var(--focus-card-bg, #fffef0); /* Distinct background for focus items */
    border: 1px solid var(--focus-card-border-color, #ffeeba);
    border-left: 5px solid var(--focus-indicator-color, #ffc107); /* Prominent focus indicator */
    border-radius: var(--border-radius-lg, 0.5rem);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-md, 0 5px 10px rgba(0,0,0,0.08));
    transition: box-shadow 0.2s ease-in-out;
  }
  .focus-display-item-card:hover {
    box-shadow: var(--shadow-lg, 0 8px 15px rgba(0,0,0,0.1));
  }

  .focus-indicator-main { /* Star icon next to title in focus display */
    color: var(--focus-indicator-color, #ffc107);
    margin-right: 0.6em;
    font-size: 1.3em;
    line-height: 1;
  }

  .focus-item-main-info { display: flex; align-items: center; width: 100%; }
  .focus-item-checkbox-area { margin-right: 1rem; flex-shrink: 0; display: flex; align-items: center; }
  .status-checkbox { width: 20px; height: 20px; cursor: pointer; accent-color: var(--primary-color, #007bff); }
  .status-checkbox:disabled { cursor: not-allowed; opacity: 0.6; }
  .checkbox-label { display: none; }
  .focus-item-title-and-meta { flex-grow: 1; cursor: pointer; min-width: 0; }
  .focus-item-title { font-size: 1.25rem; font-weight: 600; color: var(--text-heading, #333); margin: 0 0 0.3rem 0; word-break: break-word; display: inline; /* To align with star */}
  .focus-item-title.completed { text-decoration: line-through; color: var(--text-secondary, #6c757d); opacity: 0.8; }
  .focus-item-meta { display: flex; flex-wrap: wrap; gap: 0.75rem; font-size: 0.8rem; color: var(--text-muted, #6c757d); margin-top: 0.25rem; }
  .meta-item { display: inline-flex; align-items: center; padding: 0.2rem 0.5rem; border-radius: var(--border-radius-sm, 0.25rem); background-color: var(--meta-item-bg-focus, #f8f9fa); }
  .meta-item svg { margin-right: 0.3em; opacity: 0.7; }
  .priority-low { background-color: var(--priority-low-bg, #e6f4ea); color: var(--priority-low-text, #28a745); }
  .priority-medium { background-color: var(--priority-medium-bg, #fff3cd); color: var(--priority-medium-text, #ffc107); }
  .priority-high { background-color: var(--priority-high-bg, #f8d7da); color: var(--priority-high-text, #dc3545); }
  .status-badge-pending { background-color: var(--status-pending-bg, #cfe2ff); color: var(--status-pending-text, #0d6efd); }
  .status-badge-in-progress { background-color: var(--status-inprogress-bg, #fff3cd); color: var(--status-inprogress-text, #ffc107); }
  .status-badge-completed { background-color: var(--status-completed-bg, #d1e7dd); color: var(--status-completed-text, #198754); }
  .status-badge-deferred { background-color: var(--status-deferred-bg, #e2e3e5); color: var(--status-deferred-text, #6c757d); }
  
  .focus-item-actions { display: flex; align-items: center; margin-left: 1rem; }
  .action-button { background: none; border: none; color: var(--text-secondary, #6c757d); padding: 0.4rem; border-radius: 50%; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; transition: background-color 0.2s ease, color 0.2s ease; margin-left: 0.5rem; }
  .action-button:hover:not(:disabled) { background-color: var(--button-hover-bg-focus, #e9ecef); }
  .action-button:disabled { opacity: 0.5; cursor: not-allowed; }
  
  .unfocus-button svg.unfocus-icon { /* Specific styling for unfocus icon if needed */
    stroke: var(--focus-indicator-color, #ffc107); /* Example: make it yellow */
  }
  .unfocus-button:hover:not(:disabled) { color: var(--focus-indicator-color, #ffc107); }
  .edit-button:hover:not(:disabled) { color: var(--info-color, #0dcaf0); }
  .delete-button:hover:not(:disabled) { color: var(--danger-color, #dc3545); }

  .focus-item-details-content { padding-top: 0.75rem; margin-top: 0.75rem; border-top: 1px dashed var(--border-color-light, #e9ecef); font-size: 0.9rem; color: var(--text-secondary, #555); }
  .description-text { white-space: pre-wrap; word-break: break-word; }

  @keyframes spin { to { transform: rotate(360deg); } }
  .spinner.small-spinner { width: 16px; height: 16px; border: 2px solid currentColor; border-top-color: transparent; border-radius: 50%; animation: spin 0.8s linear infinite; }
  
  .modal-form-actions .button { padding: 0.6rem 1.2rem; font-size: 0.9rem; font-weight: 500; border-radius: var(--border-radius, 0.375rem); cursor: pointer; transition: background-color 0.2s ease, border-color 0.2s ease; }
  .modal-form-actions .primary-button { background-color: var(--primary-color, #007bff); color: white; border: 1px solid var(--primary-color, #007bff); }
  .modal-form-actions .primary-button:hover:not(:disabled) { background-color: #0056b3; border-color: #0056b3; }
  .modal-form-actions .primary-button:disabled { background-color: var(--secondary-color, #6c757d); border-color: var(--secondary-color, #6c757d); opacity: 0.65; }
  .modal-form-actions .secondary-button { background-color: var(--button-secondary-bg, #6c757d); color: white; border: 1px solid var(--button-secondary-bg, #6c757d); }
  .modal-form-actions .secondary-button:hover:not(:disabled) { background-color: #5a6268; border-color: #545b62; }
  .modal-form-actions .secondary-button:disabled { opacity: 0.65; }
</style>
