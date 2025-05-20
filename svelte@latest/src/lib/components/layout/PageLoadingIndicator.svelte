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
  let navigationStart = $state<number | null>(null);
  let navigationDuration = $state(0);
  let previousNavigations = $state<number[]>([]);
  let averageNavigationTime = $state(0);
  let expectedCompletionTime = $state(0);

  // Maximum number of previous navigations to track for average calculation
  const MAX_NAVIGATION_HISTORY = 5;

  // Minimum progress to show (even for instant navigations)
  const MIN_PROGRESS = 15;

  // Watch for navigation changes using $effect
  $effect(() => {
    const isNavigating = navigating.from !== null;
    const navigationFromPath = navigating.from?.url.pathname;
    const navigationToPath = navigating.to?.url.pathname;

    if (isNavigating) {
      // Start navigation
      navigationStart = performance.now();

      // Calculate expected completion time based on previous navigations
      if (previousNavigations.length > 0) {
        averageNavigationTime = previousNavigations.reduce((sum, time) => sum + time, 0) / previousNavigations.length;
        expectedCompletionTime = navigationStart + averageNavigationTime;
      } else {
        // Default to 500ms if no history
        expectedCompletionTime = navigationStart + 500;
      }

      // Log navigation for debugging
      console.log(`Navigation started: ${navigationFromPath} -> ${navigationToPath}`);
      console.log(`Expected completion in ~${averageNavigationTime.toFixed(0)}ms based on history`);

      startLoading();
    } else if (visible) {
      // Navigation complete
      if (navigationStart) {
        const endTime = performance.now();
        navigationDuration = endTime - navigationStart;

        // Add to history (keeping only the most recent ones)
        previousNavigations = [navigationDuration, ...previousNavigations.slice(0, MAX_NAVIGATION_HISTORY - 1)];

        // Log for debugging
        console.log(`Navigation completed in ${navigationDuration.toFixed(0)}ms`);
        console.log(`Navigation history: ${previousNavigations.map(t => t.toFixed(0)).join(', ')}ms`);

        // Reset
        navigationStart = null;
      }

      completeLoading();
    }
  });

  // Start loading animation
  function startLoading() {
    visible = true;
    complete = false;
    progress = MIN_PROGRESS; // Start with minimum progress
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

  // Simulate progress incrementally based on expected completion time
  function simulateProgress() {
    if (!visible || complete) return;

    if (progress < 90) {
      // Calculate progress based on time elapsed and expected completion
      if (navigationStart && expectedCompletionTime) {
        const now = performance.now();
        const elapsed = now - navigationStart;
        const expectedTotal = expectedCompletionTime - navigationStart;

        // Calculate target progress (capped at 90%)
        const targetProgress = Math.min(
          90,
          MIN_PROGRESS + (elapsed / expectedTotal) * (90 - MIN_PROGRESS)
        );

        // Smooth progress updates
        progress = progress + (targetProgress - progress) * 0.2;
      } else {
        // Fallback to simple increment if timing data is not available
        const increment = (100 - progress) / 10;
        progress += Math.min(increment, 5);
      }

      // Schedule next increment
      timeoutId = setTimeout(simulateProgress, 50);
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
  <!-- Main progress bar -->
  <div class="relative h-full">
    <!-- Background track -->
    <div
      class="absolute top-0 left-0 right-0 bg-gray-200 dark:bg-gray-700 opacity-30"
      style={`height: ${height};`}
    ></div>

    <!-- Progress indicator -->
    <div
      class="h-full bg-current relative"
      style={`
        height: ${height};
        width: ${progress}%;
        transition: width 300ms ease-out, opacity 300ms ease-in-out;
        background-color: ${color};
        ${complete ? 'transition-timing-function: cubic-bezier(0.19, 1, 0.22, 1);' : ''}
      `}
    >
      <!-- Animated pulse effect for the leading edge -->
      <div
        class="absolute right-0 top-0 bottom-0 w-4 bg-white opacity-50 animate-pulse"
        style={`height: ${height};`}
      ></div>
    </div>
  </div>

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
