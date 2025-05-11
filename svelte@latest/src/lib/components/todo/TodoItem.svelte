<script lang="ts">
  import type { TodoItem as TodoItemType } from '$lib/services/todoService';
  import { todoStore } from '$lib/store/todoStore';
  import Icon from '$lib/components/common/Icon.svelte';

  export let todo: TodoItemType;

  // --- Callback Props ---
  export let onEditRequest: (item: TodoItemType) => void = (item) => {
    console.warn("TodoItem: onEditRequest prop was not provided.", item);
  };
  export let onDeleteRequest: (id: number) => void = (id) => {
    console.warn("TodoItem: onDeleteRequest prop was not provided.", id);
  };
  export let onActionError: (detail: { message: string }) => void = (detail) => {
    console.warn("TodoItem: onActionError prop was not provided.", detail);
  };

  // --- Component State ---
  let isLoadingToggleStatus: boolean = false;
  let isLoadingDelete: boolean = false;
  let isLoadingToggleFocus: boolean = false;

  // --- Derived State ---
  // Determine if the todo is complete based on the presence of completed_at timestamp
  $: isCompleted = !!todo.completed_at;

  // --- Event Handlers ---
  /**
   * Toggles the completion status of the todo item by calling todoStore.updateTodo.
   */
  async function toggleStatus() {
    if (!todo || typeof todo.id === 'undefined') {
      console.error('Todo item or todo.id is undefined in toggleStatus.');
      onActionError({ message: '无法更新待办事项状态：项目数据无效。' });
      return;
    }
    isLoadingToggleStatus = true;
    try {
      const newCompletedAt = isCompleted ? null : new Date().toISOString();
      await todoStore.updateTodo(todo.id, { completed_at: newCompletedAt });
      // todoStore will update the item, and reactivity will handle the UI update.
    } catch (error: any) {
      console.error('Failed to toggle todo status:', error);
      onActionError({ message: error.message || '更新状态失败。' });
    } finally {
      isLoadingToggleStatus = false;
    }
  }

  /**
   * Toggles the 'is_current_focus' status of the todo item by calling todoStore.updateTodo.
   */
  async function toggleFocus() {
    if (!todo || typeof todo.id === 'undefined') {
      console.error('Todo item or todo.id is undefined in toggleFocus.');
      onActionError({ message: '无法切换焦点状态：项目数据无效。' });
      return;
    }
    isLoadingToggleFocus = true;
    try {
      const newFocusState = !todo.is_current_focus;
      await todoStore.updateTodo(todo.id, { is_current_focus: newFocusState });
      // todoStore updates the item, UI updates reactively.
    } catch (error: any) {
      console.error('Failed to toggle todo focus:', error);
      onActionError({ message: error.message || '切换焦点失败。' });
    } finally {
      isLoadingToggleFocus = false;
    }
  }
  
  function handleEditClick() {
    if (!todo || typeof todo.id === 'undefined') {
      console.error('Todo item or todo.id is undefined in handleEditClick.');
      onActionError({ message: '无法编辑待办事项：项目数据无效。' });
      return;
    }
    onEditRequest(todo);
  }

  async function handleDeleteClick() {
    if (!todo || typeof todo.id === 'undefined') {
      console.error('Todo item or todo.id is undefined in handleDeleteClick.');
      onActionError({ message: '无法删除待办事项：项目数据无效。' });
      return;
    }
    isLoadingDelete = true;
    try {
      onDeleteRequest(todo.id);
    } catch (error: any) { 
        console.error('Error during onDeleteRequest call propagation:', error);
        onActionError({ message: '删除请求处理失败。' });
    } finally {
        isLoadingDelete = false;
    }
  }

  // --- Computed Properties for Styling ---
  $: itemClasses = `
    flex items-center justify-between p-4 rounded-xl transition-all duration-200 ease-in-out
    border
    ${isCompleted ? 'bg-neutral-bg-alt border-neutral-border-soft opacity-70' : 'bg-neutral-bg-card hover:shadow-md border-neutral-border-subtle'}
    ${todo.is_current_focus && !isCompleted ? 'ring-2 ring-accent-doing shadow-lg' : ''}
  `;

  $: titleClasses = `
    font-medium cursor-pointer group-hover:text-brand-primary transition-colors
    ${isCompleted ? 'line-through text-neutral-text-muted' : 'text-neutral-text-primary'}
  `;

  $: descriptionClasses = `
    text-sm mt-1
    ${isCompleted ? 'text-neutral-text-muted' : 'text-neutral-text-secondary'}
  `;

  $: dueDateClasses = `
    text-xs mt-2 px-2 py-0.5 rounded-full
    ${isCompleted ? 'bg-neutral-border-soft text-neutral-text-muted' : 'bg-neutral-bg-alt text-neutral-text-secondary'}
    ${todo.due_date && new Date(todo.due_date) < new Date() && !isCompleted ? 'text-red-600 bg-red-100' : ''}
  `;
