<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import { todoStore, currentFocusTodos } from '$lib/store/todoStore'; // Gets all focus items
  import type { TodoItem as TodoItemType } from '$lib/services/todoService';
  
  // Using the corrected historical item display component
  import CurrentFocusDisplayItem from './CurrentFocusDisplayItem.svelte'; 
  import Icon from '$lib/components/common/Icon.svelte';

  // --- Props for Callbacks (to pass events up to parent) ---
  // These are called by CurrentFocusDisplayItem and propagated upwards.
  export let onEditRequest: (item: TodoItemType) => void = (item) => {
    console.warn("CurrentFocusDisplay: onEditRequest prop was not provided.", item);
  };
  export let onActionError: (detail: { message: string }) => void = (detail) => {
    console.warn("CurrentFocusDisplay: onActionError prop was not provided.", detail);
  };
   export let onFocusCleared: (itemId: number) => void = (itemId) => {
    console.warn("CurrentFocusDisplay: onFocusCleared prop was not provided.", itemId);
  };
  export let onDeleted: (itemId: number) => void = (itemId) => {
    console.warn("CurrentFocusDisplay: onDeleted prop was not provided.", itemId);
  };

  // No 'anchor' prop needed for this simple display version if $currentFocusTodos is global.
  // If $currentFocusTodos needs an anchorId to filter, this component would need an anchorId prop.
  // For now, assuming $currentFocusTodos provides all relevant focus items.

  // isLoading and error are taken directly from todoStore for general loading/error states.
</script>

<div class="current-focus-display-container p-4 bg-neutral-bg-main rounded-lg shadow">
  {#if $todoStore.isLoading && $todoStore.todos.length === 0}
    <div class="flex items-center justify-center py-6 text-neutral-text-secondary">
      <Icon name="loader" size="w-8 h-8" extraClass="animate-spin text-brand-primary" />
      <span class="ml-3 text-lg">正在加载焦点项目...</span>
    </div>
  {:else if $currentFocusTodos.length === 0}
    <div class="text-center py-8 px-4 bg-neutral-bg-alt rounded-md">
      <Icon name="info" size="w-12 h-12" extraClass="mx-auto text-neutral-text-muted mb-3" />
      <p class="text-neutral-text-primary font-medium text-lg">当前没有设置主要焦点。</p>
      <p class="text-neutral-text-secondary text-sm mt-1">
        您可以从主待办事项列表中选择一项标记为“当前焦点”！
      </p>
    </div>
  {:else}
    <div class="focus-items-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each $currentFocusTodos as focusItem (focusItem.id)}
        <div class="focus-item-wrapper">
          <CurrentFocusDisplayItem 
            item={focusItem}
            {onEditRequest}
            {onActionError}
            {onFocusCleared}
            {onDeleted}
          />
        </div>
      {/each}
    </div>
  {/if}

  {#if $todoStore.error && !$todoStore.isLoading && $currentFocusTodos.length === 0 }
    <div class="mt-6 p-4 rounded-md bg-red-50 border border-red-200 text-red-700 text-center">
      <p class="font-medium">无法加载焦点项目:</p>
      <p class="text-sm mt-1">{$todoStore.error}</p>
      </div>
  {/if}
</div>

<style>
  /* Minimal specific styles, relying on Tailwind or global styles mostly. */
  /* .focus-items-grid can have more specific styling if needed beyond Tailwind's grid. */
</style>
