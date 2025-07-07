<script lang="ts">
  /**
   * Theme Toggle component for switching between light and dark mode
   *
   * Usage:
   * ```svelte
   * <ThemeToggle />
   * ```
   */
  import { themeStore, isDarkMode } from '$lib/store/themeStore';

  // Props
  let {
    size = 'md',
    class: className = '',
    ...rest
  } = $props<{
    size?: 'sm' | 'md' | 'lg';
    class?: string;
    [key: string]: any;
  }>();

  // Size classes mapping
  const sizeClassesMap = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12',
  };

  // Compute size classes
  const sizeClasses = $derived(sizeClassesMap[size as keyof typeof sizeClassesMap]);

  // Toggle dark mode
  function toggleTheme() {
    themeStore.toggleDarkMode();
  }
</script>

<button
  type="button"
  class={`rounded-full p-2 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 ${
    $isDarkMode
      ? 'bg-gray-800 text-yellow-300 hover:bg-gray-700'
      : 'bg-gray-200 text-gray-900 hover:bg-gray-300'
  } ${sizeClasses} ${className}`}
  aria-label={$isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
  title={$isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
  onclick={toggleTheme}
  {...rest}
>
  {#if $isDarkMode}
    <!-- Sun icon for dark mode (clicking switches to light) -->
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" class="w-full h-full">
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
    </svg>
  {:else}
    <!-- Moon icon for light mode (clicking switches to dark) -->
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" class="w-full h-full">
      <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
    </svg>
  {/if}
</button>
