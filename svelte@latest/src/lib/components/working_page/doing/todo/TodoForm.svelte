<script lang="ts">
  import { todoStore } from '$lib/store/todoStore';
  // Corrected import for CreateTodoPayload from todoService.ts
  import type { CreateTodoPayload } from '$lib/services/todoService';
  import type { ApiError } from '$lib/services/api';

  let title: string = '';
  let description: string = '';
  let dueDate: string = ''; // Format: YYYY-MM-DD

  let isLoading: boolean = false;
  let errorMessage: string = '';
  let successMessage: string = '';

  async function handleSubmit() {
    if (!title.trim()) {
      errorMessage = 'Title is required.';
      return;
    }

    isLoading = true;
    errorMessage = '';
    successMessage = '';

    const payload: CreateTodoPayload = {
      title: title.trim(),
    };

    if (description.trim()) {
      payload.description = description.trim();
    }
    if (dueDate) {
      payload.due_date = dueDate;
    }

    try {
      const newTodo = await todoStore.addTodo(payload);
      if (newTodo) {
        successMessage = `Todo "${newTodo.title}" added successfully!`;
        title = '';
        description = '';
        dueDate = '';
        setTimeout(() => successMessage = '', 3000);
      } else {
        if (!$todoStore.error) {
            errorMessage = 'Failed to add todo. Please try again.';
        } else {
            errorMessage = $todoStore.error;
        }
      }
    } catch (error: any) {
      const apiError = error as ApiError;
      errorMessage = apiError?.message || 'An unexpected error occurred.';
      console.error('TodoForm handleSubmit error:', error);
    } finally {
      isLoading = false;
    }
  }

  function getCurrentDateString(): string {
    const today = new Date();
    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, '0');
    const day = today.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
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
        <span>Adding...</span>
      {:else}
        <span>Add To-Do</span>
      {/if}
    </button>
  </form>
</div>
