<script lang="ts">
  import { onMount } from 'svelte';
  import { todoStore, currentFocusTodos, otherActiveTodos, completedTodos } from '$lib/store/todoStore';
  import type { TodoItem as TodoItemType } from '$lib/services/todoService';

  import CurrentFocusDisplay from '$lib/components/anchor/current_focus/CurrentFocusDisplay.svelte';
  import TodoItemComponent from '$lib/components/todo/TodoItem.svelte'; // Uses callback props now
  import TodoForm from '$lib/components/todo/TodoForm.svelte';
  import Icon from '$lib/components/common/Icon.svelte'; 
  import Modal from '$lib/components/common/Modal.svelte';
  import TodoEditForm from '$lib/components/todo/TodoEditForm.svelte';

  let showCompletedTasks: boolean = false;
  let showAddTodoForm: boolean = false;
  let isEditModalOpenGlobal: boolean = false;
  let todoToEditGlobal: TodoItemType | null = null;
  let todoEditFormGlobalComponent: TodoEditForm;

  onMount(async () => {
    if ($todoStore.todos.length === 0 && !$todoStore.isLoading) {
      await todoStore.loadAllTodos();
    }
  });

  function handleTodoAdded() {
    showAddTodoForm = false;
    console.log("Todo added successfully from page, hiding form.");
  }

  /**
   * Handles edit requests. Now receives the item directly.
   * @param {TodoItemType} item - The todo item to edit.
   */
  function handleGlobalEditRequest(item: TodoItemType) { // No longer CustomEvent
    console.log('Global Edit Request for:', item);
    if (item && typeof item === 'object' && 'id' in item) {
        todoToEditGlobal = item;
        isEditModalOpenGlobal = true;
    } else {
        console.error("Invalid item passed to handleGlobalEditRequest:", item);
        handleActionError({ message: "无法编辑该项目：数据无效。" });
    }
  }

  function closeGlobalEditModal() {
    isEditModalOpenGlobal = false;
    todoToEditGlobal = null;
  }

  function handleGlobalEditSaveSuccess(event: CustomEvent<TodoItemType>) {
    console.log('Global Edit Saved:', event.detail);
    closeGlobalEditModal();
  }

  function handleGlobalEditError(event: CustomEvent<{ message: string }>) {
    console.error('Global Edit Error:', event.detail.message);
    handleActionError({ message: `编辑失败: ${event.detail.message}` });
  }

  /**
   * Handles delete requests. Now receives the id directly.
   * @param {number} id - The ID of the todo item to delete.
   */
  async function handleDeleteRequest(id: number) { // No longer CustomEvent
    console.log('Request to delete todo in /doing page with id:', id);
    try {
      await todoStore.removeTodo(id);
    } catch (e: unknown) {
      console.error('Failed to delete todo from page:', e);
      const message = e instanceof Error ? `删除待办事项失败: ${e.message}` : `删除待办事项失败: 未知错误`;
      handleActionError({ message });
    }
  }
  
  /**
   * Handles generic action errors. Now receives the detail object directly.
   * @param {{ message: string }} detail - An object containing the error message.
   */
  function handleActionError(detail: { message: string }) { // No longer CustomEvent
    console.error('Action Error on /doing page:', detail.message);
    alert(`操作错误: ${detail.message}`);
  }
</script>

