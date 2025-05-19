<script lang="ts">
  /**
   * Page Loading Indicator component
   * Shows a loading bar at the top of the page during navigation
   *
   * Usage:
   * ```svelte
   * <PageLoadingIndicator />
   * ```
   */
  import { navigating } from '$app/state';
  import { onMount } from 'svelte';

  // Props
  let {
    height = '3px',
    color = 'var(--color-primary-500, #6366f1)',
    class: className = '',
    ...rest
  } = $props<{
    height?: string;
    color?: string;
    class?: string;
    [key: string]: any;
  }>();

  // State
  let progress = $state(0);
  let visible = $state(false);
  let complete = $state(false);
  let timeoutId: ReturnType<typeof setTimeout> | null = null;
  let loadingStuckTimeoutId: ReturnType<typeof setTimeout> | null = null;
  let loadingStuck = $state(false);

  // Watch for navigation changes using $effect
  $effect(() => {
    const isNavigating = navigating.from !== null;

    if (isNavigating) {
      startLoading();
    } else if (visible) {
      completeLoading();
    }
  });

  // Start loading animation
  function startLoading() {
    visible = true;
    complete = false;
    progress = 0;
    loadingStuck = false;

    // Clear any existing timeout
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }

    // Clear any existing loading stuck timeout
    if (loadingStuckTimeoutId) {
      clearTimeout(loadingStuckTimeoutId);
      loadingStuckTimeoutId = null;
    }

    // Set a timeout to detect if loading is stuck
    loadingStuckTimeoutId = setTimeout(() => {
      if (visible && !complete) {
        loadingStuck = true;
        console.warn('Loading seems to be taking longer than expected');
      }
    }, 8000); // 8 seconds timeout

    // Simulate progress
    simulateProgress();
  }

  // Simulate progress incrementally
  function simulateProgress() {
    if (!visible || complete) return;

    if (progress < 80) {
      // Increment progress with decreasing speed
      const increment = (100 - progress) / 10;
      progress += Math.min(increment, 10);

      // Schedule next increment
      timeoutId = setTimeout(simulateProgress, 100 + Math.random() * 300);
    }
  }

  // Complete loading animation
  function completeLoading() {
    // Jump to 100%
    progress = 100;
    complete = true;
    loadingStuck = false;

    // Clear loading stuck timeout
    if (loadingStuckTimeoutId) {
      clearTimeout(loadingStuckTimeoutId);
      loadingStuckTimeoutId = null;
    }

    // Hide after animation completes
    timeoutId = setTimeout(() => {
      visible = false;
      progress = 0;
    }, 300);
  }

  // Clean up on unmount
  onMount(() => {
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      if (loadingStuckTimeoutId) {
        clearTimeout(loadingStuckTimeoutId);
      }
    };
  });
</script>

<div
  class={`fixed top-0 left-0 right-0 z-50 ${loadingStuck ? 'pointer-events-auto' : 'pointer-events-none'} ${className} ${visible ? 'opacity-100' : 'opacity-0'}`}
  style="transition: opacity 300ms ease-in-out;"
  {...rest}
>
  <div
    class="h-full bg-current"
    style="
      height: {height};
      width: {progress}%;
      transition: width 300ms ease-out, opacity 300ms ease-in-out;
      background-color: {color};
      {complete ? 'transition-timing-function: cubic-bezier(0.19, 1, 0.22, 1);' : ''}
    "
  ></div>

  {#if loadingStuck}
    <div class="fixed inset-0 flex items-center justify-center bg-white/80 dark:bg-gray-900/80 z-50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg max-w-md text-center">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Loading seems to be stuck</h3>
        <p class="text-gray-600 dark:text-gray-300 mb-6">
          The page is taking longer than expected to load. This might be due to a network issue or a problem with the application.
        </p>
        <div class="flex justify-center space-x-4">
          <button
            class="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-md transition-colors"
            onclick={() => window.location.reload()}
          >
            Reload Page
          </button>
          <button
            class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white rounded-md transition-colors"
            onclick={() => { loadingStuck = false; }}
          >
            Continue Waiting
          </button>
        </div>
      </div>
    </div>
  {/if}
</div>