</script>

<div class={itemClasses} data-todo-id={todo.id}>
  <div class="flex items-start space-x-3 flex-1 group" on:click={toggleStatus} role="button" tabindex="0" 
       on:keydown={(e) => e.key === 'Enter' || e.key === ' ' ? toggleStatus() : null}
       aria-pressed={isCompleted}
       aria-label={isCompleted ? `将 ${todo.title} 标记为未完成` : `将 ${todo.title} 标记为已完成`}>
    
    <div class="flex-shrink-0 pt-1">
      <button
        class="w-5 h-5 rounded border-2 flex items-center justify-center transition-all duration-150
              focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-brand-primary
              disabled:opacity-50 disabled:cursor-not-allowed"
        class:border-brand-primary={!isCompleted}
        class:bg-brand-primary={isCompleted}
        class:border-neutral-border-strong={isCompleted}
        disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
        aria-hidden="true" tabindex="-1"
      >
        {#if isCompleted}
          <Icon name="check" size="w-3 h-3" extraClass="text-white" />
        {/if}
      </button>
    </div>

    <div class="flex-1">
      <h4 class={titleClasses}>{todo.title}</h4>
      {#if todo.description}
        <p class={descriptionClasses}>{todo.description}</p>
      {/if}
      {#if todo.due_date}
        <span class={dueDateClasses}>
          截止: {new Date(todo.due_date).toLocaleDateString()}
        </span>
      {/if}
    </div>
  </div>

  <div class="flex items-center space-x-1.5 ml-3 flex-shrink-0">
    {#if !isCompleted}
    <button
      class="p-1.5 rounded-md text-neutral-text-secondary hover:bg-neutral-bg-hover hover:text-accent-doing focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-accent-doing disabled:opacity-50"
      on:click|stopPropagation={toggleFocus}
      title={todo.is_current_focus ? "取消当前焦点" : "设为当前焦点"}
      aria-label={todo.is_current_focus ? `从当前焦点移除 ${todo.title}` : `将 ${todo.title} 设为当前焦点`}
      disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
    >
      <Icon name={todo.is_current_focus ? "starSolid" : "starOutline"} size="w-5 h-5" />
    </button>
    {/if}
    <button
      class="p-1.5 rounded-md text-neutral-text-secondary hover:bg-neutral-bg-hover hover:text-brand-primary focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-brand-primary disabled:opacity-50"
      on:click|stopPropagation={handleEditClick}
      title="编辑待办"
      aria-label={"编辑 " + todo.title}
      disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
    >
      <Icon name="edit" size="w-5 h-5" />
    </button>
    <button
      class="p-1.5 rounded-md text-neutral-text-secondary hover:bg-neutral-bg-hover hover:text-red-500 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-red-500 disabled:opacity-50"
      on:click|stopPropagation={handleDeleteClick}
      title="删除待办"
      aria-label={"删除 " + todo.title}
      disabled={isLoadingToggleStatus || isLoadingDelete || isLoadingToggleFocus}
    >
      <Icon name="trash" size="w-5 h-5" />
    </button>
  </div>
</div>
