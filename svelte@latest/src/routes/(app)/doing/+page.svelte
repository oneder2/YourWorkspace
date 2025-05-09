<script lang="ts">
  import { onMount, onDestroy } from 'svelte'; // 引入 onDestroy
  import { authStore, type UserProfile } from '$lib/store/authStore';
  import { anchorStore } from '$lib/store/anchorStore';

  import TodoForm from '$lib/components/todo/TodoForm.svelte';
  import TodoList from '$lib/components/todo/TodoList.svelte';

  import FocusForm from '$lib/components/anchor/current_focus/FocusForm.svelte';
  import FocusItemComponent from '$lib/components/anchor/current_focus/FocusItem.svelte';
  import type { CurrentFocusItem } from '$lib/services/anchorService';

  let currentUser: UserProfile | null = null;
  let authUnsubscribe: () => void; // 将取消订阅函数保存到变量中

  onMount(async () => {
    authUnsubscribe = authStore.subscribe(value => { // 保存取消订阅函数
      currentUser = value.user;
    });

    if ($anchorStore.currentFocus.items.length === 0 && !$anchorStore.currentFocus.isLoading && !$anchorStore.currentFocus.error) {
      await anchorStore.loadCurrentFocusItems();
    }
    // 不再从 async onMount 返回清理函数
  });

  onDestroy(() => {
    // 在组件销毁时执行清理逻辑
    if (authUnsubscribe) {
      authUnsubscribe();
    }
  });
</script>

<div class="doing-page-container">
  <header class="page-header">
    <h1>当前进行中 (Currently Doing)</h1>
    {#if currentUser}
      <p class="welcome-message">
        欢迎回来, {currentUser.username || currentUser.email?.split('@')[0]}！在这里管理您当前的任务和焦点。
      </p>
    {/if}
  </header>

  <section id="current-focus-section" class="app-section current-focus-module">
    <h2 class="section-title">我的当前焦点</h2>
    <div class="focus-form-wrapper">
      <FocusForm />
    </div>

    <div class="focus-list-wrapper">
      {#if $anchorStore.currentFocus.isLoading && $anchorStore.currentFocus.items.length === 0}
        <div class="message loading-message">
          <p>正在加载当前焦点项目...</p>
        </div>
      {:else if $anchorStore.currentFocus.error}
        <div class="message error-message">
          <p>加载焦点项目失败: {$anchorStore.currentFocus.error}</p>
          <button on:click={() => anchorStore.loadCurrentFocusItems()} class="retry-button">重试</button>
        </div>
      {:else if $anchorStore.currentFocus.items.length === 0}
        <div class="message empty-list-message">
          <p>暂无当前焦点项目。使用上面的表单添加一个吧！</p>
        </div>
      {:else}
        <div class="focus-items-grid">
          {#each $anchorStore.currentFocus.items as focusItem (focusItem.id)}
            <FocusItemComponent item={focusItem} />
          {/each}
        </div>
      {/if}
    </div>
  </section>

  <section id="todo-section" class="app-section todo-module">
    <h2 class="section-title">我的待办清单</h2>
    <div class="todo-content">
      <div class="todo-form-wrapper">
        <TodoForm />
      </div>
      <div class="todo-list-wrapper">
        <TodoList />
      </div>
    </div>
  </section>

</div>

<style>
  .doing-page-container {
    padding: 1rem 1.5rem;
    max-width: 1100px;
    margin: 0 auto;
  }

  .page-header {
    margin-bottom: 2.5rem;
    text-align: center;
  }

  .page-header h1 {
    font-size: 2.25rem;
    color: var(--text-primary, #212529);
    margin-bottom: 0.5rem;
  }

  .welcome-message {
    font-size: 1rem;
    color: var(--text-secondary, #6c757d);
  }

  .app-section {
    margin-bottom: 3rem;
    padding: 1.5rem;
    background-color: var(--section-bg, #fff);
    border-radius: var(--border-radius-xl, 0.75rem);
    box-shadow: var(--shadow-lg, 0 8px 16px rgba(0,0,0,0.08));
  }
  
  .current-focus-module {
    background-color: var(--focus-section-bg, #f0f7ff);
  }
  .todo-module {
     background-color: var(--todo-section-bg, #f8f9fa);
  }

  .section-title {
    font-size: 1.75rem;
    color: var(--text-heading, #1a202c);
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid var(--primary-color-light, #a0cfff);
    text-align: center;
  }
  
  .focus-form-wrapper, .todo-form-wrapper {
    margin-bottom: 2rem;
  }

  .focus-items-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
    gap: 1.5rem;
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
    border: 1px solid var(--secondary-border-light, rgba(108, 117, 125, 0.1));
    padding: 2rem;
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
</style>
