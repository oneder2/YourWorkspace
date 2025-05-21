<script lang="ts">
  import { onMount } from 'svelte';
  import { todoStore } from '$lib/store/todoStore';
  import type { TodoItem, UpdateTodoPayload, TodoStatus, TodoPriority } from '$lib/services/todoService';
  import type { ApiError } from '$lib/services/api';

  let {
    todo,
    isLoading: externalIsLoading = false,
    onSaveSuccess = (updatedTodo: TodoItem) => {},
    onCloseModalRequest = () => {}
  } = $props<{
    todo: TodoItem;
    isLoading?: boolean;
    onSaveSuccess?: (updatedTodo: TodoItem) => void;
    onCloseModalRequest?: () => void;
  }>();

  // Use the external isLoading value
  let isLoading = $state(externalIsLoading);

  // 表单字段的本地状态
  let title = $state('');
  let description = $state('');
  let dueDate = $state('');
  let status = $state<TodoStatus>('pending');
  let priority = $state<TodoPriority>('medium');
  let isCurrentFocus = $state(false); // 新增：用于编辑当前焦点状态

  // 表单反馈的本地状态
  let errorMessage = $state('');
  let successMessage = $state('');

  // We're using isLoading for both internal and external state

  // 用于表单的唯一ID
  let formId = $state(`todo-edit-form-${todo?.id || Math.random().toString(36).substring(2)}`);

  // 当组件挂载或 'todo' prop 改变时，初始化表单字段
  onMount(() => {
    initializeForm();
  });

  // 监听 'todo' prop 的变化以重新初始化表单
  $effect(() => {
    initializeForm();
  });

  // 初始化表单字段
  function initializeForm() {
    if (todo) {
      title = todo.title;
      description = todo.description || '';
      dueDate = todo.due_date || '';
      status = todo.status;
      priority = todo.priority;
      isCurrentFocus = todo.is_current_focus; // 更新 isCurrentFocus
      errorMessage = ''; // 清除之前的错误
      successMessage = '';
      formId = `todo-edit-form-${todo.id}`;
    }
  }

  // 导出 handleSubmit 以便模态框的页脚按钮可以调用
  export async function handleSubmit() {
    if (!title.trim()) {
      errorMessage = '标题为必填项。';
      successMessage = '';
      return;
    }

    // 检查是否会超出最大焦点数限制 (仅当从非焦点设为焦点时)
    if (isCurrentFocus && !todo.is_current_focus) {
        const storeState = $todoStore; // 获取当前 store 状态
        const currentFocusedCount = storeState.todos.filter(t => t.is_current_focus && t.id !== todo.id && t.status !== 'completed').length;
        if (currentFocusedCount >= storeState.maxFocusItems) {
            errorMessage = `最多只能将 ${storeState.maxFocusItems} 个项目设为当前焦点。请先取消其他项目的焦点状态。`;
            successMessage = '';
            return;
        }
    }


    isLoading = true;
    errorMessage = '';
    successMessage = '';

    const payload: UpdateTodoPayload = {
      title: title.trim(),
      description: description.trim() || null,
      due_date: dueDate || null,
      status,
      priority,
      is_current_focus: isCurrentFocus, // 包含 is_current_focus 状态
    };

    try {
      // 注意：editTodo 现在也负责处理 is_current_focus 的切换
      const updatedTodo = await todoStore.editTodo(todo.id, payload);
      if (updatedTodo) {
        successMessage = `待办事项 "${updatedTodo.title}" 更新成功！`;
        onSaveSuccess(updatedTodo);
      } else {
        errorMessage = $todoStore.error || '更新待办事项失败，请重试。';
      }
    } catch (error: any) {
      const apiError = error as ApiError;
      errorMessage = apiError?.message || '更新时发生意外错误。';
      console.error('TodoEditForm handleSubmit error:', error);
    } finally {
      isLoading = false;
    }
  }

  // 导出 handleCancel
  export function handleCancel() {
    onCloseModalRequest();
  }

  function getCurrentDateString(): string {
    const today = new Date();
    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, '0');
    const day = today.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  const statusOptions: TodoStatus[] = ['pending', 'in_progress', 'completed', 'deferred'];
  const priorityOptions: TodoPriority[] = ['low', 'medium', 'high'];

</script>

