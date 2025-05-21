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
      <label for="edit-todo-title-{todo.id}">标题 <span class="required-asterisk">*</span></label>
      <input
        type="text"
        id="edit-todo-title-{todo.id}"
        bind:value={title}
        required
        disabled={isLoading}
      />
    </div>

    <div class="form-group">
      <label for="edit-todo-description-{todo.id}">描述</label>
      <textarea
        id="edit-todo-description-{todo.id}"
        bind:value={description}
        rows="4"
        disabled={isLoading}
      ></textarea>
    </div>

    <div class="form-row">
      <div class="form-group form-group-half">
        <label for="edit-todo-due-date-{todo.id}">截止日期</label>
        <input
          type="date"
          id="edit-todo-due-date-{todo.id}"
          bind:value={dueDate}
          min={getCurrentDateString()}
          disabled={isLoading}
        />
      </div>

      <div class="form-group form-group-half">
        <label for="edit-todo-status-{todo.id}">状态</label>
        <select id="edit-todo-status-{todo.id}" bind:value={status} disabled={isLoading}>
          {#each statusOptions as statusOpt (statusOpt)}
            <option value={statusOpt}>{statusOpt.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</option>
          {/each}
        </select>
      </div>
    </div>

    <div class="form-group">
      <label for="edit-todo-priority-{todo.id}">优先级</label>
      <select id="edit-todo-priority-{todo.id}" bind:value={priority} disabled={isLoading}>
        {#each priorityOptions as priorityOpt (priorityOpt)}
          <option value={priorityOpt}>{priorityOpt.charAt(0).toUpperCase() + priorityOpt.slice(1)}</option>
        {/each}
      </select>
    </div>

    <div class="form-group focus-toggle-group">
      <input
        type="checkbox"
        id="edit-todo-is-focus-{todo.id}"
        bind:checked={isCurrentFocus}
        disabled={isLoading || (status === 'completed' && isCurrentFocus)}
      />
      <label for="edit-todo-is-focus-{todo.id}" class="checkbox-label-inline">
        标记为当前焦点
        {#if status === 'completed' && todo.is_current_focus}
          <small>(已完成的任务不能是当前焦点)</small>
        {/if}
      </label>
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
  .todo-edit-form-container { padding: 0.5rem; }
  .todo-edit-form .form-group { margin-bottom: 1.25rem; }
  .form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: var(--text-secondary, #495057); font-size: 0.9rem; }
  .required-asterisk { color: var(--danger-color, #dc3545); margin-left: 0.2rem; }
  .form-group input[type="text"],
  .form-group input[type="date"],
  .form-group input[type="checkbox"], /* 为复选框添加基础样式 */
  .form-group textarea,
  .form-group select {
    width: 100%;
    padding: 0.65rem 0.9rem;
    border: 1px solid var(--border-color, #ced4da);
    border-radius: var(--border-radius, 0.375rem);
    font-size: 0.95rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    background-color: var(--input-bg, #f8f9fa);
    color: var(--text-primary, #212529);
  }
  .form-group input[type="checkbox"] { /* 复选框特定样式调整 */
    width: auto; /* 不要占满整行 */
    margin-right: 0.5rem;
    vertical-align: middle;
    height: 1.1em; /* 调整大小 */
    width: 1.1em;
  }
  .checkbox-label-inline {
    font-weight: normal;
    font-size: 0.95rem;
    color: var(--text-primary, #333);
    vertical-align: middle;
  }
  .checkbox-label-inline small {
    font-size: 0.8em;
    color: var(--text-muted);
  }

  .form-group input::placeholder,
  .form-group textarea::placeholder { color: var(--text-placeholder, #6c757d); opacity: 0.8; }
  .form-group input:focus,
  .form-group textarea:focus,
  .form-group select:focus { border-color: var(--primary-color, #007bff); box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25); outline: none; background-color: #fff; }
  .form-group input:disabled,
  .form-group textarea:disabled,
  .form-group select:disabled { background-color: #e9ecef; opacity: 0.7; cursor: not-allowed; }
  .form-row { display: flex; gap: 1rem; margin-bottom: 1.25rem; }
  .form-group-half { flex: 1; }
  .message { padding: 0.75rem 1rem; border-radius: var(--border-radius, 0.375rem); margin-top: 1rem; margin-bottom: 0.5rem; text-align: center; font-size: 0.9rem; }
  .message p { margin: 0; }
  .error-message { background-color: rgba(220, 53, 69, 0.1); color: var(--danger-color, #dc3545); border: 1px solid rgba(220, 53, 69, 0.2); }
  .success-message { background-color: rgba(40, 167, 69, 0.1); color: var(--success-color, #28a745); border: 1px solid rgba(40, 167, 69, 0.2); }
  .focus-toggle-group { /* “标记为当前焦点”复选框组的样式 */
    display: flex;
    align-items: center;
    padding: 0.5rem;
    background-color: var(--background-alt-light, #f8f9fa); /* 轻微背景 */
    border-radius: var(--border-radius-sm, 0.25rem);
    border: 1px solid var(--border-color-extra-light, #eef0f2);
  }
</style>
