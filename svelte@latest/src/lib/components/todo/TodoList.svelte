<script lang="ts">
  import { onMount } from 'svelte';
  import { todoStore } from '$lib/store/todoStore'; // Store 仍然用于触发加载和获取错误/加载状态
  import type { TodoItem } from '$lib/services/todoService';
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

<div class="todo-list-container">
  <h3 class="list-title">{listTitle}</h3>

  {#if $todoStore.isLoading && todos.length === 0 && $todoStore.todos.length === 0} <div class="message loading-message">
      <p>正在加载待办事项...</p>
    </div>
  {:else if $todoStore.error && todos.length === 0 && $todoStore.todos.length === 0} <div class="message error-message">
      <p>加载待办事项失败: {$todoStore.error}</p>
      <button on:click={() => todoStore.loadAllTodos()} class="retry-button">重试</button>
    </div>
  {:else if todos.length === 0}
    <div class="message empty-list-message">
      <p>这个列表里还没有待办事项。</p>
      {#if listTitle.toLowerCase().includes("活动中的任务") || listTitle.toLowerCase().includes("other active")}
        <p>所有任务都已完成，或者已设为当前焦点！</p>
      {/if}
    </div>
  {:else}
    <ul class="todo-list">
      {#each todos as todo (todo.id)} <li class="todo-list-item-wrapper">
          <TodoItemComponent {todo} />
        </li>
      {/each}
    </ul>
  {/if}
</div>

<style>
  /* 样式与之前版本基本一致，确保它们适用于通用列表展示 */
  .todo-list-container {
    background-color: var(--list-bg, #f9f9f9);
    padding: 1.5rem 2rem;
    border-radius: var(--border-radius-lg, 0.5rem);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    margin-top: 1rem; /* 减少与表单的间距，如果表单在同一section */
  }

  .list-title {
    font-size: 1.3rem; /* 调整标题大小 */
    font-weight: 600;
    color: var(--text-primary, #212529);
    margin-bottom: 1.25rem;
    text-align: left; /* 标题左对齐 */
    /* border-bottom: 1px solid var(--border-color-light, #e0e0e0); */
    /* padding-bottom: 0.75rem; */
  }

  .message {
    padding: 1rem 1.5rem;
    border-radius: var(--border-radius, 0.375rem);
    margin: 1rem 0;
    text-align: center;
    font-size: 1rem;
  }
  .message p {
    margin: 0 0 0.5rem 0;
  }

  .loading-message {
    background-color: var(--info-bg-light, rgba(23, 162, 184, 0.1));
    color: var(--info-color, #17a2b8);
    border: 1px solid var(--info-border-light, rgba(23, 162, 184, 0.2));
  }

  .error-message {
    background-color: var(--danger-bg-light, rgba(220, 53, 69, 0.1));
    color: var(--danger-color, #dc3545);
    border: 1px solid var(--danger-border-light, rgba(220, 53, 69, 0.2));
  }

  .empty-list-message {
    background-color: var(--secondary-bg-light, rgba(108, 117, 125, 0.05));
    color: var(--text-muted, #6c757d);
    border: 1px dashed var(--secondary-border-light, rgba(108, 117, 125, 0.15)); /* 改为虚线边框 */
    padding: 1.5rem;
  }
  
  .retry-button {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    color: #fff;
    background-color: var(--primary-color, #007bff);
    border: none;
    border-radius: var(--border-radius, 0.375rem);
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
    margin-top: 0.5rem;
  }

  .retry-button:hover {
    background-color: #0056b3;
  }

  .todo-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .todo-list-item-wrapper {
    margin-bottom: 0.75rem;
  }

  .todo-list-item-wrapper:last-child {
    margin-bottom: 0;
  }
</style>
