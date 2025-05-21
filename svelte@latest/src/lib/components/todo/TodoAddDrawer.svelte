<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fly } from 'svelte/transition';
  import { todoStore } from '$lib/store/todoStore';
  import type { CreateTodoPayload, TodoPriority } from '$lib/services/todoService';
  import type { ApiError } from '$lib/services/api';

  // Props
  let {
    isOpen = false,
    isLoading: externalIsLoading = false,
    onAddSuccess = () => {},
    onCloseRequest = () => {}
  } = $props<{
    isOpen?: boolean;
    isLoading?: boolean;
    onAddSuccess?: () => void;
    onCloseRequest?: () => void;
  }>();

  // Use the external isLoading value
  let isLoading = $state(externalIsLoading);

  // 表单字段的本地状态
  let title = $state('');
  let description = $state('');
  let dueDate = $state('');
  let priority = $state<TodoPriority>('medium');
  let isCurrentFocus = $state(false);

  // 表单反馈的本地状态
  let errorMessage = $state('');
  let successMessage = $state('');

  // 用于表单的唯一ID
  let formId = $state(`todo-add-form-${Math.random().toString(36).substring(2)}`);

  // 当组件挂载时，添加ESC键监听
  onMount(() => {
    document.addEventListener('keydown', handleKeyDown);
  });

  onDestroy(() => {
    // 移除ESC键监听
    document.removeEventListener('keydown', handleKeyDown);
  });

  // 处理ESC键关闭抽屉
  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === 'Escape' && isOpen) {
      handleCancel();
    }
  }

  // 重置表单
  function resetForm() {
    title = '';
    description = '';
    dueDate = '';
    priority = 'medium';
    isCurrentFocus = false;
    errorMessage = '';
    successMessage = '';
  }

  // 处理表单提交
  async function handleSubmit() {
    if (!title.trim()) {
      errorMessage = '标题为必填项。';
      successMessage = '';
      return;
    }

    // 检查是否会超出最大焦点数限制 (仅当设为焦点时)
    if (isCurrentFocus) {
      const storeState = $todoStore;
      const currentFocusedCount = storeState.todos.filter(t => t.is_current_focus && t.status !== 'completed').length;
      if (currentFocusedCount >= storeState.maxFocusItems) {
        errorMessage = `最多只能将 ${storeState.maxFocusItems} 个项目设为当前焦点。请先取消其他项目的焦点状态。`;
        successMessage = '';
        return;
      }
    }

    isLoading = true;
    errorMessage = '';
    successMessage = '';

    const payload: CreateTodoPayload = {
      title: title.trim(),
      description: description.trim() || undefined,
      due_date: dueDate || undefined,
      priority
    };

    try {
      const newTodo = await todoStore.addTodo(payload);
      if (newTodo) {
        successMessage = `待办事项 "${newTodo.title}" 添加成功！`;
        resetForm();
        onAddSuccess();
      } else {
        errorMessage = $todoStore.error || '添加待办事项失败，请重试。';
      }
    } catch (error: any) {
      const apiError = error as ApiError;
      errorMessage = apiError?.message || '添加时发生意外错误。';
      console.error('TodoAddDrawer handleSubmit error:', error);
    } finally {
      isLoading = false;
    }
  }

  // 处理取消
  function handleCancel() {
    resetForm();
    onCloseRequest();
  }

  // 处理点击抽屉外部关闭
  function handleOutsideClick(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (target.classList.contains('drawer-overlay')) {
      handleCancel();
    }
  }

  function getCurrentDateString(): string {
    const today = new Date();
    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, '0');
    const day = today.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  const priorityOptions = ['low', 'medium', 'high'];
</script>

{#if isOpen}
  <!-- 抽屉遮罩层 -->
  <div
    class="drawer-overlay fixed inset-0 bg-black/30 dark:bg-black/50 z-40"
    onclick={handleOutsideClick}
    onkeydown={(e) => e.key === 'Escape' && handleCancel()}
    role="dialog"
    aria-modal="true"
    tabindex="-1"
  >
    <!-- 抽屉容器 -->
    <div
      class="drawer-container fixed top-0 right-0 h-full w-full sm:w-[450px] max-w-full bg-white dark:bg-gray-800 shadow-xl z-50 overflow-hidden flex flex-col"
      in:fly={{ x: 500, duration: 300, opacity: 1 }}
      out:fly={{ x: 500, duration: 300, opacity: 1 }}
      tabindex="-1"
      role="document"
    >
      <!-- 抽屉头部 -->
      <div class="drawer-header flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">添加待办事项</h2>
        <button
          class="bg-transparent border-none text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 cursor-pointer p-1"
          onclick={handleCancel}
          aria-label="关闭"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- 抽屉内容 -->
      <div class="drawer-content flex-grow overflow-y-auto p-4">
        <form id={formId} onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="todo-add-form">
          <div class="form-group">
            <label for="add-todo-title" class="form-label">
              <span class="label-text">标题</span>
              <span class="required-asterisk">*</span>
            </label>
            <input
              type="text"
              id="add-todo-title"
              bind:value={title}
              placeholder="输入待办事项标题"
              required
              disabled={isLoading}
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="add-todo-description" class="form-label">
              <span class="label-text">描述</span>
            </label>
            <textarea
              id="add-todo-description"
              bind:value={description}
              placeholder="添加详细描述..."
              rows="3"
              disabled={isLoading}
              class="form-input"
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group form-group-half">
              <label for="add-todo-due-date" class="form-label">
                <span class="label-text">截止日期</span>
              </label>
              <input
                type="date"
                id="add-todo-due-date"
                bind:value={dueDate}
                min={getCurrentDateString()}
                disabled={isLoading}
                class="form-input"
              />
            </div>

            <div class="form-group form-group-half">
              <label for="add-todo-priority" class="form-label">
                <span class="label-text">优先级</span>
              </label>
              <select id="add-todo-priority" bind:value={priority} disabled={isLoading} class="form-input">
                {#each priorityOptions as priorityOpt (priorityOpt)}
                  <option value={priorityOpt}>{priorityOpt.charAt(0).toUpperCase() + priorityOpt.slice(1)}</option>
                {/each}
              </select>
            </div>
          </div>

          <div class="form-group focus-toggle-container">
            <div class="focus-toggle-group">
              <input
                type="checkbox"
                id="add-todo-is-focus"
                bind:checked={isCurrentFocus}
                disabled={isLoading}
                class="focus-checkbox"
              />
              <label for="add-todo-is-focus" class="checkbox-label-inline">
                标记为当前焦点
              </label>
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

      <!-- 抽屉底部 -->
      <div class="drawer-footer p-4 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-800/80">
        <button
          type="button"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 dark:text-gray-300 dark:bg-gray-700 dark:border-gray-600 dark:hover:bg-gray-600"
          onclick={handleCancel}
          disabled={isLoading}
        >
          取消
        </button>
        <button
          type="submit"
          form={formId}
          class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600"
          disabled={isLoading}
        >
          {isLoading ? '添加中...' : '添加待办事项'}
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  /* 容器样式 */
  .todo-add-form {
    width: 100%;
  }

  /* 表单组样式 */
  .form-group {
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
