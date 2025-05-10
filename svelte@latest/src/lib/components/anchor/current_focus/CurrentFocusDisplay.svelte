<script lang="ts">
  // Import the main store for isLoading/error and the specific derived store
  import { todoStore, currentFocusTodos } from '$lib/store/todoStore';
  import CurrentFocusDisplayItem from './CurrentFocusDisplayItem.svelte';
  // No need to import TodoItem type here as it's handled by CurrentFocusDisplayItem
</script>

<div class="current-focus-display-container">
  {#if $todoStore.isLoading && $todoStore.todos.length === 0}
    <div class="message info-message">
      <p>正在加载焦点项目...</p>
    </div>
  {:else if $currentFocusTodos.length === 0} <div class="message empty-focus-message">
      <p>
        当前没有设置主要焦点。
        <br />
        您可以从主待办事项列表中选择一项标记为“当前焦点”！
      </p>
    </div>
  {:else}
    <div class="focus-items-layout">
      {#each $currentFocusTodos as focusItem (focusItem.id)} <div class="focus-item-wrapper">
          <CurrentFocusDisplayItem item={focusItem} />
        </div>
      {/each}
    </div>
  {/if}

  {#if $todoStore.error && $todoStore.todos.length === 0 && !$todoStore.isLoading }
    <div class="message error-message">
      <p>无法加载项目: {$todoStore.error}</p>
    </div>
  {/if}
</div>

<style>
  /* Styles remain the same */
  .focus-items-layout {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 350px), 1fr));
    gap: 1.5rem;
  }
  .message {
    padding: 1rem 1.5rem;
    border-radius: var(--border-radius-md, 0.375rem);
    margin: 1rem auto;
    text-align: center;
    font-size: 0.95rem;
    max-width: 500px;
  }
  .info-message {
    background-color: var(--info-bg-light, rgba(23, 162, 184, 0.08));
    color: var(--info-color, #17a2b8);
    border: 1px solid var(--info-border-light, rgba(23, 162, 184, 0.15));
  }
  .empty-focus-message {
    background-color: var(--secondary-bg-light, rgba(108, 117, 125, 0.05));
    color: var(--text-muted, #6c757d);
    border: 1px dashed var(--secondary-border-light, rgba(108, 117, 125, 0.2));
    padding: 1.5rem;
    line-height: 1.6;
  }
  .error-message {
    background-color: var(--danger-bg-light, rgba(220, 53, 69, 0.08));
    color: var(--danger-color, #dc3545);
    border: 1px solid var(--danger-border-light, rgba(220, 53, 69, 0.15));
  }
</style>
