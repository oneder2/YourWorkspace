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

<div class="todo-form-container">
  <form on:submit|preventDefault={handleSubmit} class="todo-form">
    <h3 class="form-title">Add New To-Do</h3>

    <div class="form-group">
      <label for="todo-title">Title <span class="required-asterisk">*</span></label>
      <input
        type="text"
        id="todo-title"
        bind:value={title}
        placeholder="What needs to be done?"
        required
        disabled={isLoading}
        aria-describedby="title-error"
      />
    </div>

    <div class="form-group">
      <label for="todo-description">Description (Optional)</label>
      <textarea
        id="todo-description"
        bind:value={description}
        placeholder="Add more details..."
        rows="3"
        disabled={isLoading}
      ></textarea>
    </div>

    <div class="form-group">
      <label for="todo-due-date">Due Date (Optional)</label>
      <input
        type="date"
        id="todo-due-date"
        bind:value={dueDate}
        min={getCurrentDateString()}
        disabled={isLoading}
      />
    </div>

    {#if errorMessage}
      <div class="message error-message" id="title-error" aria-live="assertive">
        <p>{errorMessage}</p>
      </div>
    {/if}

    {#if successMessage}
      <div class="message success-message" aria-live="polite">
        <p>{successMessage}</p>
      </div>
    {/if}

    <button type="submit" class="submit-button" disabled={isLoading}>
      {#if isLoading}
        <span>Adding...</span>
      {:else}
        <span>Add To-Do</span>
      {/if}
    </button>
  </form>
</div>

<style>
  .todo-form-container {
    background-color: #ffffff;
    padding: 1.5rem 2rem;
    border-radius: var(--border-radius-lg, 0.5rem);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    margin-bottom: 2rem; /* Space below the form */
    max-width: 600px; /* Max width for the form */
    margin-left: auto;
    margin-right: auto;
  }

  .form-title {
    font-size: 1.5rem; /* h3 size */
    font-weight: 600;
    color: var(--text-primary, #212529);
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .todo-form .form-group {
    margin-bottom: 1.25rem;
  }

  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--text-secondary, #495057);
    font-size: 0.9rem;
  }

  .required-asterisk {
    color: var(--danger-color, #dc3545);
    margin-left: 0.2rem;
  }

  .form-group input[type="text"],
  .form-group input[type="date"],
  .form-group textarea {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid var(--border-color, #ced4da);
    border-radius: var(--border-radius, 0.375rem);
    font-size: 1rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    background-color: var(--input-bg, #f8f9fa);
    color: var(--text-primary, #212529);
  }
  
  .form-group input::placeholder,
  .form-group textarea::placeholder {
    color: var(--text-placeholder, #6c757d);
    opacity: 0.8;
  }


  .form-group input:focus,
  .form-group textarea:focus {
    border-color: var(--primary-color, #007bff);
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    outline: none;
    background-color: #fff;
  }

  .form-group input:disabled,
  .form-group textarea:disabled {
    background-color: #e9ecef;
    opacity: 0.7;
    cursor: not-allowed;
  }

  .message {
    padding: 0.75rem 1rem;
    border-radius: var(--border-radius, 0.375rem);
    margin-bottom: 1.25rem;
    text-align: center;
    font-size: 0.9rem;
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

  .submit-button {
    width: 100%;
    padding: 0.85rem 1rem;
    font-size: 1rem;
    font-weight: 600;
    color: #fff;
    background-color: var(--primary-color, #007bff);
    border: none;
    border-radius: var(--border-radius, 0.375rem);
    cursor: pointer;
    transition: background-color 0.2s ease-in-out, box-shadow 0.15s ease-in-out;
  }

  .submit-button:hover:not(:disabled) {
    background-color: #0056b3; /* Darker shade of primary */
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .submit-button:disabled {
    background-color: var(--secondary-color, #6c757d);
    cursor: not-allowed;
    opacity: 0.65;
  }
</style>
