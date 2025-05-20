<script lang="ts">
  /**
   * Content Loader component
   *
   * This component provides a loading state for content areas.
   * It shows skeleton loaders or a spinner based on the configuration.
   */
  import Skeleton from './Skeleton.svelte';
  import { fade } from 'svelte/transition';
  import { onDestroy } from 'svelte';

  // Props
  let {
    isLoading = true,
    error = null,
    delay = 300,
    type = 'default',
    skeletonCount = 3,
    skeletonType = 'text',
    skeletonHeight = '1rem',
    skeletonGap = '0.5rem',
    showSpinner = false,
    children,
    class: className = '',
    ...rest
  } = $props<{
    /** Whether content is loading */
    isLoading?: boolean;
    /** Error message or object if loading failed */
    error?: any;
    /** Delay before showing loading state (ms) */
    delay?: number;
    /** Type of content being loaded */
    type?: 'default' | 'list' | 'card' | 'table' | 'custom';
    /** Number of skeleton items to show */
    skeletonCount?: number;
    /** Type of skeleton to use */
    skeletonType?: 'text' | 'card' | 'image' | 'avatar' | 'button';
    /** Height of skeleton items */
    skeletonHeight?: string | number;
    /** Gap between skeleton items */
    skeletonGap?: string | number;
    /** Whether to show a spinner instead of skeletons */
    showSpinner?: boolean;
    /** Content to render when not loading */
    children?: any;
    /** Additional CSS classes */
    class?: string;
    /** Additional attributes */
    [key: string]: any;
  }>();

  // State
  let showLoading = $state(false);
  let timeoutId: ReturnType<typeof setTimeout> | null = null;

  // Handle loading state with delay
  $effect(() => {
    if (isLoading) {
      // Clear any existing timeout
      if (timeoutId) {
        clearTimeout(timeoutId);
      }

      // Set timeout to show loading state after delay
      timeoutId = setTimeout(() => {
        showLoading = true;
      }, delay);
    } else {
      // Clear timeout if loading finished
      if (timeoutId) {
        clearTimeout(timeoutId);
        timeoutId = null;
      }

      // Hide loading state
      showLoading = false;
    }
  });

  // Clean up on unmount
  onDestroy(() => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
  });

  // Generate skeleton items based on type
  function getSkeletonItems() {
    const items = [];

    for (let i = 0; i < skeletonCount; i++) {
      items.push({
        type: skeletonType,
        key: i
      });
    }

    return items;
  }

  // Skeleton items
  const skeletonItems = $derived(getSkeletonItems());
</script>

<div class={`content-loader ${className}`} {...rest}>
  {#if isLoading && showLoading}
    <div
      class="content-loader-skeleton"
      style={`gap: ${typeof skeletonGap === 'number' ? `${skeletonGap}px` : skeletonGap};`}
      transition:fade={{ duration: 200 }}
    >
      {#if showSpinner}
        <div class="flex justify-center items-center py-8">
          <div class="spinner"></div>
        </div>
      {:else if type === 'list'}
        {#each skeletonItems as item (item.key)}
          <Skeleton
            type={item.type}
            height={skeletonHeight}
            shimmer={true}
          />
        {/each}
      {:else if type === 'card'}
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {#each skeletonItems as item (item.key)}
            <Skeleton type="card" />
          {/each}
        </div>
      {:else}
        {#each skeletonItems as item (item.key)}
          <Skeleton
            type={item.type}
            height={skeletonHeight}
            shimmer={true}
          />
        {/each}
      {/if}
    </div>
  {:else if error}
    <div class="content-loader-error" transition:fade={{ duration: 200 }}>
      <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md p-4 my-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
              Error loading content
            </h3>
            <div class="mt-2 text-sm text-red-700 dark:text-red-300">
              {typeof error === 'string' ? error : error?.message || 'An unexpected error occurred'}
            </div>
          </div>
        </div>
      </div>
    </div>
  {:else}
    <div class="content-loader-content" transition:fade={{ duration: 200 }}>
      {@render children()}
    </div>
  {/if}
</div>

<style>
  .content-loader {
    width: 100%;
  }

  .content-loader-skeleton {
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  .spinner {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    border: 0.25rem solid rgba(156, 163, 175, 0.3);
    border-top-color: rgba(156, 163, 175, 1);
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