<div class="todo-edit-form-container">
  <form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="todo-edit-form" id={formId}>
    <div class="form-group">
      <label for="edit-todo-title-{todo.id}" class="form-label">
        <span class="label-text">标题</span>
        <span class="required-asterisk">*</span>
      </label>
      <input
        type="text"
        id="edit-todo-title-{todo.id}"
        bind:value={title}
        placeholder="输入待办事项标题"
        required
        disabled={isLoading}
        class="form-input"
      />
    </div>

    <div class="form-group">
      <label for="edit-todo-description-{todo.id}" class="form-label">
        <span class="label-text">描述</span>
      </label>
      <textarea
        id="edit-todo-description-{todo.id}"
        bind:value={description}
        placeholder="添加详细描述..."
        rows="3"
        disabled={isLoading}
        class="form-input"
      ></textarea>
    </div>

    <div class="form-row">
      <div class="form-group form-group-half">
        <label for="edit-todo-due-date-{todo.id}" class="form-label">
          <span class="label-text">截止日期</span>
        </label>
        <input
          type="date"
          id="edit-todo-due-date-{todo.id}"
          bind:value={dueDate}
          min={getCurrentDateString()}
          disabled={isLoading}
          class="form-input"
        />
      </div>

      <div class="form-group form-group-half">
        <label for="edit-todo-status-{todo.id}" class="form-label">
          <span class="label-text">状态</span>
        </label>
        <select id="edit-todo-status-{todo.id}" bind:value={status} disabled={isLoading} class="form-input">
          {#each statusOptions as statusOpt (statusOpt)}
            <option value={statusOpt}>{statusOpt.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</option>
          {/each}
        </select>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group form-group-half">
        <label for="edit-todo-priority-{todo.id}" class="form-label">
          <span class="label-text">优先级</span>
        </label>
        <select id="edit-todo-priority-{todo.id}" bind:value={priority} disabled={isLoading} class="form-input">
          {#each priorityOptions as priorityOpt (priorityOpt)}
            <option value={priorityOpt}>{priorityOpt.charAt(0).toUpperCase() + priorityOpt.slice(1)}</option>
          {/each}
        </select>
      </div>
      
      <div class="form-group form-group-half focus-toggle-container">
        <div class="focus-toggle-group">
          <input
            type="checkbox"
            id="edit-todo-is-focus-{todo.id}"
            bind:checked={isCurrentFocus}
            disabled={isLoading || (status === 'completed' && isCurrentFocus)}
            class="focus-checkbox"
          />
          <label for="edit-todo-is-focus-{todo.id}" class="checkbox-label-inline">
            标记为当前焦点
            {#if status === 'completed' && todo.is_current_focus}
              <small>(已完成的任务不能是当前焦点)</small>
            {/if}
          </label>
        </div>
      </div>
    </div>

    {#if errorMessage}
      <div class="message error-message" aria-live="assertive">
        <p>{errorMessage}</p>
      </div>
    {/if}

    {#if successMessage && !errorMessage}
      <div class="message success-message" aria-live="polite">
        <p>{successMessage}</p>
      </div>
    {/if}
  </form>
</div>

<style>
  /* 容器样式 */
  .todo-edit-form-container {
    padding: 0.5rem 0.75rem;
  }
  
  /* 表单组样式 */
  .todo-edit-form .form-group {
    margin-bottom: 0.75rem;
  }
  
  /* 标签样式 */
  .form-label {
    display: flex;
    align-items: center;
    margin-bottom: 0.25rem;
    font-weight: 500;
    color: var(--text-secondary, #495057);
    font-size: 0.85rem;
  }
  
  .label-text {
    margin-right: 0.2rem;
  }
  
  .required-asterisk {
    color: var(--danger-color, #dc3545);
  }
  
  /* 输入框通用样式 */
  .form-input {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--border-color, #ced4da);
    border-radius: var(--border-radius, 0.375rem);
    font-size: 0.9rem;
    transition: all 0.2s ease;
    background-color: var(--input-bg, #f8f9fa);
    color: var(--text-primary, #212529);
  }
  
  /* 输入框焦点状态 */
  .form-input:focus {
    border-color: var(--primary-color, #007bff);
    box-shadow: 0 0 0 0.15rem rgba(0, 123, 255, 0.2);
    outline: none;
    background-color: #fff;
  }
  
  /* 输入框禁用状态 */
  .form-input:disabled {
    background-color: #e9ecef;
    opacity: 0.7;
    cursor: not-allowed;
  }
  
  /* 占位符样式 */
  .form-input::placeholder {
    color: var(--text-placeholder, #6c757d);
    opacity: 0.7;
  }
  
  /* 行布局 */
  .form-row {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }
  
  .form-group-half {
    flex: 1;
  }
  
  /* 焦点切换组样式 */
  .focus-toggle-container {
    display: flex;
    align-items: center;
  }
  
  .focus-toggle-group {
    display: flex;
    align-items: center;
    padding: 0.5rem;
    background-color: var(--background-alt-light, #f8f9fa);
    border-radius: var(--border-radius-sm, 0.25rem);
    border: 1px solid var(--border-color-extra-light, #eef0f2);
    width: 100%;
    height: 38px; /* 与其他输入框高度一致 */
  }
  
  /* 复选框样式 */
  .focus-checkbox {
    margin-right: 0.5rem;
    vertical-align: middle;
    height: 1rem;
    width: 1rem;
    cursor: pointer;
  }
  
  .checkbox-label-inline {
    font-weight: normal;
    font-size: 0.85rem;
    color: var(--text-primary, #333);
    vertical-align: middle;
  }
  
  .checkbox-label-inline small {
    font-size: 0.75rem;
    color: var(--text-muted, #6c757d);
    margin-left: 0.25rem;
  }
  
  /* 消息样式 */
  .message {
    padding: 0.6rem 0.75rem;
    border-radius: var(--border-radius, 0.375rem);
    margin-top: 0.75rem;
    margin-bottom: 0.25rem;
    text-align: center;
    font-size: 0.85rem;
  }
  
  .message p {
    margin: 0;
  }
  
  .error-message {
    background-color: rgba(220, 53, 69, 0.1);
    color: var(--danger-color, #dc3545);
    border: 1px solid rgba(220, 53, 69, 0.2);
  }
  
  .success-message {
    background-color: rgba(40, 167, 69, 0.1);
    color: var(--success-color, #28a745);
    border: 1px solid rgba(40, 167, 69, 0.2);
  }
</style>
