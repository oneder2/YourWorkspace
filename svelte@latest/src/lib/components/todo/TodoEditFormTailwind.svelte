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

  // 表单反馈的本地状态
  let errorMessage = $state('');
  let successMessage = $state('');

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
      errorMessage = ''; // 清除之前的错误
      successMessage = '';
      formId = `todo-edit-form-${todo.id}`;
    }
  }

  // 导出 handleSubmit 以便模态框的页脚按钮可以调用
  export async function handleSubmit(): Promise<boolean> {
    if (!title.trim()) {
      errorMessage = '标题为必填项。';
      successMessage = '';
      return false;
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
    };

    try {
      // 注意：editTodo 现在也负责处理 is_current_focus 的切换
      const updatedTodo = await todoStore.editTodo(todo.id, payload);
      if (updatedTodo) {
        successMessage = `待办事项 "${updatedTodo.title}" 更新成功！`;
        // 延迟调用 onSaveSuccess 以确保用户能看到成功消息
        setTimeout(() => {
          onSaveSuccess(updatedTodo);
        }, 500);
        return true;
      } else {
        // editTodo 返回 null 表示失败，不依赖 store 的 error 状态
        errorMessage = '更新待办事项失败，请重试。';
        return false;
      }
    } catch (error: any) {
      const apiError = error as ApiError;
      errorMessage = apiError?.message || '更新时发生意外错误。';
      console.error('TodoEditForm handleSubmit error:', error);
      return false;
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

  // 不再需要这些选项，因为我们直接在select中定义了选项
</script>

<form id={formId} onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="todo-edit-form">
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
    <label for="edit-todo-title-{todo.id}" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
      <span class="label-text">标题</span>
      <span class="text-red-500 ml-0.5">*</span>
    </label>
    <input
      type="text"
      id="edit-todo-title-{todo.id}"
      bind:value={title}
      placeholder="输入待办事项标题"
      required
      disabled={isLoading}
      class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
    />
  </div>

  <div class="form-group mb-4">
    <label for="edit-todo-description-{todo.id}" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
      <span class="label-text">描述</span>
    </label>
    <textarea
      id="edit-todo-description-{todo.id}"
      bind:value={description}
      placeholder="添加详细描述..."
      rows="3"
      disabled={isLoading}
      class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
    ></textarea>
  </div>

<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
    <div class="form-group">
      <label for="edit-todo-due-date-{todo.id}" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
        <span class="label-text">截止日期</span>
      </label>
      <input
        type="date"
        id="edit-todo-due-date-{todo.id}"
        bind:value={dueDate}
        min={getCurrentDateString()}
        disabled={isLoading}
        class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
      />
    </div>

    <div class="form-group">
      <label for="edit-todo-priority-{todo.id}" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
        <span class="label-text">优先级</span>
      </label>
      <select
        id="edit-todo-priority-{todo.id}"
        bind:value={priority}
        disabled={isLoading}
        class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
      >
        <option value="low">低</option>
        <option value="medium">中</option>
        <option value="high">高</option>
      </select>
    </div>

    <div class="form-group">
      <label for="edit-todo-status-{todo.id}" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
        <span class="label-text">状态</span>
      </label>
      <select
        id="edit-todo-status-{todo.id}"
        bind:value={status}
        disabled={isLoading}
        class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
      >
        <option value="pending">待处理</option>
        <option value="in_progress">进行中</option>
        <option value="completed">已完成</option>
        <option value="deferred">已延期</option>
      </select>
    </div>
  </div>
</form>
