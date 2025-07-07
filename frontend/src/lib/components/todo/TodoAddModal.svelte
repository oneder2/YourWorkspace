<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { todoStore } from '$lib/store/todoStore';
  import type { CreateTodoPayload, TodoPriority } from '$lib/services/todoService';
  import type { ApiError } from '$lib/services/api';
  import Modal from '$lib/components/common/Modal.svelte';

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
      console.error('TodoAddModal handleSubmit error:', error);
    } finally {
      isLoading = false;
    }
  }

  // 处理取消
  function handleCancel() {
    resetForm();
    onCloseRequest();
  }

  // 当组件挂载时，添加ESC键监听
  onMount(() => {
    document.addEventListener('keydown', handleKeyDown);
  });

  onDestroy(() => {
    // 移除ESC键监听
    document.removeEventListener('keydown', handleKeyDown);
  });

  // 处理ESC键关闭模态窗口
  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === 'Escape' && isOpen) {
      handleCancel();
    }
  }
</script>

{#if isOpen}
  <Modal
    isOpen={isOpen}
    close={handleCancel}
    title="添加待办事项"
    modalWidth="max-w-xl"
  >
    <form id={formId} onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="todo-add-form">
      <!-- 错误消息显示 -->
      {#if errorMessage}
        <div class="mb-4 p-3 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800 rounded-md">
          {errorMessage}
        </div>
      {/if}

      <!-- 成功消息显示 -->
      {#if successMessage}
        <div class="mb-4 p-3 bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800 rounded-md">
          {successMessage}
        </div>
      {/if}

      <div class="form-group mb-4">
        <label for="add-todo-title" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
          <span class="label-text">标题</span>
          <span class="text-red-500 ml-0.5">*</span>
        </label>
        <input
          type="text"
          id="add-todo-title"
          bind:value={title}
          placeholder="输入待办事项标题"
          required
          disabled={isLoading}
          class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
        />
      </div>

      <div class="form-group mb-4">
        <label for="add-todo-description" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
          <span class="label-text">描述</span>
        </label>
        <textarea
          id="add-todo-description"
          bind:value={description}
          placeholder="添加详细描述..."
          rows="3"
          disabled={isLoading}
          class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
        ></textarea>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div class="form-group">
          <label for="add-todo-due-date" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
            <span class="label-text">截止日期</span>
          </label>
          <input
            type="date"
            id="add-todo-due-date"
            bind:value={dueDate}
            disabled={isLoading}
            class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
          />
        </div>

        <div class="form-group">
          <label for="add-todo-priority" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
            <span class="label-text">优先级</span>
          </label>
          <select
            id="add-todo-priority"
            bind:value={priority}
            disabled={isLoading}
            class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
          >
            <option value="low">低</option>
            <option value="medium">中</option>
            <option value="high">高</option>
          </select>
        </div>
      </div>

      <div class="form-group mb-6">
        <label class="flex items-center cursor-pointer">
          <input
            type="checkbox"
            bind:checked={isCurrentFocus}
            disabled={isLoading}
            class="form-checkbox h-5 w-5 text-primary-500 rounded border-gray-300 dark:border-gray-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:bg-gray-700 disabled:opacity-70 disabled:cursor-not-allowed"
          />
          <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">设为当前焦点</span>
        </label>
      </div>

      <div class="flex justify-end space-x-3">
        <button
          type="button"
          onclick={handleCancel}
          disabled={isLoading}
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-400 dark:focus:ring-gray-500 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
        >
          取消
        </button>
        <button
          type="submit"
          disabled={isLoading}
          class="px-4 py-2 bg-primary-500 text-white rounded-md hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-400 disabled:opacity-70 disabled:cursor-not-allowed transition-colors flex items-center"
        >
          {#if isLoading}
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            处理中...
          {:else}
            添加
          {/if}
        </button>
      </div>
    </form>
  </Modal>
{/if}

<!-- No need for styles as we're using Tailwind classes directly in the component -->
