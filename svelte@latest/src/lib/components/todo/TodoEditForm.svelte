<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';
  import { todoStore } from '$lib/store/todoStore';
  import type { TodoItem, UpdateTodoPayload, TodoStatus, TodoPriority } from '$lib/services/todoService';
  import type { ApiError } from '$lib/services/api';

  export let todo: TodoItem; // The To-Do item to be edited
  
  // Export isLoading for the parent component (Modal footer buttons) to use
  export let isLoading: boolean = false;


  const dispatch = createEventDispatcher();

  let title: string = '';
  let description: string = '';
  let dueDate: string = '';
  let status: TodoStatus = 'pending';
  let priority: TodoPriority = 'medium';

  // errorMessage and successMessage are kept internal to the form for now
  let errorMessage: string = '';
  let successMessage: string = '';

  // Unique form ID based on todo.id for the 'form' attribute on external submit button
  let formId = `todo-edit-form-${todo?.id || Math.random().toString(36).substring(2)}`;


  onMount(() => {
    if (todo) {
      title = todo.title;
      description = todo.description || '';
      dueDate = todo.due_date || '';
      status = todo.status;
      priority = todo.priority;
      formId = `todo-edit-form-${todo.id}`; // Ensure formId is set with actual todo.id
    }
  });

  $: if (todo) {
    title = todo.title;
    description = todo.description || '';
    dueDate = todo.due_date || '';
    status = todo.status;
    priority = todo.priority;
    errorMessage = '';
    successMessage = '';
    formId = `todo-edit-form-${todo.id}`; // Update formId if todo prop changes
  }

  // Export handleSubmit so it can be called from the modal's footer button
  export async function handleSubmit() {
    if (!title.trim()) {
      errorMessage = 'Title is required.';
      successMessage = ''; // Clear success message if there's a new error
      return;
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
      const updatedTodo = await todoStore.editTodo(todo.id, payload);
      if (updatedTodo) {
        successMessage = `Todo "${updatedTodo.title}" updated successfully!`;
        dispatch('saveSuccess', updatedTodo);
        // setTimeout(() => dispatch('closeModalRequest'), 1500); // Optionally close after delay
      } else {
        if (!$todoStore.error) {
            errorMessage = 'Failed to update todo. Please try again.';
        } else {
            errorMessage = $todoStore.error;
        }
      }
    } catch (error: any) {
      const apiError = error as ApiError;
      errorMessage = apiError?.message || 'An unexpected error occurred while updating.';
      console.error('TodoEditForm handleSubmit error:', error);
    } finally {
      isLoading = false;
    }
  }

  // Export handleCancel
  export function handleCancel() {
    dispatch('closeModalRequest');
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
  <form on:submit|preventDefault={handleSubmit} class="todo-edit-form" id={formId}>
    <div class="form-group">
      <label for="edit-todo-title-{todo.id}">Title <span class="required-asterisk">*</span></label>
      <input
        type="text"
        id="edit-todo-title-{todo.id}" bind:value={title}
        required
        disabled={isLoading}
      />
    </div>

    <div class="form-group">
      <label for="edit-todo-description-{todo.id}">Description</label>
      <textarea
        id="edit-todo-description-{todo.id}" bind:value={description}
        rows="4"
        disabled={isLoading}
      ></textarea>
    </div>

    <div class="form-row">
      <div class="form-group form-group-half">
        <label for="edit-todo-due-date-{todo.id}">Due Date</label>
        <input
          type="date"
          id="edit-todo-due-date-{todo.id}" bind:value={dueDate}
          min={getCurrentDateString()}
          disabled={isLoading}
        />
      </div>

      <div class="form-group form-group-half">
        <label for="edit-todo-status-{todo.id}">Status</label>
        <select id="edit-todo-status-{todo.id}" bind:value={status} disabled={isLoading}>
          {#each statusOptions as statusOpt (statusOpt)}
            <option value={statusOpt}>{statusOpt.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</option>
          {/each}
        </select>
      </div>
    </div>

    <div class="form-group">
      <label for="edit-todo-priority-{todo.id}">Priority</label>
      <select id="edit-todo-priority-{todo.id}" bind:value={priority} disabled={isLoading}>
        {#each priorityOptions as priorityOpt (priorityOpt)}
          <option value={priorityOpt}>{priorityOpt.charAt(0).toUpperCase() + priorityOpt.slice(1)}</option>
        {/each}
      </select>
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
  /* Styles remain the same as previously defined */
  .todo-edit-form-container {
    padding: 0.5rem;
  }
  .todo-edit-form .form-group { margin-bottom: 1.25rem; }
  .form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: var(--text-secondary, #495057); font-size: 0.9rem; }
  .required-asterisk { color: var(--danger-color, #dc3545); margin-left: 0.2rem; }
  .form-group input[type="text"],
  .form-group input[type="date"],
  .form-group textarea,
  .form-group select { width: 100%; padding: 0.65rem 0.9rem; border: 1px solid var(--border-color, #ced4da); border-radius: var(--border-radius, 0.375rem); font-size: 0.95rem; transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out; background-color: var(--input-bg, #f8f9fa); color: var(--text-primary, #212529); }
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
</style>
