<script lang="ts">
  /**
   * Badge component for displaying status, counts, or labels
   *
   * Usage:
   * ```svelte
   * <Badge>Default</Badge>
   * <Badge variant="primary">Primary</Badge>
   * <Badge variant="success" size="lg">Success</Badge>
   * <Badge variant="danger" rounded="full">Error</Badge>
   * ```
   */

  // Define props with TypeScript types
  let {
    variant = 'default',
    size = 'md',
    rounded = 'full',
    class: className = '',
    children,
    ...rest
  } = $props<{
    variant?: 'default' | 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'info' | 'outline';
    size?: 'sm' | 'md' | 'lg';
    rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | 'full';
    class?: string;
    children?: any;
    [key: string]: any;
  }>();

  // Variant classes mapping
  const variantClassesMap = {
    default: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    primary: 'bg-primary-100 text-primary-800 dark:bg-primary-900/30 dark:text-primary-300',
    secondary: 'bg-secondary-100 text-secondary-800 dark:bg-secondary-900/30 dark:text-secondary-300',
    danger: 'bg-danger-100 text-danger-800 dark:bg-danger-900/30 dark:text-danger-300',
    success: 'bg-success-100 text-success-800 dark:bg-success-900/30 dark:text-success-300',
    warning: 'bg-warning-100 text-warning-800 dark:bg-warning-900/30 dark:text-warning-300',
    info: 'bg-info-100 text-info-800 dark:bg-info-900/30 dark:text-info-300',
    outline: 'bg-transparent border border-gray-300 text-gray-700 dark:border-gray-600 dark:text-gray-300',
  };

  // Size classes mapping
  const sizeClassesMap = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-0.5 text-xs',
    lg: 'px-3 py-1 text-sm',
  };

  // Rounded classes mapping
  const roundedClassesMap = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    full: 'rounded-full',
  };

  // Compute classes
  const variantClasses = $derived(variantClassesMap[variant as keyof typeof variantClassesMap]);
  const sizeClasses = $derived(sizeClassesMap[size as keyof typeof sizeClassesMap]);
  const roundedClasses = $derived(roundedClassesMap[rounded as keyof typeof roundedClassesMap]);

  // Combine all classes
  const badgeClasses = $derived(`
    inline-flex items-center font-medium
    ${variantClasses}
    ${sizeClasses}
    ${roundedClasses}
    ${className}
  `);
</script>

<span class={badgeClasses} {...rest}>
  {children}
</span>
