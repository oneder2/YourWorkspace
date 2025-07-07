<script lang="ts">
  /**
   * Page Transition component for smooth transitions between pages
   * Enhanced with multiple transition effects and performance optimizations
   *
   * Usage:
   * ```svelte
   * <PageTransition>
   *   <slot />
   * </PageTransition>
   * ```
   */
  import { fly, fade, slide, scale } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  import { page } from '$app/state';
  import { browser } from '$app/environment';
  import { preloadRouteImages } from '$lib/utils/imagePreloader';
  import { preloadRouteSvgIcons } from '$lib/utils/svgUtils';
  import { prefetchRoute } from '$lib/utils/lazyLoad';
  import { mark } from '$lib/utils/performance';

  // Transition types
  type TransitionType = 'fly' | 'fade' | 'slide' | 'scale' | 'none';

  // Props
  let {
    duration = 250,
    delay = 0,
    y = 15,
    x = 0,
    type = 'fly' as TransitionType,
    easing = cubicOut,
    class: className = '',
    children,
    ...rest
  } = $props<{
    duration?: number;
    delay?: number;
    y?: number;
    x?: number;
    type?: TransitionType;
    easing?: (t: number) => number;
    class?: string;
    children?: any;
    [key: string]: any;
  }>();

  // Track current path for transitions
  let currentPath = $state('');
  let previousPath = $state('');
  let isInitialLoad = $state(true);
  let transitionDirection = $state<'next' | 'prev' | 'none'>('none');

  // Determine transition direction based on route
  function getTransitionDirection(from: string, to: string): 'next' | 'prev' | 'none' {
    const routeOrder = ['/done', '/doing', '/plan'];

    // If either path is not in the route order, don't animate direction
    if (!routeOrder.includes(from) || !routeOrder.includes(to)) {
      return 'none';
    }

    const fromIndex = routeOrder.indexOf(from);
    const toIndex = routeOrder.indexOf(to);

    if (fromIndex < toIndex) {
      return 'next';
    } else if (fromIndex > toIndex) {
      return 'prev';
    } else {
      return 'none';
    }
  }

  // Adjust transition parameters based on direction
  function getTransitionParams() {
    // Default parameters
    const params = {
      duration,
      delay,
      easing
    };

    // Add direction-specific parameters
    if (transitionDirection === 'next') {
      return {
        ...params,
        x: 50,
        y: 0
      };
    } else if (transitionDirection === 'prev') {
      return {
        ...params,
        x: -50,
        y: 0
      };
    } else {
      return {
        ...params,
        x,
        y
      };
    }
  }

  // Preload resources for the next route
  async function preloadNextRoute(route: string) {
    if (!browser) return;

    mark(`route-preload-start-${route}`);

    // Preload in parallel
    await Promise.all([
      preloadRouteImages(route),
      preloadRouteSvgIcons(route)
    ]);

    // Prefetch components for the route
    prefetchRoute(route);

    mark(`route-preload-end-${route}`, `route-preload-${route}`);
  }

  // Update current path when page changes
  $effect(() => {
    if (browser && page.url.pathname !== currentPath) {
      // Store previous path
      previousPath = currentPath;

      // Update current path
      currentPath = page.url.pathname;

      // Determine transition direction
      transitionDirection = getTransitionDirection(previousPath, currentPath);

      // Skip transition on initial load
      if (isInitialLoad) {
        isInitialLoad = false;
      }

      // Preload resources for the current route
      preloadNextRoute(currentPath);
    }
  });

  // Choose transition effect based on type
  function getTransition(node: HTMLElement) {
    const params = getTransitionParams();

    switch (type) {
      case 'fly':
        return fly(node, params);
      case 'fade':
        return fade(node, params);
      case 'slide':
        return slide(node, params);
      case 'scale':
        return scale(node, params);
      case 'none':
        return {
          duration: 0,
          css: () => ''
        };
      default:
        return fly(node, params);
    }
  }
</script>

{#key currentPath}
  <div
    class={`page-transition ${className} ${transitionDirection !== 'none' ? `transition-${transitionDirection}` : ''}`}
    in:getTransition
    {...rest}
  >
    {@render children()}
  </div>
{/key}

<style>
  .page-transition {
    width: 100%;
    height: 100%;
    position: relative;
  }

  .transition-next {
    transform-origin: left center;
  }

  .transition-prev {
    transform-origin: right center;
  }
</style>
