<script lang="ts">
  import { onMount } from 'svelte';
  import { todoStore } from '$lib/store/todoStore'; // Store 仍然用于触发加载和获取错误/加载状态
  import type { TodoItem } from '$lib/services/todoService';
  // Import the TodoItem component directly
  import TodoItemComponent from './TodoItem.svelte';

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

<div class="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg shadow-sm mt-4">
  <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-5">{listTitle}</h3>

  {#if $todoStore.isLoading && todos.length === 0 && $todoStore.todos.length === 0}
    <div class="p-4 rounded-md bg-info-50 dark:bg-info-900/30 text-info-700 dark:text-info-300 border border-info-200 dark:border-info-800 my-4 text-center">
      <p class="mb-2">正在加载待办事项...</p>
    </div>
  {:else if $todoStore.error && todos.length === 0 && $todoStore.todos.length === 0}
    <div class="p-4 rounded-md bg-danger-50 dark:bg-danger-900/30 text-danger-700 dark:text-danger-300 border border-danger-200 dark:border-danger-800 my-4 text-center">
      <p class="mb-2">加载待办事项失败: {$todoStore.error}</p>
      <button
        on:click={() => todoStore.loadAllTodos()}
        class="px-4 py-2 text-sm font-medium text-white bg-primary-500 hover:bg-primary-600 rounded-md transition-colors mt-2"
      >
        重试
      </button>
    </div>
  {:else if todos.length === 0}
    <div class="p-6 rounded-md bg-gray-100 dark:bg-gray-700/30 text-gray-600 dark:text-gray-400 border border-dashed border-gray-300 dark:border-gray-600 my-4 text-center">
      <p class="mb-2">这个列表里还没有待办事项。</p>
      {#if listTitle.toLowerCase().includes("活动中的任务") || listTitle.toLowerCase().includes("other active")}
        <p>所有任务都已完成，或者已设为当前焦点！</p>
      {/if}
    </div>
  {:else}
    <ul class="space-y-3">
      {#each todos as todo (todo.id)}
        <li>
          <TodoItemComponent {todo} />
        </li>
      {/each}
    </ul>
  {/if}
</div>
