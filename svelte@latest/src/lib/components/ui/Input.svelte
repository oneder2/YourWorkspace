<script lang="ts">
  /**
   * Input component with various styles and states
   * 
   * Usage:
   * ```svelte
   * <Input placeholder="Enter your name" />
   * <Input type="email" label="Email Address" required />
   * <Input type="password" label="Password" error="Password is too short" />
   * <Input type="text" label="Username" hint="Choose a unique username" />
   * <Input type="text" disabled value="Disabled input" />
   * ```
   */

  // Import types
  import type { HTMLInputAttributes } from 'svelte/elements';
  import { createEventDispatcher } from 'svelte';

  // Create event dispatcher
  const dispatch = createEventDispatcher();
  
  // Define props with TypeScript types
  let {
    type = 'text',
    value = '',
    placeholder = '',
    label = '',
    id = '',
    name = '',
    disabled = false,
    readonly = false,
    required = false,
    error = '',
    hint = '',
    fullWidth = true,
    class: className = '',
    ...rest
  } = $props<{
    type?: HTMLInputAttributes['type'];
    value?: string | number;
    placeholder?: string;
    label?: string;
    id?: string;
    name?: string;
    disabled?: boolean;
    readonly?: boolean;
    required?: boolean;
    error?: string;
    hint?: string;
    fullWidth?: boolean;
    class?: string;
    [key: string]: any;
  }>();

  // Generate a unique ID if not provided
  $: inputId = id || `input-${Math.random().toString(36).substring(2, 9)}`;
  
  // Compute classes based on state
  $: inputClasses = `
    block px-3 py-2 bg-white dark:bg-gray-800 
    border rounded-md shadow-sm
    focus:outline-none focus:ring-2 focus:ring-offset-0
    disabled:opacity-50 disabled:cursor-not-allowed
    ${error ? 'border-danger-500 focus:border-danger-500 focus:ring-danger-400' : 'border-gray-300 dark:border-gray-600 focus:border-primary-500 focus:ring-primary-400'}
    ${fullWidth ? 'w-full' : ''}
    ${className}
  `;

  // Handle input event
  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    value = target.value;
    dispatch('input', { value });
  }

  // Handle change event
  function handleChange(event: Event) {
    const target = event.target as HTMLInputElement;
    value = target.value;
    dispatch('change', { value });
  }
</script>

{#if label}
  <div class="mb-4">
    <label for={inputId} class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
      {label}
      {#if required}
        <span class="text-danger-500 ml-1">*</span>
      {/if}
    </label>
    <input
      {type}
      id={inputId}
      {name}
      bind:value
      {placeholder}
      {disabled}
      {readonly}
      {required}
      class={inputClasses}
      on:input={handleInput}
      on:change={handleChange}
      on:focus
      on:blur
      {...rest}
    />
    {#if error}
      <p class="mt-1 text-sm text-danger-500">{error}</p>
    {:else if hint}
      <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{hint}</p>
    {/if}
  </div>
{:else}
  <input
    {type}
    id={inputId}
    {name}
    bind:value
    {placeholder}
    {disabled}
    {readonly}
    {required}
    class={inputClasses}
    on:input={handleInput}
    on:change={handleChange}
    on:focus
    on:blur
    {...rest}
  />
{/if}
