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

<div class="bg-white dark:bg-gray-800 p-6 md:p-8 rounded-lg shadow-md mb-8 max-w-xl mx-auto">
  <form on:submit|preventDefault={handleSubmit}>
    <h3 class="text-2xl font-semibold text-gray-800 dark:text-gray-200 mb-6 text-center">Add New To-Do</h3>

    <div class="mb-5">
      <label for="todo-title" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
        Title <span class="text-danger-500 ml-0.5">*</span>
      </label>
      <input
        type="text"
        id="todo-title"
        bind:value={title}
        placeholder="What needs to be done?"
        required
        disabled={isLoading}
        aria-describedby="title-error"
        class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
      />
    </div>
  {/if}

    <div class="mb-5">
      <label for="todo-description" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
        Description (Optional)
      </label>
      <textarea
        id="todo-description"
        bind:value={description}
        placeholder="Add more details..."
        rows="3"
        disabled={isLoading}
        class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
      ></textarea>
    </div>

    <div class="mb-5">
      <label for="todo-due-date" class="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
        Due Date (Optional)
      </label>
      <input
        type="date"
        id="todo-due-date"
        bind:value={dueDate}
        min={getCurrentDateString()}
        disabled={isLoading}
        class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-200 dark:disabled:bg-gray-800 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
      />
    </div>

    {#if errorMessage}
      <div class="p-3 mb-5 rounded-md bg-danger-50 dark:bg-danger-900/30 text-danger-700 dark:text-danger-300 border border-danger-200 dark:border-danger-800 text-center text-sm" id="title-error" aria-live="assertive">
        <p>{errorMessage}</p>
      </div>
    {/if}

    {#if successMessage}
      <div class="p-3 mb-5 rounded-md bg-success-50 dark:bg-success-900/30 text-success-700 dark:text-success-300 border border-success-200 dark:border-success-800 text-center text-sm" aria-live="polite">
        <p>{successMessage}</p>
      </div>
    {/if}

    <button
      type="submit"
      class="w-full py-3 px-4 text-base font-semibold text-white bg-primary-500 hover:bg-primary-600 disabled:bg-gray-500 disabled:cursor-not-allowed disabled:opacity-70 rounded-md transition-colors shadow-sm hover:shadow focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
      disabled={isLoading}
    >
      {#if isLoading}
        <Icon name="loader" size="w-4 h-4" extraClass="animate-spin mr-2" />
        添加中...
      {:else}
        <Icon name="plus" size="w-4 h-4" extraClass="mr-2" />
        添加待办
      {/if}
    </button>
  </form>
</div>
