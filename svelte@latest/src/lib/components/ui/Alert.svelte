<script lang="ts">
  /**
   * Alert component for displaying messages, warnings, or errors
   *
   * Usage:
   * ```svelte
   * <Alert>Default alert message</Alert>
   * <Alert variant="primary" title="Information">This is an informational message</Alert>
   * <Alert variant="danger" dismissible>This is a dismissible error message</Alert>
   * ```
   */

  // Import necessary functions
  import { tick } from 'svelte';
  import { fade } from 'svelte/transition';

  // Create event dispatcher for Svelte 5
  const dispatch = (event: string, detail?: any) => {
    const e = new CustomEvent(event, { detail });
    document.dispatchEvent(e);
  };

  // Define props with TypeScript types
  let {
    variant = 'default',
    title = '',
    dismissible = false,
    icon = true,
    class: className = '',
    children,
    ...rest
  } = $props<{
    variant?: 'default' | 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'info';
    title?: string;
    dismissible?: boolean;
    icon?: boolean;
    class?: string;
    children?: any;
    [key: string]: any;
  }>();

  // State for visibility
  let visible = $state(true);

  // Variant classes mapping
  const variantClassesMap = {
    default: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-700',
    primary: 'bg-primary-50 text-primary-800 dark:bg-primary-900/20 dark:text-primary-300 border-primary-200 dark:border-primary-800',
    secondary: 'bg-secondary-50 text-secondary-800 dark:bg-secondary-900/20 dark:text-secondary-300 border-secondary-200 dark:border-secondary-800',
    danger: 'bg-danger-50 text-danger-800 dark:bg-danger-900/20 dark:text-danger-300 border-danger-200 dark:border-danger-800',
    success: 'bg-success-50 text-success-800 dark:bg-success-900/20 dark:text-success-300 border-success-200 dark:border-success-800',
    warning: 'bg-warning-50 text-warning-800 dark:bg-warning-900/20 dark:text-warning-300 border-warning-200 dark:border-warning-800',
    info: 'bg-info-50 text-info-800 dark:bg-info-900/20 dark:text-info-300 border-info-200 dark:border-info-800',
  };

  // Icon mapping
  const iconMap = {
    default: 'info',
    primary: 'info',
    secondary: 'info',
    danger: 'alert-triangle',
    success: 'check-circle',
    warning: 'alert-triangle',
    info: 'info',
  };

  // Compute classes based on variant
  const variantClasses = $derived(variantClassesMap[variant as keyof typeof variantClassesMap]);

  // Combine all classes
  const alertClasses = $derived(`
    relative rounded-lg border p-4
    ${variantClasses}
    ${className}
  `);

  // Get icon based on variant
  const alertIcon = $derived(iconMap[variant as keyof typeof iconMap]);

  // Handle dismiss
  async function dismiss() {
    visible = false;
    await tick();
    dispatch('dismiss');
  }
</script>

{#if visible}
  <div
    class={alertClasses}
    role="alert"
    transition:fade={{ duration: 200 }}
    {...rest}
  >
    <div class="flex">
      {#if icon}
        <div class="flex-shrink-0 mr-3">
          {#if alertIcon === 'info'}
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
          {:else if alertIcon === 'alert-triangle'}
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          {:else if alertIcon === 'check-circle'}
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          {/if}
        </div>
      {/if}

      <div class="flex-1">
        {#if title}
          <h3 class="text-sm font-medium mb-1">{title}</h3>
        {/if}
        <div class="text-sm">
          {children}
        </div>
      </div>

      {#if dismissible}
        <button
          type="button"
          class="ml-auto -mx-1.5 -my-1.5 bg-transparent text-current p-1.5 inline-flex items-center justify-center rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-transparent"
          aria-label="Dismiss"
          onclick={dismiss}
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      {/if}
    </div>
  </div>
{/if}
