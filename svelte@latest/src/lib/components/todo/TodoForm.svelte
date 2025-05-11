<script lang="ts">
  import { todoStore } from '$lib/store/todoStore';
  // Correctly import CreateTodoPayload instead of TodoPayload
  import type { TodoItem, CreateTodoPayload } from '$lib/services/todoService'; 
  import Icon from '$lib/components/common/Icon.svelte';

  // --- Callback Props ---
  export let onAddSuccess: (newTodo: TodoItem) => void = (newTodo) => {
    console.warn("TodoForm: onAddSuccess prop was not provided.", newTodo);
  };
  export let onAddError: (errorDetail: { message: string }) => void = (errorDetail) => {
    console.warn("TodoForm: onAddError prop was not provided.", errorDetail);
  };

  // --- Component State ---
  let title: string = '';
  let description: string = '';
  let dueDate: string = ''; // Store as YYYY-MM-DD string from input
  let isLoading: boolean = false;
  let errorMessage: string = '';
  let successMessage: string = '';

  // --- Event Handlers ---
  async function handleSubmit() {
    if (!title.trim()) {
      errorMessage = '标题不能为空。';
      setTimeout(() => errorMessage = '', 3000);
      return;
    }

    isLoading = true;
    errorMessage = '';
    successMessage = '';

    // Use CreateTodoPayload for the payload type
    const payload: CreateTodoPayload = {
      title: title.trim(),
      description: description.trim() || undefined, // Send undefined if empty, service might handle as null
      due_date: dueDate || undefined, // Send undefined if empty, service might handle as null
      // completed_at and is_current_focus are typically not set at creation by the client;
      // backend defaults them (e.g., completed_at=null, is_current_focus=false).
      // CreateTodoPayload should reflect fields required/allowed at creation.
    };

    try {
      const newTodo = await todoStore.addTodo(payload);
      if (newTodo) {
        successMessage = `待办事项 "${newTodo.title}" 已成功添加!`;
        onAddSuccess(newTodo);
        title = '';
        description = '';
        dueDate = '';
        setTimeout(() => successMessage = '', 3000);
      } else {
        errorMessage = '添加待办事项失败，未收到有效的响应。';
        onAddError({ message: errorMessage });
        setTimeout(() => errorMessage = '', 3000);
      }
    } catch (error: unknown) {
      console.error('Failed to add todo:', error);
      const msg = error instanceof Error ? error.message : '添加待办事项时发生未知错误。';
      errorMessage = `添加失败: ${msg}`;
      onAddError({ message: errorMessage });
      setTimeout(() => errorMessage = '', 3000);
    } finally {
      isLoading = false;
    }
  }

  function handleClearForm() {
    title = '';
    description = '';
    dueDate = '';
    errorMessage = '';
    successMessage = '';
  }
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-4">
  <div>
    <label for="todo-title" class="block text-sm font-medium text-neutral-text-primary mb-1">
      标题 <span class="text-red-500">*</span>
    </label>
    <input
      type="text"
      id="todo-title"
      bind:value={title}
      required
      placeholder="例如：完成项目报告"
      class="w-full px-3 py-2 border border-neutral-border-strong rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary transition-colors disabled:bg-neutral-bg-alt"
      disabled={isLoading}
    />
  </div>

  <div>
    <label for="todo-description" class="block text-sm font-medium text-neutral-text-primary mb-1">
      描述 (可选)
    </label>
    <textarea
      id="todo-description"
      bind:value={description}
      rows="3"
      placeholder="例如：包含所有关键发现和建议..."
      class="w-full px-3 py-2 border border-neutral-border-strong rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary transition-colors disabled:bg-neutral-bg-alt"
      disabled={isLoading}
    ></textarea>
  </div>

  <div>
    <label for="todo-due-date" class="block text-sm font-medium text-neutral-text-primary mb-1">
      截止日期 (可选)
    </label>
    <input
      type="date"
      id="todo-due-date"
      bind:value={dueDate}
      class="w-full px-3 py-2 border border-neutral-border-strong rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary transition-colors disabled:bg-neutral-bg-alt"
      disabled={isLoading}
    />
  </div>

  {#if successMessage}
    <div class="p-3 rounded-md bg-green-50 border border-green-200 text-sm text-green-700 transition-opacity duration-300" role="alert">
      {successMessage}
    </div>
  {/if}

  {#if errorMessage}
    <div class="p-3 rounded-md bg-red-50 border border-red-200 text-sm text-red-700 transition-opacity duration-300" role="alert">
      {errorMessage}
    </div>
  {/if}

  <div class="flex items-center justify-end space-x-3 pt-2">
    <button
      type="button"
      on:click={handleClearForm}
      disabled={isLoading}
      class="px-4 py-2 text-sm font-medium rounded-lg border border-neutral-border-strong text-neutral-text-primary hover:bg-neutral-bg-hover focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-neutral-border-strong transition-colors disabled:opacity-60"
    >
      清空
    </button>
    <button
      type="submit"
      disabled={isLoading || !title.trim()}
      class="px-4 py-2 text-sm font-medium rounded-lg text-white bg-brand-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-brand-primary transition-colors disabled:opacity-60 disabled:bg-neutral-text-muted flex items-center"
    >
      {#if isLoading}
        <Icon name="loader" size="w-4 h-4" extraClass="animate-spin mr-2" />
        添加中...
      {:else}
        <Icon name="plus" size="w-4 h-4" extraClass="mr-2" />
        添加待办
      {/if}
    </button>
  </div>
</form>
