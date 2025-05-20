<script lang="ts">
  /**
   * Skeleton component for loading states
   *
   * This component provides a customizable skeleton loader for various UI elements.
   * It can be used to create loading placeholders for text, images, cards, etc.
   */

  // Props
  let {
    type = 'text',
    width = '100%',
    height = '1rem',
    rounded = 'md',
    animate = true,
    shimmer = true,
    className = '',
    ...rest
  } = $props<{
    /** Type of skeleton (text, image, card, avatar, button, etc.) */
    type?: 'text' | 'image' | 'card' | 'avatar' | 'button' | 'custom';
    /** Width of the skeleton */
    width?: string | number;
    /** Height of the skeleton */
    height?: string | number;
    /** Rounded corners style */
    rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | 'full';
    /** Whether the skeleton should animate */
    animate?: boolean;
    /** Whether to show shimmer effect */
    shimmer?: boolean;
    /** Additional CSS classes */
    className?: string;
    /** Additional attributes */
    [key: string]: any;
  }>();

  // Rounded classes
  const roundedClasses: Record<string, string> = {
    'none': 'rounded-none',
    'sm': 'rounded-sm',
    'md': 'rounded',
    'lg': 'rounded-lg',
    'xl': 'rounded-xl',
    'full': 'rounded-full'
  };

  // Convert number to pixel string
  function toPx(value: string | number): string {
    if (typeof value === 'number') {
      return `${value}px`;
    }
    return value;
  }

  // Compute dimensions based on type
  $effect(() => {
    if (type === 'avatar' && height === '1rem') {
      width = '40px';
      height = '40px';
      rounded = 'full';
    } else if (type === 'image' && height === '1rem') {
      height = '200px';
    } else if (type === 'button' && height === '1rem') {
      height = '36px';
    } else if (type === 'card' && height === '1rem') {
      height = '120px';
    }
  });
</script>

<div
  class="skeleton {roundedClasses[rounded]} {animate ? 'animate-pulse' : ''} {shimmer ? 'with-shimmer' : ''} {className}"
  style="width: {toPx(width)}; height: {toPx(height)};"
  data-skeleton-type={type}
  {...rest}
>
  {#if type === 'card'}
    <div class="flex flex-col h-full">
      <div class="skeleton-part h-2/3 rounded-t-md"></div>
      <div class="skeleton-part p-3 space-y-2">
        <div class="skeleton-part h-4 rounded w-3/4"></div>
        <div class="skeleton-part h-3 rounded w-1/2"></div>
      </div>
    </div>
  {/if}
</div>

<style>
  .skeleton {
    background-color: rgb(229, 231, 235); /* bg-gray-200 */
    position: relative;
    overflow: hidden;
  }

  :global(.dark) .skeleton {
    background-color: rgb(55, 65, 81); /* dark:bg-gray-700 */
  }

  .with-shimmer::after {
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    transform: translateX(-100%);
    animation: shimmer 2s infinite;
  }

  .skeleton-part {
    position: relative;
    overflow: hidden;
  }

  @keyframes shimmer {
    100% {
      transform: translateX(100%);
    }
  }
</style>
