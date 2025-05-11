<script lang="ts">
  import { onMount, tick } from 'svelte';
  // Correctly import UpdateTodoPayload instead of TodoPayload
  import type { TodoItem, UpdateTodoPayload } from '$lib/services/todoService'; 
  import { todoStore } from '$lib/store/todoStore';
  import Icon from '$lib/components/common/Icon.svelte';

  // --- Props ---
  export let todo: TodoItem;

  // --- Callback Props ---
  export let onSaveSuccess: (updatedTodo: TodoItem) => void = (updatedTodo) => {
    console.warn("TodoEditForm: onSaveSuccess prop was not provided.", updatedTodo);
  };
  export let onSaveError: (errorDetail: { message: string }) => void = (errorDetail) => {
    console.warn("TodoEditForm: onSaveError prop was not provided.", errorDetail);
  };
  export let onCloseModalRequest: () => void = () => {
    console.warn("TodoEditForm: onCloseModalRequest prop was not provided.");
  };

  // --- Component State ---
  let formTitle: string = '';
  let formDescription: string = '';
  let formDueDate: string = ''; // Store as YYYY-MM-DD string
  let formCompleted: boolean = false; // UI state for the checkbox

  export let isLoading: boolean = false;
  let errorMessage: string = '';
  // successMessage is less relevant here as modal usually closes on success

  // --- Lifecycle ---
  onMount(() => {
    if (todo) {
      formTitle = todo.title;
      formDescription = todo.description || '';
      formDueDate = todo.due_date ? new Date(todo.due_date).toISOString().split('T')[0] : '';
      // Correctly initialize formCompleted based on todo.completed_at
      formCompleted = !!todo.completed_at; 
    }
  });

  // --- Event Handlers ---
  export async function handleSubmit() {
    if (!formTitle.trim()) {
      errorMessage = '标题不能为空。';
      setTimeout(() => errorMessage = '', 3000);
      return;
    }

    isLoading = true;
    errorMessage = '';

    // Construct the payload for updating the todo item
    // Use UpdateTodoPayload for the base, then add specific fields like completed_at
    const payload: Partial<UpdateTodoPayload & { completed_at?: string | null, is_current_focus?: boolean }> = {
      title: formTitle.trim(),
      description: formDescription.trim() || undefined, // Send undefined for empty to potentially clear
      due_date: formDueDate || undefined, // Send undefined for empty to potentially clear
      // is_current_focus is not typically edited here, but can be added if needed.
    };

    // Handle completed_at based on formCompleted state
    if (formCompleted) {
      // If marking as complete, and it wasn't already, set new timestamp.
      // If it was already complete, we can send the existing timestamp or let backend handle it.
      // For simplicity, if formCompleted is true, ensure completed_at is a timestamp.
      payload.completed_at = todo.completed_at || new Date().toISOString();
    } else {
      // If marking as incomplete, completed_at should be null.
      payload.completed_at = null;
    }
    
    // Only include fields in the payload if they have changed from the original todo item,
    // or if the backend API expects all fields or handles partial updates gracefully.
    // For this example, we are sending fields that might have been edited.
    // A more sophisticated approach would be to only send changed fields.

    try {
      const updatedTodo = await todoStore.updateTodo(todo.id, payload as UpdateTodoPayload); // Cast if needed
      if (updatedTodo) {
        onSaveSuccess(updatedTodo); 
      } else {
        // This path might be hit if updateTodo returns null on non-exception failure
        errorMessage = '更新待办事项失败，未收到有效的响应。';
        onSaveError({ message: errorMessage });
        setTimeout(() => errorMessage = '', 3000);
      }
    } catch (error: unknown) {
      console.error('Failed to update todo:', error);
      const msg = error instanceof Error ? error.message : '更新待办事项时发生未知错误。';
      errorMessage = `更新失败: ${msg}`;
      onSaveError({ message: errorMessage });
      setTimeout(() => errorMessage = '', 3000);
    } finally {
      isLoading = false;
    }
  }

  export function handleCancel() {
    onCloseModalRequest();
  }

  let titleInput: HTMLInputElement;
  onMount(async () => {
    await tick(); 
    titleInput?.focus();
  });

</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-4 p-1" id="todo-edit-form-{todo?.id}">
  <div>
    <label for="edit-todo-title-{todo?.id}" class="block text-sm font-medium text-neutral-text-primary mb-1">
      标题 <span class="text-red-500">*</span>
    </label>
    <input
      bind:this={titleInput}
      type="text"
      id="edit-todo-title-{todo?.id}"
      bind:value={formTitle}
      required
      placeholder="例如：完成项目报告"
      class="w-full px-3 py-2 border border-neutral-border-strong rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary transition-colors disabled:bg-neutral-bg-alt"
      disabled={isLoading}
    />
  </div>

  <div>
    <label for="edit-todo-description-{todo?.id}" class="block text-sm font-medium text-neutral-text-primary mb-1">
      描述 (可选)
    </label>
    <textarea
      id="edit-todo-description-{todo?.id}"
      bind:value={formDescription}
      rows="4"
      placeholder="例如：包含所有关键发现和建议..."
      class="w-full px-3 py-2 border border-neutral-border-strong rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary transition-colors disabled:bg-neutral-bg-alt"
      disabled={isLoading}
    ></textarea>
  </div>

  <div>
    <label for="edit-todo-due-date-{todo?.id}" class="block text-sm font-medium text-neutral-text-primary mb-1">
      截止日期 (可选)
    </label>
    <input
      type="date"
      id="edit-todo-due-date-{todo?.id}"
      bind:value={formDueDate}
      class="w-full px-3 py-2 border border-neutral-border-strong rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary transition-colors disabled:bg-neutral-bg-alt"
      disabled={isLoading}
    />
  </div>
  
  <div class="flex items-center">
    <input
      type="checkbox"
      id="edit-todo-completed-{todo?.id}"
      bind:checked={formCompleted} class="h-4 w-4 text-brand-primary border-neutral-border-strong rounded focus:ring-brand-primary disabled:opacity-70"
      disabled={isLoading}
    />
    <label for="edit-todo-completed-{todo?.id}" class="ml-2 block text-sm text-neutral-text-primary">
      已完成
    </label>
  </div>

  {#if errorMessage}
    <div class="my-3 p-3 rounded-md bg-red-50 border border-red-200 text-sm text-red-700" role="alert">
      {errorMessage}
    </div>
  {/if}
</form>
