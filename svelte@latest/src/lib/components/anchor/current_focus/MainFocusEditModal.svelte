<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import type { TodoItem } from '$lib/services/todoService';
  import Modal from '$lib/components/common/Modal.svelte';
  import TodoEditFormTailwind from '$lib/components/todo/TodoEditFormTailwind.svelte';

  // Props
  let {
    todo,
    isOpen = false,
    isLoading: externalIsLoading = false,
    onSaveSuccess = (updatedTodo: TodoItem) => {},
    onCloseRequest = () => {}
  } = $props<{
    todo: TodoItem;
    isOpen?: boolean;
    isLoading?: boolean;
    onSaveSuccess?: (updatedTodo: TodoItem) => void;
    onCloseRequest?: () => void;
  }>();

  // Use the external isLoading value
  let isLoading = $state(externalIsLoading);

  // 表单引用
  let formComponent = $state<{ handleSubmit: () => Promise<void>, handleCancel: () => void } | null>(null);

  // 处理表单提交
  async function handleSubmit() {
    if (formComponent) {
      await formComponent.handleSubmit();
    }
  }

  // 处理取消
  function handleCancel() {
    onCloseRequest();
  }

  // 当组件挂载时，添加ESC键监听
  onMount(() => {
    document.addEventListener('keydown', handleKeyDown);
  });

  onDestroy(() => {
    // 移除ESC键监听
    document.removeEventListener('keydown', handleKeyDown);
  });

  // 处理ESC键关闭模态窗口
  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === 'Escape' && isOpen) {
      handleCancel();
    }
  }
</script>

{#if isOpen && todo}
  <Modal
    isOpen={isOpen}
    close={handleCancel}
    title="编辑主要焦点项目"
    modalWidth="max-w-xl"
  >
    <TodoEditFormTailwind
      bind:this={formComponent}
      {todo}
      isLoading={isLoading}
      onSaveSuccess={onSaveSuccess}
      onCloseModalRequest={handleCancel}
    />

    <svelte:fragment slot="footer">
      <div class="flex justify-end space-x-3 p-4 border-t border-gray-200 dark:border-gray-700">
        <button
          type="button"
          onclick={handleCancel}
          disabled={isLoading}
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-400 dark:focus:ring-gray-500 disabled:opacity-70 disabled:cursor-not-allowed transition-colors"
        >
          取消
        </button>
        <button
          type="button"
          onclick={handleSubmit}
          disabled={isLoading}
          class="px-4 py-2 bg-amber-600 text-white rounded-md hover:bg-amber-700 focus:outline-none focus:ring-2 focus:ring-amber-400 disabled:opacity-70 disabled:cursor-not-allowed transition-colors flex items-center"
        >
          {#if isLoading}
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            保存中...
          {:else}
            保存更改
          {/if}
        </button>
      </div>
    </svelte:fragment>
  </Modal>
{/if}
