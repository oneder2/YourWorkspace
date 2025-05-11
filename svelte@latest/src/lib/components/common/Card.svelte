<script lang="ts">
  /**
   * Card component using Tailwind CSS
   *
   * Usage:
   * <Card>Simple card with just body content</Card>
   *
   * <Card>
   *   <div slot="header">Card Header</div>
   *   Card Body Content
   *   <div slot="footer">Card Footer</div>
   * </Card>
   */

  // Props with defaults
  export let variant: 'default' | 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' = 'default';
  export let padding: 'none' | 'sm' | 'default' | 'lg' = 'default';
  export let shadow: 'none' | 'sm' | 'md' | 'lg' | 'xl' = 'md';
  export let rounded: 'none' | 'sm' | 'md' | 'lg' | 'xl' | 'full' = 'lg';
  export let border = false;
  export let hover = false;
  export let className = '';

  // Compute classes based on props
  const variantClassMap = {
    'default': 'bg-white dark:bg-gray-800',
    'primary': 'bg-primary-50 dark:bg-primary-900',
    'secondary': 'bg-secondary-50 dark:bg-secondary-900',
    'success': 'bg-success-50 dark:bg-success-900',
    'danger': 'bg-danger-50 dark:bg-danger-900',
    'warning': 'bg-warning-50 dark:bg-warning-900',
    'info': 'bg-info-50 dark:bg-info-900',
  };

  const shadowClassMap = {
    'none': '',
    'sm': 'shadow-sm',
    'md': 'shadow-md',
    'lg': 'shadow-lg',
    'xl': 'shadow-xl',
  };

  const roundedClassMap = {
    'none': 'rounded-none',
    'sm': 'rounded-sm',
    'md': 'rounded-md',
    'lg': 'rounded-lg',
    'xl': 'rounded-xl',
    'full': 'rounded-full',
  };

  const paddingClassMap = {
    'none': 'p-0',
    'sm': 'p-3',
    'default': 'p-5',
    'lg': 'p-7',
  };

  // Reactive declarations
  $: variantClasses = variantClassMap[variant];
  $: shadowClasses = shadowClassMap[shadow];
  $: roundedClasses = roundedClassMap[rounded];
  $: borderClass = border ? 'border border-gray-200 dark:border-gray-700' : '';
  $: hoverClass = hover ? 'transition-transform duration-200 hover:-translate-y-1 hover:shadow-lg' : '';
  $: cardClasses = `${variantClasses} ${shadowClasses} ${roundedClasses} ${borderClass} ${hoverClass} overflow-hidden ${className}`;
  $: bodyPaddingClass = paddingClassMap[padding];
</script>

<div class={cardClasses}>
  <slot name="header">
    <!-- Header content will be rendered here if provided -->
  </slot>

  <div class={bodyPaddingClass}>
    <slot>
      <!-- Default content will be rendered here -->
    </slot>
  </div>

  <slot name="footer">
    <!-- Footer content will be rendered here if provided -->
  </slot>
</div>
