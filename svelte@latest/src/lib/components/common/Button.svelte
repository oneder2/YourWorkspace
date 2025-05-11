<script lang="ts">
  /**
   * Button component using Tailwind CSS
   *
   * Usage:
   * <Button>Default Button</Button>
   * <Button variant="primary" size="lg">Primary Large Button</Button>
   * <Button variant="outline" disabled>Disabled Outline Button</Button>
   */

  // Button variants
  type ButtonVariant = 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'light' | 'dark' | 'outline' | 'link';

  // Button sizes
  type ButtonSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

  // Props with defaults
  export let variant: ButtonVariant = 'primary';
  export let size: ButtonSize = 'md';
  export let type: 'button' | 'submit' | 'reset' = 'button';
  export let disabled = false;
  export let fullWidth = false;
  export let loading = false;
  export let loadingText = 'Loading...';
  export let icon = null;
  export let iconPosition: 'left' | 'right' = 'left';
  export let href: string | undefined = undefined;
  export let onClick: ((event: MouseEvent) => void) | undefined = undefined;
  export let ariaLabel: string | undefined = undefined;
  export let className = '';

  // Variant classes mapping
  const variantClassMap = {
    'primary': 'bg-primary-500 hover:bg-primary-600 text-white focus:ring-primary-500',
    'secondary': 'bg-secondary-500 hover:bg-secondary-600 text-white focus:ring-secondary-500',
    'success': 'bg-success-500 hover:bg-success-600 text-white focus:ring-success-500',
    'danger': 'bg-danger-500 hover:bg-danger-600 text-white focus:ring-danger-500',
    'warning': 'bg-warning-500 hover:bg-warning-600 text-dark focus:ring-warning-500',
    'info': 'bg-info-500 hover:bg-info-600 text-white focus:ring-info-500',
    'light': 'bg-light hover:bg-light-hover text-dark focus:ring-light',
    'dark': 'bg-dark hover:bg-dark-hover text-white focus:ring-dark',
    'outline': 'bg-transparent border border-gray-300 hover:bg-gray-50 text-dark focus:ring-primary-500',
    'link': 'bg-transparent hover:underline text-primary-500 focus:ring-primary-500',
  };

  // Size classes mapping
  const sizeClassMap = {
    'xs': 'text-xs py-1 px-2',
    'sm': 'text-sm py-1.5 px-3',
    'md': 'text-sm py-2 px-4',
    'lg': 'text-base py-2.5 px-5',
    'xl': 'text-lg py-3 px-6',
  };

  // Base classes
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors';

  // Reactive declarations
  $: variantClasses = variantClassMap[variant];
  $: sizeClasses = sizeClassMap[size];
  $: widthClass = fullWidth ? 'w-full' : '';
  $: disabledClass = disabled ? 'opacity-60 cursor-not-allowed' : '';
  $: buttonClasses = `${baseClasses} ${variantClasses} ${sizeClasses} ${widthClass} ${disabledClass} ${className}`;

  function handleClick(event: MouseEvent) {
    if (disabled || loading) {
      event.preventDefault();
      return;
    }

    if (onClick) onClick(event);
  }
</script>

{#if href !== undefined}
  <a
    {href}
    class={buttonClasses}
    aria-disabled={disabled || loading}
    aria-label={ariaLabel}
    on:click={handleClick}
  >
    {#if loading}
      <span class="mr-2 inline-block animate-spin">⟳</span>
      {loadingText}
    {:else if icon && iconPosition === 'left'}
      <span class="mr-2">{icon}</span>
      <slot />
    {:else if icon && iconPosition === 'right'}
      <slot />
      <span class="ml-2">{icon}</span>
    {:else}
      <slot />
    {/if}
  </a>
{:else}
  <button
    {type}
    class={buttonClasses}
    disabled={disabled || loading}
    aria-disabled={disabled || loading}
    aria-label={ariaLabel}
    on:click={handleClick}
  >
    {#if loading}
      <span class="mr-2 inline-block animate-spin">⟳</span>
      {loadingText}
    {:else if icon && iconPosition === 'left'}
      <span class="mr-2">{icon}</span>
      <slot />
    {:else if icon && iconPosition === 'right'}
      <slot />
      <span class="ml-2">{icon}</span>
    {:else}
      <slot />
    {/if}
  </button>
{/if}
