<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  // Props
  let { fallback } = $props<{
    fallback?: (error: Error, reset: () => void) => any;
  }>();

  // State
  let error = $state<Error | null>(null);
  let errorInfo = $state<string>('');

  // Error handling
  function handleError(event: ErrorEvent) {
    error = event.error || new Error(event.message);
    errorInfo = event.message;
    event.preventDefault();
    console.error('ErrorBoundary caught an error:', error);
  }

  // Reset error state
  function reset() {
    error = null;
    errorInfo = '';
  }

  // Lifecycle
  onMount(() => {
    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', (event) => {
      handleError(new ErrorEvent('error', {
        error: event.reason,
        message: event.reason?.message || 'Unhandled Promise Rejection'
      }));
      event.preventDefault();
    });
  });

  onDestroy(() => {
    window.removeEventListener('error', handleError);
    window.removeEventListener('unhandledrejection', handleError);
  });
</script>

{#if error}
  {#if fallback}
    {@render fallback(error, reset)}
  {:else}
    <div class="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
      <div class="flex items-center mb-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <h3 class="text-lg font-medium text-red-800 dark:text-red-200">Something went wrong</h3>
      </div>
      <p class="text-sm text-red-700 dark:text-red-300 mb-4">{errorInfo || error.message}</p>
      <button
        onclick={reset}
        class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
      >
        Try Again
      </button>
    </div>
  {/if}
{:else}
  <slot />
{/if}
