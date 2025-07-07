<script lang="ts">
  /**
   * Button component with various styles and sizes
   *
   * Usage:
   * ```svelte
   * <Button>Default Button</Button>
   * <Button variant="primary">Primary Button</Button>
   * <Button variant="outline" size="sm">Small Outline Button</Button>
   * <Button variant="danger" disabled>Disabled Danger Button</Button>
   * <Button variant="success" class="mt-4">Custom Class Button</Button>
   * ```
   */

  // Import types
  import type { HTMLButtonAttributes } from 'svelte/elements';

  // Define props with TypeScript types
  let {
    variant = 'default',
    size = 'md',
    type = 'button',
    disabled = false,
    loading = false,
    fullWidth = false,
    class: className = '',
    onclick,
    onfocus,
    onblur,
    onmouseenter,
    onmouseleave,
    ...rest
  } = $props<{
    variant?: 'default' | 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'info' | 'outline' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    type?: HTMLButtonAttributes['type'];
    disabled?: boolean;
    loading?: boolean;
    fullWidth?: boolean;
    class?: string;
    onclick?: (event: MouseEvent) => void;
    onfocus?: (event: FocusEvent) => void;
    onblur?: (event: FocusEvent) => void;
    onmouseenter?: (event: MouseEvent) => void;
    onmouseleave?: (event: MouseEvent) => void;
    [key: string]: any;
  }>();

  // Variant classes mapping
  const variantClassesMap = {
    default: 'bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-400 dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600',
    primary: 'bg-primary-500 text-white hover:bg-primary-600 focus:ring-primary-400 dark:bg-primary-600 dark:hover:bg-primary-700',
    secondary: 'bg-secondary-500 text-white hover:bg-secondary-600 focus:ring-secondary-400 dark:bg-secondary-600 dark:hover:bg-secondary-700',
    danger: 'bg-danger-500 text-white hover:bg-danger-600 focus:ring-danger-400 dark:bg-danger-600 dark:hover:bg-danger-700',
    success: 'bg-success-500 text-white hover:bg-success-600 focus:ring-success-400 dark:bg-success-600 dark:hover:bg-success-700',
    warning: 'bg-warning-500 text-white hover:bg-warning-600 focus:ring-warning-400 dark:bg-warning-600 dark:hover:bg-warning-700',
    info: 'bg-info-500 text-white hover:bg-info-600 focus:ring-info-400 dark:bg-info-600 dark:hover:bg-info-700',
    outline: 'border border-gray-300 bg-transparent text-gray-700 hover:bg-gray-50 focus:ring-gray-400 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-gray-400 dark:text-gray-300 dark:hover:bg-gray-800',
  };

  // Size classes mapping
  const sizeClassesMap = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
  };

  // Compute classes
  const variantClasses = $derived(variantClassesMap[variant as keyof typeof variantClassesMap]);
  const sizeClasses = $derived(sizeClassesMap[size as keyof typeof sizeClassesMap]);
  const widthClass = $derived(fullWidth ? 'w-full' : '');

  // Combine all classes
  const buttonClasses = $derived(`
    inline-flex items-center justify-center
    font-medium rounded-md
    transition-colors duration-200
    focus:outline-none focus:ring-2 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
    ${variantClasses}
    ${sizeClasses}
    ${widthClass}
    ${className}
  `);
</script>

<button
  type={type}
  class={buttonClasses}
  disabled={disabled || loading}
  onclick={onclick}
  onfocus={onfocus}
  onblur={onblur}
  onmouseenter={onmouseenter}
  onmouseleave={onmouseleave}
  {...rest}
>
  {#if loading}
    <span class="mr-2 inline-block animate-spin">
      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
      </svg>
    </span>
  {/if}
  <slot />
</button>
