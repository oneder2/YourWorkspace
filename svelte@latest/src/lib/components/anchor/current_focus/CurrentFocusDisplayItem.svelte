<script lang="ts">
  import { todoStore } from '$lib/store/todoStore';
  // Assuming TodoItem, TodoStatus, TodoPriority are correctly defined in todoService
  import type { TodoItem, TodoStatus, TodoPriority, UpdateTodoPayload } from '$lib/services/todoService'; 

  // --- Props ---
  export let item: TodoItem; // Prop: The To-Do item to display 

  // --- Callback Props ---
  export let onActionError: (detail: { message: string }) => void = (detail) => {
    console.warn("CurrentFocusDisplayItem: onActionError prop was not provided.", detail);
  };
  export let onFocusCleared: (itemId: number) => void = (itemId) => {
    console.warn("CurrentFocusDisplayItem: onFocusCleared prop was not provided.", itemId);
  };
  export let onDeleted: (itemId: number) => void = (itemId) => {
    console.warn("CurrentFocusDisplayItem: onDeleted prop was not provided.", itemId);
  };
  export let onEditRequest: (itemToEdit: TodoItem) => void = (itemToEdit) => {
    console.warn("CurrentFocusDisplayItem: onEditRequest prop was not provided.", itemToEdit);
  };

  // --- Component State ---
  let isLoadingToggleStatus = false;
  let isLoadingDelete = false;
  let isLoadingToggleFocus = false; 
  
  // --- Derived State ---
  $: isCompleted = !!item.completed_at; // Use completed_at

  // --- Event Handlers ---
  async function handleToggleCompleteStatus() {
    if (!item) return;
    isLoadingToggleStatus = true;
    try {
      const newCompletedAt = isCompleted ? null : new Date().toISOString();
      const payload: Partial<UpdateTodoPayload> = { 
        completed_at: newCompletedAt,
        // If completing an item, also update its status to 'completed'
        // If un-completing, revert to 'pending' or 'in_progress' (this might need more complex logic or be handled by backend)
        status: newCompletedAt ? 'completed' : 'pending' // Simplified status update
      };

      if (newCompletedAt && item.is_current_focus) { // If marking as complete AND it was a focus
        payload.is_current_focus = false; // Also unfocus it
      }
      
      const updatedItem = await todoStore.updateTodo(item.id, payload);

      if (payload.is_current_focus === false && updatedItem) {
        onFocusCleared(item.id); 
      }
    } catch (error) {
      console.error(`Failed to toggle complete status for focus item ${item.id}:`, error);
      const msg = error instanceof Error ? error.message : 'Failed to update completion status.';
      onActionError({ message: msg });
    } finally {
      isLoadingToggleStatus = false;
    }
  }

  async function handleRemoveFromFocus() {
    if (!item || !item.is_current_focus) return; 
    isLoadingToggleFocus = true;
    try {
      await todoStore.updateTodo(item.id, { is_current_focus: false });
      onFocusCleared(item.id); 
    } catch (error) {
      console.error(`Failed to remove from focus for item ${item.id}:`, error);
      const msg = error instanceof Error ? error.message : 'Failed to update focus status.';
      onActionError({ message: msg });
    } finally {
      isLoadingToggleFocus = false;
    }
  }

  async function handleDelete() {
    if (!item) return;
    if (!confirm(`Are you sure you want to delete this focused item: "${item.title}"?`)) {
      return;
    }
    isLoadingDelete = true;
    try {
      await todoStore.removeTodo(item.id);
      onDeleted(item.id); 
    } catch (error) {
      console.error(`Failed to delete focus item ${item.id}:`, error);
      const msg = error instanceof Error ? error.message : 'Failed to delete item.';
      onActionError({ message: msg });
    } finally {
      isLoadingDelete = false;
    }
  }

  function requestEdit() {
    onEditRequest(item); 
  }

  function formatDate(dateString?: string | null): string {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString.includes('T') ? dateString : dateString + 'T00:00:00Z'); // Assume UTC if no T
      return new Intl.DateTimeFormat('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' }).format(date); // Using zh-CN for date format
    } catch (e) { return dateString; }
  }
  
  // Text representations for TodoPriority and TodoStatus
  // Ensure TodoPriority and TodoStatus types are correctly imported or defined if they are string literal unions
  const priorityText: Record<TodoPriority, string> = { 
    low: '低', 
    medium: '中', 
    high: '高' 
  };
  const statusText: Record<TodoStatus, string> = { 
    pending: '待处理', 
    in_progress: '进行中', 
    completed: '已完成', 
    deferred: '已推迟' 
    // Add 'abandoned' if it's part of your TodoStatus enum/type
    // abandoned: '已放弃' 
  };

  $: itemClasses = `
    focus-display-item-card
    status-${item.status.replace('_', '-')} 
    priority-${item.priority}
    ${isCompleted ? 'item-completed' : ''}
  `;
