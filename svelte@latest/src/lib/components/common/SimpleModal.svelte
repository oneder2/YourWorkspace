<script lang="ts">
  import { onMount, onDestroy, tick } from 'svelte';
  import { fly, fade } from 'svelte/transition';

  let {
    isOpen = false,
    title = '',
    close = () => {},
    modalWidth = 'max-w-lg'
  } = $props<{
    isOpen: boolean;
    title?: string;
    close: () => void;
    modalWidth?: string;
  }>();

  let modalContentElement = $state<HTMLElement | null>(null);

  function closeModal() {
    close();
  }

  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      closeModal();
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape' && isOpen) {
      closeModal();
    }
  }

  onMount(() => {
    window.addEventListener('keydown', handleKeydown);
  });

  onDestroy(() => {
    window.removeEventListener('keydown', handleKeydown);
  });
</script>

{#if isOpen}
<div
  class="fixed inset-0 bg-black/60 flex justify-center items-center p-4 z-50"
  on:click={handleBackdropClick}
  transition:fade={{ duration: 200 }}
>
  <div
    bind:this={modalContentElement}
    class="bg-white dark:bg-gray-800 rounded-lg shadow-xl flex flex-col w-full max-h-[90vh] overflow-hidden {modalWidth}"
    transition:fly={{ y: -30, duration: 300 }}
  >
    <header class="flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-700">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white">{title}</h2>
      <button
        class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
        on:click={closeModal}
      >
        &times;
      </button>
    </header>
    
    <div class="p-6 overflow-y-auto flex-grow">
      {@render $$slots.default ? $$slots.default() : () => (
        <p class="text-gray-700 dark:text-gray-300">Modal content goes here</p>
      )}
    </div>
    
    {#if $$slots.footer}
      <footer class="p-4 border-t border-gray-200 dark:border-gray-700">
        {@render $$slots.footer()}
      </footer>
    {/if}
  </div>
</div>
{/if}