<div class="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8"> 
    <section class="lg:col-span-7 xl:col-span-8 bg-neutral-bg-card shadow-xl rounded-2xl p-6 md:p-8 flex flex-col space-y-6">
      <h2 class="text-2xl md:text-3xl font-bold text-accent-doing border-b-2 border-accent-doing/30 pb-3 mb-2">
        当前焦点
      </h2>
      <CurrentFocusDisplay
        onEditRequest={handleGlobalEditRequest} 
        onDeleteRequest={handleDeleteRequest}
        onActionError={handleActionError}
      />
    </section>

    <aside class="lg:col-span-5 xl:col-span-4 bg-neutral-bg-card shadow-xl rounded-2xl p-6 md:p-8 flex flex-col space-y-6">
      <div class="flex justify-between items-center border-b-2 border-neutral-border-soft pb-3 mb-2">
        <h2 class="text-2xl md:text-3xl font-bold text-neutral-text-primary">
          待办列表
        </h2>
        {#if !showAddTodoForm}
          <button 
            on:click={() => showAddTodoForm = true}
            class="flex items-center px-4 py-2 text-sm font-medium rounded-lg text-white bg-brand-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-1 transition-colors"
            aria-label="添加新的待办事项"
          >
            <Icon name="edit" size="w-4 h-4" extraClass="mr-2" /> 
            <span>添加</span>
          </button>
        {/if}
      </div>

      {#if showAddTodoForm}
        <div class="border-b border-neutral-border-soft pb-6 mb-6">
          <h3 class="text-lg font-semibold text-neutral-text-primary mb-3">创建新待办</h3>
          <TodoForm 
            on:addSuccess={handleTodoAdded}
            on:addError={(e) => handleActionError({message: `添加待办失败: ${e.detail.message || '未知错误'}`})}
          />
           <button 
            on:click={() => showAddTodoForm = false}
            class="mt-4 w-full flex items-center justify-center px-4 py-2 text-sm font-medium rounded-lg text-neutral-text-secondary bg-neutral-bg-alt hover:bg-neutral-border-soft focus:outline-none focus:ring-2 focus:ring-neutral-border-strong focus:ring-offset-1 transition-colors"
            aria-label="取消添加待办事项"
          >
            <span>取消</span>
          </button>
        </div>
      {/if}
      
      {#if $todoStore.isLoading && $todoStore.todos.length === 0 && !showAddTodoForm}
        <div class="text-center py-10 text-neutral-text-secondary">
          <div class="inline-block w-10 h-10 border-4 border-brand-primary border-t-transparent rounded-full animate-spin"></div>
          <p class="mt-3 text-lg">加载中...</p>
        </div>
      {:else if $todoStore.error && $todoStore.todos.length === 0 && !showAddTodoForm}
        <div class="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-center">
          <p class="font-medium">加载待办事项失败</p>
          <p class="text-sm mt-1">{$todoStore.error}</p>
          <button 
            on:click={() => todoStore.loadAllTodos()} 
            class="mt-3 px-4 py-2 text-sm font-medium bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
          >
            重试
          </button>
        </div>
      {/if}

      {#if !showAddTodoForm}
        <div class="flex-grow flex flex-col space-y-4 overflow-y-auto pr-2 -mr-2 custom-scrollbar">
          {#if !showCompletedTasks}
            <div>
              <h3 class="text-xl font-semibold text-neutral-text-secondary mb-4">活动中的任务</h3>
              {#if $otherActiveTodos.length > 0}
                <ul class="space-y-4">
                  {#each $otherActiveTodos as todo (todo.id)}
                    <li>
                      <TodoItemComponent 
                        {todo} 
                        onEditRequest={handleGlobalEditRequest}
                        onDeleteRequest={handleDeleteRequest}
                        onActionError={handleActionError}
                      />
                    </li>
                  {/each}
                </ul>
              {:else if !($todoStore.isLoading && $todoStore.todos.length === 0)}
                <p class="text-center text-neutral-text-muted py-6 px-4 border border-dashed border-neutral-border-soft rounded-lg">
                  太棒了! <br/> 没有其他活动中的任务了。
                </p>
              {/if}
            </div>
          {/if}

          {#if showCompletedTasks}
            <div>
              <h3 class="text-xl font-semibold text-neutral-text-secondary mb-4">已完成的任务</h3>
              {#if $completedTodos.length > 0}
                <ul class="space-y-4">
                  {#each $completedTodos as todo (todo.id)}
                    <li>
                       <TodoItemComponent 
                        {todo} 
                        onEditRequest={handleGlobalEditRequest}
                        onDeleteRequest={handleDeleteRequest}
                        onActionError={handleActionError}
                      />
                    </li>
                  {/each}
                </ul>
              {:else if !($todoStore.isLoading && $todoStore.todos.length === 0)}
                <p class="text-center text-neutral-text-muted py-6">还没有已完成的任务。</p>
              {/if}
            </div>
          {/if}
        </div>
      {/if}

      {#if ($completedTodos.length > 0 || showCompletedTasks) && !showAddTodoForm}
        <div class="mt-auto pt-4 border-t border-neutral-border-soft">
          <button
            on:click={() => showCompletedTasks = !showCompletedTasks}
            class="w-full py-3 px-4 text-sm font-medium rounded-lg transition-colors
                  bg-neutral-bg-alt text-neutral-text-primary hover:bg-neutral-border-soft
                  focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-1"
          >
            {showCompletedTasks ? '显示活动中的任务' : `显示已完成的任务 (${$completedTodos.length})`}
          </button>
        </div>
      {/if}
    </aside>
</div>

{#if isEditModalOpenGlobal && todoToEditGlobal}
  <Modal
    isOpen={isEditModalOpenGlobal}
    title="编辑待办: {todoToEditGlobal.title}"
    on:close={closeGlobalEditModal}
    modalWidth="max-w-xl"
  >
    <TodoEditForm
      bind:this={todoEditFormGlobalComponent}
      todo={todoToEditGlobal}
      on:saveSuccess={handleGlobalEditSaveSuccess}
      on:saveError={handleGlobalEditError} 
      on:closeModalRequest={closeGlobalEditModal}
    />
    <div slot="footer" class="flex justify-end space-x-3 p-4 bg-neutral-bg-alt rounded-b-lg border-t border-neutral-border-soft">
      <button 
        type="button" 
        class="px-4 py-2 text-sm font-medium rounded-md border border-neutral-border-strong text-neutral-text-primary hover:bg-neutral-bg-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-primary disabled:opacity-50"
        on:click={() => todoEditFormGlobalComponent?.handleCancel()} 
        disabled={todoEditFormGlobalComponent?.isLoading}
      >
        取消
      </button>
      <button 
        type="submit" 
        class="px-4 py-2 text-sm font-medium rounded-md text-white bg-brand-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-primary disabled:opacity-50 disabled:bg-neutral-text-muted"
        on:click={() => todoEditFormGlobalComponent?.handleSubmit()} 
        disabled={todoEditFormGlobalComponent?.isLoading}
        form="todo-edit-form-{todoToEditGlobal.id}" 
      >
        {#if todoEditFormGlobalComponent?.isLoading}
          <span class="flex items-center">
            <div class="w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            保存中...
          </span>
        {:else}
          保存更改
        {/if}
      </button>
    </div>
  </Modal>
{/if}

<style>
  .custom-scrollbar::-webkit-scrollbar {
    width: 8px;
  }
  .custom-scrollbar::-webkit-scrollbar-track {
    background: theme('colors.neutral-bg-alt');
    border-radius: 10px;
  }
  .custom-scrollbar::-webkit-scrollbar-thumb {
    background: theme('colors.neutral-border-soft');
    border-radius: 10px;
  }
  .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: theme('colors.neutral-border-strong');
  }
</style>