</script>

<div class={itemClasses}>
  <div class="focus-item-main-info">
    <div class="focus-item-checkbox-area">
      <input
        type="checkbox"
        id="focus-status-{item.id}"
        class="status-checkbox"
        checked={isCompleted}
        on:change={handleToggleCompleteStatus}
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
        aria-labelledby="focus-title-{item.id}"
      />
      <label for="focus-status-{item.id}" class="checkbox-label" aria-hidden="true"></label>
    </div>

    <div class="focus-item-title-and-meta" role="button" tabindex="0">
      <span class="focus-indicator-main" title="当前焦点项目">⭐</span>
      <h4 class="focus-item-title" id="focus-title-{item.id}" class:completed={isCompleted}>
        {item.title}
      </h4>
      <div class="focus-item-meta">
        {#if item.due_date}
          <span class="meta-item due-date" title="截止日期">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            {formatDate(item.due_date)}
          </span>
        {/if}
        {#if item.priority}
        <span class="meta-item priority priority-{item.priority}" title="优先级: {priorityText[item.priority] || item.priority}">
           <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          {priorityText[item.priority] || item.priority}
        </span>
        {/if}
        {#if item.status}
         <span class="meta-item status status-badge-{item.status.replace('_', '-')}" title="状态: {statusText[item.status] || item.status}">
          {statusText[item.status] || item.status}
        </span>
        {/if}
      </div>
    </div>

    <div class="focus-item-actions">
      {#if !isCompleted && item.is_current_focus}
      <button
        class="action-button unfocus-button"
        on:click|stopPropagation={handleRemoveFromFocus}
        title="从当前焦点移除"
        aria-label="将 {item.title} 从当前焦点移除"
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
      >
        {#if isLoadingToggleFocus}
          <span class="spinner small-spinner"></span>
        {:else}
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="unfocus-icon"><polygon points="12 2 8.91 8.26 2 9.27 7 14.14 5.82 21.02 12 17.77 18.18 21.02 19.07 14.14 24 9.27 17.09 8.26 12 2"></polygon><line x1="2" y1="12" x2="22" y2="12"></line></svg>
        {/if}
      </button>
      {/if}
      <button
        class="action-button edit-button"
        on:click|stopPropagation={requestEdit}
        title="编辑项目"
        aria-label="编辑项目: {item.title}"
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
      </button>
      <button
        class="action-button delete-button"
        on:click|stopPropagation={handleDelete}
        title="删除项目"
        aria-label="删除项目: {item.title}"
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
</div>

<style>
  /* Styles from historical CurrentFocusDisplayItem.svelte.txt, slightly adapted */
  .focus-display-item-card {
    background-color: var(--focus-card-bg, #fffef0); 
    border: 1px solid var(--focus-card-border-color, #ffeeba);
    border-left: 5px solid var(--focus-indicator-color, #ffc107); 
    border-radius: var(--border-radius-lg, 0.5rem);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-md, 0 5px 10px rgba(0,0,0,0.08));
    transition: box-shadow 0.2s ease-in-out;
  }
  .focus-display-item-card.item-completed { /* Changed class name for clarity */
    background-color: var(--neutral-bg-alt, #f3f4f6);
    border-left-color: var(--neutral-border-strong, #d1d5db);
    opacity: 0.8;
  }
  .focus-display-item-card:hover {
    box-shadow: var(--shadow-lg, 0 8px 15px rgba(0,0,0,0.1));
  }
  .focus-indicator-main { 
    color: var(--focus-indicator-color, #ffc107);
    margin-right: 0.6em;
    font-size: 1.3em;
    line-height: 1;
  }
  .focus-item-main-info { display: flex; align-items: center; width: 100%; }
  .focus-item-checkbox-area { margin-right: 1rem; flex-shrink: 0; display: flex; align-items: center; }
  .status-checkbox { width: 20px; height: 20px; cursor: pointer; accent-color: var(--brand-primary, #2563eb); }
  .status-checkbox:disabled { cursor: not-allowed; opacity: 0.6; }
  .checkbox-label { display: none; }
  .focus-item-title-and-meta { flex-grow: 1; cursor: default; min-width: 0; }
  .focus-item-title { font-size: 1.25rem; font-weight: 600; color: var(--neutral-text-primary, #1F2937); margin: 0 0 0.3rem 0; word-break: break-word; display: inline; }
  .focus-item-title.completed { text-decoration: line-through; color: var(--neutral-text-secondary, #6B7280); }
  .focus-item-meta { display: flex; flex-wrap: wrap; gap: 0.75rem; font-size: 0.8rem; color: var(--neutral-text-muted, #9CA3AF); margin-top: 0.25rem; }
  .meta-item { display: inline-flex; align-items: center; padding: 0.2rem 0.5rem; border-radius: var(--border-radius-sm, 0.25rem); background-color: var(--neutral-bg-alt, #F3F4F6); }
  .meta-item svg { margin-right: 0.3em; opacity: 0.7; }
  
  /* Priority and Status Badge Styles (assuming these are defined in global styles or Tailwind config) */
  .priority-low { background-color: var(--priority-low-bg, #e6f4ea); color: var(--priority-low-text, #28a745); }
  .priority-medium { background-color: var(--priority-medium-bg, #fff3cd); color: var(--priority-medium-text, #ffc107); }
  .priority-high { background-color: var(--priority-high-bg, #f8d7da); color: var(--priority-high-text, #dc3545); }
  .status-badge-pending { background-color: var(--status-pending-bg, #cfe2ff); color: var(--status-pending-text, #0d6efd); }
  .status-badge-in-progress { background-color: var(--status-inprogress-bg, #fff3cd); color: var(--status-inprogress-text, #ffc107); }
  .status-badge-completed { background-color: var(--status-completed-bg, #d1e7dd); color: var(--status-completed-text, #198754); }
  .status-badge-deferred { background-color: var(--status-deferred-bg, #e2e3e5); color: var(--status-deferred-text, #6c757d); }
  /* Add .status-badge-abandoned if needed */

  .focus-item-actions { display: flex; align-items: center; margin-left: 1rem; }
  .action-button { background: none; border: none; color: var(--neutral-text-secondary, #6B7280); padding: 0.4rem; border-radius: 50%; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; transition: background-color 0.2s ease, color 0.2s ease; margin-left: 0.5rem; }
  .action-button:hover:not(:disabled) { background-color: var(--neutral-bg-hover, #E5E7EB); }
  .action-button:disabled { opacity: 0.5; cursor: not-allowed; }
  
  .unfocus-button svg.unfocus-icon { stroke: var(--focus-indicator-color, #ffc107); }
  .unfocus-button:hover:not(:disabled) { color: var(--focus-indicator-color, #ffc107); }
  .edit-button:hover:not(:disabled) { color: var(--brand-primary, #2563EB); }
  .delete-button:hover:not(:disabled) { color: var(--accent-danger, #EF4444); }

  @keyframes spin { to { transform: rotate(360deg); } }
  .spinner.small-spinner { width: 16px; height: 16px; border: 2px solid currentColor; border-top-color: transparent; border-radius: 50%; animation: spin 0.8s linear infinite; }
</style>
