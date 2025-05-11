<script lang="ts">
  /**
   * Select component for dropdown selection
   * 
   * Usage:
   * ```svelte
   * <Select 
   *   label="Choose a country" 
   *   options={[
   *     { value: 'us', label: 'United States' },
   *     { value: 'ca', label: 'Canada' },
   *     { value: 'mx', label: 'Mexico' }
   *   ]} 
   * />
   * ```
   */

  // Import types
  import type { HTMLSelectAttributes } from 'svelte/elements';
  import { createEventDispatcher } from 'svelte';

  // Create event dispatcher
  const dispatch = createEventDispatcher();
  
  // Define option type
  type Option = {
    value: string | number;
    label: string;
    disabled?: boolean;
  };

  // Define option group type
  type OptionGroup = {
    label: string;
    options: Option[];
    disabled?: boolean;
  };
  
  // Define props with TypeScript types
  let {
    value = '',
    options = [],
    label = '',
    id = '',
    name = '',
    placeholder = 'Select an option',
    disabled = false,
    required = false,
    error = '',
    hint = '',
    fullWidth = true,
    class: className = '',
    ...rest
  } = $props<{
    value?: string | number;
    options?: (Option | OptionGroup)[];
    label?: string;
    id?: string;
    name?: string;
    placeholder?: string;
    disabled?: boolean;
    required?: boolean;
    error?: string;
    hint?: string;
    fullWidth?: boolean;
    class?: string;
    [key: string]: any;
  }>();

  // Generate a unique ID if not provided
  $: selectId = id || `select-${Math.random().toString(36).substring(2, 9)}`;
  
  // Compute classes based on state
  $: selectClasses = `
    block px-3 py-2 bg-white dark:bg-gray-800 
    border rounded-md shadow-sm
    focus:outline-none focus:ring-2 focus:ring-offset-0
    disabled:opacity-50 disabled:cursor-not-allowed
    ${error ? 'border-danger-500 focus:border-danger-500 focus:ring-danger-400' : 'border-gray-300 dark:border-gray-600 focus:border-primary-500 focus:ring-primary-400'}
    ${fullWidth ? 'w-full' : ''}
    ${className}
  `;

  // Check if an option is a group
  function isOptionGroup(option: Option | OptionGroup): option is OptionGroup {
    return 'options' in option && Array.isArray(option.options);
  }

  // Handle change event
  function handleChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    value = target.value;
    dispatch('change', { value });
  }
</script>

{#if label}
  <div class="mb-4">
    <label for={selectId} class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
      {label}
      {#if required}
        <span class="text-danger-500 ml-1">*</span>
      {/if}
    </label>
    <div class="relative">
      <select
        id={selectId}
        {name}
        bind:value
        {disabled}
        {required}
        class={selectClasses}
        on:change={handleChange}
        on:focus
        on:blur
        {...rest}
      >
        <option value="" disabled selected={!value}>{placeholder}</option>
        {#each options as option}
          {#if isOptionGroup(option)}
            <optgroup label={option.label} disabled={option.disabled}>
              {#each option.options as subOption}
                <option 
                  value={subOption.value} 
                  disabled={subOption.disabled}
                  selected={value === subOption.value}
                >
                  {subOption.label}
                </option>
              {/each}
            </optgroup>
          {:else}
            <option 
              value={option.value} 
              disabled={option.disabled}
              selected={value === option.value}
            >
              {option.label}
            </option>
          {/if}
        {/each}
      </select>
      <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
        <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </div>
    </div>
    {#if error}
      <p class="mt-1 text-sm text-danger-500">{error}</p>
    {:else if hint}
      <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{hint}</p>
    {/if}
  </div>
{:else}
  <div class="relative">
    <select
      id={selectId}
      {name}
      bind:value
      {disabled}
      {required}
      class={selectClasses}
      on:change={handleChange}
      on:focus
      on:blur
      {...rest}
    >
      <option value="" disabled selected={!value}>{placeholder}</option>
      {#each options as option}
        {#if isOptionGroup(option)}
          <optgroup label={option.label} disabled={option.disabled}>
            {#each option.options as subOption}
              <option 
                value={subOption.value} 
                disabled={subOption.disabled}
                selected={value === subOption.value}
              >
                {subOption.label}
              </option>
            {/each}
          </optgroup>
        {:else}
          <option 
            value={option.value} 
            disabled={option.disabled}
            selected={value === option.value}
          >
            {option.label}
          </option>
        {/if}
      {/each}
    </select>
    <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
      <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </div>
  </div>
{/if}
