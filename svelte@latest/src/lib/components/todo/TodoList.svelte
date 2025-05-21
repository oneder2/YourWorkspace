<script lang="ts">
  import { onMount } from 'svelte';
  import { todoStore } from '$lib/store/todoStore'; // Store for loading state and errors
  import type { TodoItem } from '$lib/services/todoService';
  import TodoAddDrawer from './TodoAddDrawer.svelte';
  import TodoEditDrawer from './TodoEditDrawer.svelte';

  // State for showing/hiding the add drawer
  let isAddDrawerOpen = false;

  // State for editing
  let editingTodo: TodoItem | null = null;
  let isEditDrawerOpen = false;

  // Functions to handle todo actions
  function handleToggleStatus(todo: TodoItem) {
    todoStore.toggleCompleteStatus(todo.id, todo.status);
  }

  function handleEdit(todo: TodoItem) {
    editingTodo = { ...todo };
    isEditDrawerOpen = true;
  }

  function handleEditSave(_updatedTodo: TodoItem) {
    // This will be called when the edit is successful
    isEditDrawerOpen = false;
    editingTodo = null;
  }

  function handleEditCancel() {
    isEditDrawerOpen = false;
    editingTodo = null;
  }

  function handleDelete(todo: TodoItem) {
    if (confirm(`Are you sure you want to delete "${todo.title}"?`)) {
      todoStore.removeTodo(todo.id);
    }
  }

  function handleAddTask() {
    isAddDrawerOpen = true;
  }

  function handleAddSuccess() {
    isAddDrawerOpen = false;
  }

  function handleAddCancel() {
    isAddDrawerOpen = false;
  }

  function handleSetAsFocus(todo: TodoItem) {
    if (todo.is_current_focus) {
      if (confirm(`Remove "${todo.title}" from Main Focus?`)) {
        todoStore.toggleCurrentFocus(todo.id);
      }
    } else {
      todoStore.toggleCurrentFocus(todo.id);
    }
  }

  // 接收一个待办事项数组作为 prop
  export let todos: TodoItem[] = [];
  // (可选) 接收一个列表标题，但在界面上不再显示
  export let listTitle: string = "";

  // 仍然可以从 store 获取全局加载和错误状态，特别是初次加载时
  // $: isLoading = $todoStore.isLoading;
  // $: errorMessage = $todoStore.error;
  // 但列表本身的数据来自 prop 'todos'

  onMount(async () => {
    // 初始数据加载请求应该由页面级别（例如 /doing/+page.svelte）
    // 或一个更高阶的布局组件来触发，以避免重复加载。
    // 如果这个组件需要在没有外部加载触发器的情况下独立工作，可以保留加载逻辑。
    // 但在 V3 架构中，/doing 页面会负责加载 $todoStore.loadAllTodos()。
    // 此处 onMount 可以简化或移除，除非有特定于此列表的加载需求。
    // if ($todoStore.todos.length === 0 && !$todoStore.isLoading && !$todoStore.error) {
    //   await todoStore.loadAllTodos(); // 确保数据已加载
    // }
  });
</script>

<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm">
  <div class="flex justify-center items-center mb-4">
    <button
      class="p-2 rounded-full bg-blue-100 dark:bg-blue-800 hover:bg-blue-200 dark:hover:bg-blue-700 text-blue-700 dark:text-blue-300 transition-colors shadow-sm"
      aria-label="添加待办事项"
      title="添加待办事项"
      on:click={handleAddTask}
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
    </button>
  </div>

  <TodoAddDrawer
    isOpen={isAddDrawerOpen}
    onAddSuccess={handleAddSuccess}
    onCloseRequest={handleAddCancel}
  />

  {#if editingTodo}
    <TodoEditDrawer
      todo={editingTodo}
      isOpen={isEditDrawerOpen}
      onSaveSuccess={handleEditSave}
      onCloseRequest={handleEditCancel}
    />
  {/if}

  {#if $todoStore.isLoading && todos.length === 0 && $todoStore.todos.length === 0}
    <div class="p-3 rounded-md bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800 my-2 text-center text-sm">
      <p>Loading tasks...</p>
    </div>
  {:else if $todoStore.error && todos.length === 0 && $todoStore.todos.length === 0}
    <div class="p-3 rounded-md bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800 my-2 text-center text-sm">
      <p class="mb-1">Failed to load tasks: {$todoStore.error}</p>
      <button
        on:click={() => todoStore.loadAllTodos()}
        class="px-3 py-1 text-xs font-medium text-white bg-primary-500 hover:bg-primary-600 rounded-md transition-colors"
      >
        Retry
      </button>
    </div>
  {:else if todos.length === 0}
    <div class="p-4 rounded-md bg-gray-50 dark:bg-gray-700/30 text-gray-600 dark:text-gray-400 border border-dashed border-gray-300 dark:border-gray-600 my-2 text-center text-sm">
      <p>No tasks in this list.</p>
      {#if listTitle.toLowerCase().includes("active")}
        <p class="text-xs mt-1">All tasks are completed or set as current focus!</p>
      {/if}
    </div>
  {:else}
    <ul class="space-y-2">
      {#each todos as todo (todo.id)}
        <li class="border border-blue-200 dark:border-blue-700 rounded-md p-3 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors {todo.is_current_focus ? 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-700' : ''}">
          <div class="flex items-center">
            <input
              type="checkbox"
              class="w-4 h-4 mr-3 rounded border-blue-300 text-blue-500 focus:ring-blue-500"
              checked={todo.status === 'completed'}
              on:change={() => handleToggleStatus(todo)}
            />
            <div class="flex-grow">
              <div class="flex items-center">
                <span class="font-medium text-blue-900 dark:text-blue-100 {todo.status === 'completed' ? 'line-through text-blue-500/70 dark:text-blue-400/70' : ''}">{todo.title}</span>
                {#if todo.priority === 'high'}
                  <span class="ml-2 text-xs px-1.5 py-0.5 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-full">High</span>
                {:else if todo.priority === 'medium'}
                  <span class="ml-2 text-xs px-1.5 py-0.5 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 rounded-full">Medium</span>
                {/if}
              </div>
              {#if todo.due_date}
                <p class="text-xs text-blue-600 dark:text-blue-400 mt-1">Due: {new Date(todo.due_date).toLocaleDateString()}</p>
              {/if}
            </div>
            <div class="flex space-x-1">
              <button
                class="p-1 {todo.is_current_focus ? 'text-yellow-500 hover:text-yellow-600' : 'text-gray-400 hover:text-yellow-500'} transition-colors"
                title={todo.is_current_focus ? "Remove from Main Focus" : "Set as Main Focus"}
                aria-label={todo.is_current_focus ? "Remove from Main Focus" : "Set as Main Focus"}
                on:click={() => handleSetAsFocus(todo)}
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </button>
              <button
                class="p-1 text-gray-400 hover:text-blue-500 transition-colors"
                title="Edit"
                aria-label="Edit task"
                on:click={() => handleEdit(todo)}
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
              <button
                class="p-1 text-gray-400 hover:text-red-500 transition-colors"
                title="Delete"
                aria-label="Delete task"
                on:click={() => handleDelete(todo)}
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </li>
      {/each}
    </ul>
  {/if}
</div>
