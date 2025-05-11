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

    // Clear any existing timeout
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }

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
    };
  });
</script>

<div
  class={`fixed top-0 left-0 right-0 z-50 pointer-events-none ${className} ${visible ? 'opacity-100' : 'opacity-0'}`}
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
</div>
