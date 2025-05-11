<script lang="ts">
  /**
   * Card component with header, body, and footer sections
   * 
   * Usage:
   * ```svelte
   * <Card>
   *   <p>Simple card with just body content</p>
   * </Card>
   * 
   * <Card>
   *   <svelte:fragment slot="header">
   *     <h3>Card Title</h3>
   *   </svelte:fragment>
   *   
   *   <p>Card body content</p>
   *   
   *   <svelte:fragment slot="footer">
   *     <Button>Action</Button>
   *   </svelte:fragment>
   * </Card>
   * ```
   */

  // Define props with TypeScript types
  let {
    variant = 'default',
    padding = true,
    shadow = 'md',
    rounded = 'lg',
    border = true,
    class: className = '',
    ...rest
  } = $props<{
    variant?: 'default' | 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'info';
    padding?: boolean;
    shadow?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
    rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | 'full';
    border?: boolean;
    class?: string;
    [key: string]: any;
  }>();

  // Compute classes based on variant
  $: variantClasses = {
    default: 'bg-white dark:bg-gray-800',
    primary: 'bg-primary-50 dark:bg-primary-900/20',
    secondary: 'bg-secondary-50 dark:bg-secondary-900/20',
    danger: 'bg-danger-50 dark:bg-danger-900/20',
    success: 'bg-success-50 dark:bg-success-900/20',
    warning: 'bg-warning-50 dark:bg-warning-900/20',
    info: 'bg-info-50 dark:bg-info-900/20',
  }[variant];

  // Compute shadow classes
  $: shadowClasses = {
    none: '',
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
    xl: 'shadow-xl',
  }[shadow];

  // Compute rounded classes
  $: roundedClasses = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    '2xl': 'rounded-2xl',
    '3xl': 'rounded-3xl',
    full: 'rounded-full',
  }[rounded];

  // Compute border classes
  $: borderClasses = border 
    ? variant === 'default' 
      ? 'border border-gray-200 dark:border-gray-700' 
      : `border border-${variant}-200 dark:border-${variant}-800`
    : '';
  
  // Combine all classes
  $: cardClasses = `
    overflow-hidden
    ${variantClasses}
    ${shadowClasses}
    ${roundedClasses}
    ${borderClasses}
    ${className}
  `;

  // Compute padding classes for body
  $: bodyPaddingClass = padding ? 'p-6' : '';
</script>

<div class={cardClasses} {...rest}>
  {#if $$slots.header}
    <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
      <slot name="header" />
    </div>
  {/if}
  
  <div class={bodyPaddingClass}>
    <slot />
  </div>
  
  {#if $$slots.footer}
    <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
      <slot name="footer" />
    </div>
  {/if}
</div>
