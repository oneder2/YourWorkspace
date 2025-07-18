<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fly, fade } from 'svelte/transition';
  import { toastStore, type Toast } from '$lib/store/toastStore';

  // Props
  let { position = 'bottom-right' } = $props<{
    position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'top-center' | 'bottom-center';
  }>();

  // State
  let toasts = $state<Toast[]>([]);

  // Subscribe to toast store
  onMount(() => {
    const unsubscribe = toastStore.subscribe(($toasts) => {
      toasts = $toasts;
    });

    return unsubscribe;
  });

  // Position classes
  const positionClasses = {
    'top-left': 'top-4 left-4',
    'top-right': 'top-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-right': 'bottom-4 right-4',
    'top-center': 'top-4 left-1/2 transform -translate-x-1/2',
    'bottom-center': 'bottom-4 left-1/2 transform -translate-x-1/2'
  };

  // Toast type classes
  const typeClasses = {
    success: 'bg-green-500 dark:bg-green-600',
    error: 'bg-red-500 dark:bg-red-600',
    warning: 'bg-yellow-500 dark:bg-yellow-600',
    info: 'bg-blue-500 dark:bg-blue-600'
  };

  // Toast icon based on type
  function getToastIcon(type: Toast['type']) {
    switch (type) {
      case 'success':
        return `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>`;
      case 'error':
        return `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>`;
      case 'warning':
        return `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>`;
      case 'info':
      default:
        return `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>`;
    }
  }

  // Dismiss toast
  function dismissToast(id: string) {
    toastStore.dismiss(id);
  }
</script>

<div class="fixed z-50 flex flex-col gap-2 max-w-xs w-full {positionClasses[position]}">
  {#each toasts as toast (toast.id)}
    <div
      class="flex items-center p-4 rounded-lg shadow-lg text-white {typeClasses[toast.type]}"
      role="alert"
      in:fly={{ y: position.includes('top') ? -20 : 20, duration: 300 }}
      out:fade={{ duration: 200 }}
    >
      <div class="flex-shrink-0 mr-2">
        {@html getToastIcon(toast.type)}
      </div>
      <div class="flex-1 mr-2">
        {#if toast.title}
          <div class="font-semibold">{toast.title}</div>
        {/if}
        <div>{toast.message}</div>
      </div>
      <button
        onclick={() => dismissToast(toast.id)}
        class="flex-shrink-0 text-white hover:text-gray-200 focus:outline-none"
        aria-label="Close"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>
  {/each}
</div>
