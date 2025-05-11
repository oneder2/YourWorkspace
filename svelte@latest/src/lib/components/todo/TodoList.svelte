<script lang="ts">
  import { onMount } from 'svelte';
  import { todoStore } from '$lib/store/todoStore'; // Store for loading state and errors
  import type { TodoItem } from '$lib/services/todoService';
  import { fade, fly } from 'svelte/transition';

  // Functions to handle todo actions
  function handleToggleStatus(todo: TodoItem) {
    todoStore.toggleCompleteStatus(todo.id, todo.status);
  }

  function handleEdit(todo: TodoItem) {
    alert(`Edit functionality will be implemented for: ${todo.title}`);
  }

  function handleDelete(todo: TodoItem) {
    if (confirm(`Are you sure you want to delete "${todo.title}"?`)) {
      todoStore.removeTodo(todo.id);
    }
  }

  function handleAddTask() {
    alert("Add task functionality will be implemented here");
  }

  // 新增：接收一个待办事项数组作为 prop
  export let todos: TodoItem[] = [];
  // (可选) 接收一个列表标题
  export let listTitle: string = "待办事项"; // Default title

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
  <div class="flex justify-between items-center mb-4">
    <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">{listTitle}</h3>
    <button
      class="p-1 rounded-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 transition-colors"
      aria-label="Add new task"
      on:click={handleAddTask}
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
    </button>
  </div>

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
        <li class="border border-gray-200 dark:border-gray-700 rounded-md p-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
          <div class="flex items-center">
            <input
              type="checkbox"
              class="w-4 h-4 mr-3 rounded border-gray-300 text-primary-500 focus:ring-primary-500"
              checked={todo.status === 'completed'}
              on:change={() => handleToggleStatus(todo)}
            />
            <div class="flex-grow">
              <div class="flex items-center">
                <span class="font-medium text-gray-900 dark:text-gray-100 {todo.status === 'completed' ? 'line-through text-gray-500 dark:text-gray-400' : ''}">{todo.title}</span>
                {#if todo.priority === 'high'}
                  <span class="ml-2 text-xs text-red-500">High Priority</span>
                {/if}
              </div>
              {#if todo.due_date}
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Due: {new Date(todo.due_date).toLocaleDateString()}</p>
              {/if}
            </div>
            <div class="flex space-x-1">
              <button
                class="p-1 text-gray-400 hover:text-primary-500 transition-colors"
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
