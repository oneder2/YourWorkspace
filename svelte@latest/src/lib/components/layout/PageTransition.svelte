<script lang="ts">
  /**
   * Page Transition component for smooth transitions between pages
   *
   * Usage:
   * ```svelte
   * <PageTransition>
   *   <slot />
   * </PageTransition>
   * ```
   */
  import { fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  import { page } from '$app/state';

  // Props
  let {
    duration = 250,
    delay = 0,
    y = 15,
    x = 0,
    class: className = '',
    children,
    ...rest
  } = $props<{
    duration?: number;
    delay?: number;
    y?: number;
    x?: number;
    class?: string;
    children?: any;
    [key: string]: any;
  }>();

  // Track current path for transitions
  let currentPath = $state('');

  // Update current path when page changes
  $effect(() => {
    if (page.url.pathname !== currentPath) {
      currentPath = page.url.pathname;
    }
  });
</script>

{#key currentPath}
  <div
    class={`page-transition ${className}`}
    in:fly={{ y, x, duration, delay, easing: cubicOut }}
    {...rest}
  >
    <slot />
  </div>
{/key}
