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
    children,
    ...rest
  } = $props<{
    variant?: 'default' | 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'info';
    padding?: boolean;
    shadow?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
    rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | 'full';
    border?: boolean;
    class?: string;
    children?: any;
    [key: string]: any;
  }>();

  // Variant classes mapping
  const variantClassesMap = {
    default: 'bg-white dark:bg-gray-800',
    primary: 'bg-primary-50 dark:bg-primary-900/20',
    secondary: 'bg-secondary-50 dark:bg-secondary-900/20',
    danger: 'bg-danger-50 dark:bg-danger-900/20',
    success: 'bg-success-50 dark:bg-success-900/20',
    warning: 'bg-warning-50 dark:bg-warning-900/20',
    info: 'bg-info-50 dark:bg-info-900/20',
  };

  // Shadow classes mapping
  const shadowClassesMap = {
    none: '',
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
    xl: 'shadow-xl',
  };

  // Rounded classes mapping
  const roundedClassesMap = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    '2xl': 'rounded-2xl',
    '3xl': 'rounded-3xl',
    full: 'rounded-full',
  };

  // Compute classes
  const variantClasses = $derived(variantClassesMap[variant as keyof typeof variantClassesMap]);
  const shadowClasses = $derived(shadowClassesMap[shadow as keyof typeof shadowClassesMap]);
  const roundedClasses = $derived(roundedClassesMap[rounded as keyof typeof roundedClassesMap]);

  // Compute border classes
  const borderClasses = $derived(border
    ? variant === 'default'
      ? 'border border-gray-200 dark:border-gray-700'
      : `border border-${variant}-200 dark:border-${variant}-800`
    : '');

  // Combine all classes
  const cardClasses = $derived(`
    overflow-hidden
    ${variantClasses}
    ${shadowClasses}
    ${roundedClasses}
    ${borderClasses}
    ${className}
  `);

  // Compute padding classes for body
  const bodyPaddingClass = $derived(padding ? 'p-6' : '');
</script>

<div class={cardClasses} {...rest}>
  {#if children?.header}
    <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
      {children.header}
    </div>
  {/if}

  <div class={bodyPaddingClass}>
    {children?.default}
  </div>

  {#if children?.footer}
    <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
      {children.footer}
    </div>
  {/if}
</div>
