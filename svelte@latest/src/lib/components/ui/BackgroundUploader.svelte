<script lang="ts">
  /**
   * Background Uploader component for setting a custom background image
   *
   * Usage:
   * ```svelte
   * <BackgroundUploader />
   * ```
   */
  import { themeStore, customBackground } from '$lib/store/themeStore';
  import { onMount } from 'svelte';
  import { slide } from 'svelte/transition';

  // Props
  let {
    class: className = '',
    ...rest
  } = $props<{
    class?: string;
    [key: string]: any;
  }>();

  // State
  let isOpen = $state(false);
  let fileInput = $state<HTMLInputElement | null>(null);
  let dragActive = $state(false);
  let previewUrl = $state<string | null>(null);
  let errorMessage = $state<string | null>(null);

  // Initialize preview from store
  onMount(() => {
    previewUrl = $customBackground;
  });

  // Toggle panel
  function togglePanel() {
    isOpen = !isOpen;
  }

  // Handle file selection
  function handleFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      processFile(input.files[0]);
    }
  }

  // Handle drag events
  function handleDragEnter(event: DragEvent) {
    event.preventDefault();
    dragActive = true;
  }

  function handleDragLeave(event: DragEvent) {
    event.preventDefault();
    dragActive = false;
  }

  function handleDragOver(event: DragEvent) {
    event.preventDefault();
    dragActive = true;
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    dragActive = false;

    if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
      processFile(event.dataTransfer.files[0]);
    }
  }

  // Process the selected file
  function processFile(file: File) {
    errorMessage = null;
    console.log('Processing file:', file.name, file.type, file.size);

    // Check file type
    if (!file.type.startsWith('image/')) {
      errorMessage = 'Please select an image file.';
      console.error('Invalid file type:', file.type);
      return;
    }

    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      errorMessage = 'Image size should be less than 5MB.';
      console.error('File too large:', file.size);
      return;
    }

    try {
      // Create object URL for preview
      const url = URL.createObjectURL(file);
      previewUrl = url;
      console.log('Preview URL created:', url);

      // Convert to base64 for storage
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const base64String = e.target?.result as string;
          if (!base64String) {
            throw new Error('Failed to convert image to base64');
          }

          console.log('Base64 string created (length):', base64String.length);

          // Store in theme store
          themeStore.setCustomBackground(base64String);
          console.log('Background set in theme store');

          // Apply the background immediately
          document.documentElement.style.setProperty('--custom-background', `url(${base64String})`);
          console.log('Background applied to document element');

          // 强制触发重绘
          document.documentElement.classList.add('has-custom-bg');

          // 验证样式是否被应用
          const appliedStyle = document.documentElement.style.getPropertyValue('--custom-background');
          console.log('Applied style value:', appliedStyle);

          // 检查 localStorage 中是否正确保存
          setTimeout(() => {
            const storedSettings = localStorage.getItem('app_theme_settings');
            if (storedSettings) {
              const settings = JSON.parse(storedSettings);
              console.log('Stored background in localStorage:', settings.customBackground ? 'exists (length: ' + settings.customBackground.length + ')' : 'none');
            }
          }, 100);
        } catch (err) {
          console.error('Error in reader.onload:', err);
          errorMessage = 'Error processing image data.';
        }
      };

      reader.onerror = (e) => {
        console.error('Error reading file:', e);
        errorMessage = 'Error processing image file.';
      };

      reader.readAsDataURL(file);
    } catch (err) {
      console.error('Error in processFile:', err);
      errorMessage = 'Failed to process the image.';
    }
  }

  // Clear background
  function clearBackground() {
    try {
      previewUrl = null;
      themeStore.setCustomBackground(null);

      // Remove the background immediately
      document.documentElement.style.setProperty('--custom-background', 'none');

      // 移除自定义背景标记类
      document.documentElement.classList.remove('has-custom-bg');

      console.log('Background cleared successfully');

      // 验证 localStorage 中的设置是否已更新
      setTimeout(() => {
        const storedSettings = localStorage.getItem('app_theme_settings');
        if (storedSettings) {
          const settings = JSON.parse(storedSettings);
          console.log('Background in localStorage after clearing:', settings.customBackground);
        }
      }, 100);
    } catch (err) {
      console.error('Error clearing background:', err);
      errorMessage = 'Failed to clear background.';
    }
  }
</script>

<div class={`relative ${className}`} {...rest}>
  <button
    type="button"
    class="inline-flex items-center justify-center font-medium rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed px-3 py-1.5 text-xs border border-gray-300 bg-transparent text-gray-700 hover:bg-gray-50 focus:ring-gray-400 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800 flex items-center"
    onclick={togglePanel}
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
    </svg>
    Background
  </button>

  {#if isOpen}
    <div
      class="absolute right-0 mt-2 w-72 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50 p-4"
      transition:slide={{ duration: 200 }}
    >
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100">Custom Background</h3>
        <button
          class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          onclick={togglePanel}
          aria-label="Close panel"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Drag and drop area -->
      <div
        role="button"
        tabindex="0"
        class={`border-2 border-dashed rounded-lg p-4 text-center cursor-pointer mb-3 ${
          dragActive
            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
            : 'border-gray-300 dark:border-gray-600 hover:border-primary-400 dark:hover:border-primary-500'
        }`}
        onclick={() => fileInput?.click()}
        onkeydown={(e) => e.key === 'Enter' && fileInput?.click()}
        ondragenter={handleDragEnter}
        ondragleave={handleDragLeave}
        ondragover={handleDragOver}
        ondrop={handleDrop}
      >
        <input
          type="file"
          accept="image/*"
          class="hidden"
          bind:this={fileInput}
          onchange={handleFileSelect}
        />

        {#if previewUrl}
          <div class="relative w-full h-32 mb-2">
            <img
              src={previewUrl}
              alt="Background preview"
              class="w-full h-full object-cover rounded"
            />
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400">Click or drag to change image</p>
        {:else}
          <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-10 w-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Click to select or drag an image here</p>
          <p class="text-xs text-gray-400 dark:text-gray-500">PNG, JPG, GIF up to 5MB</p>
        {/if}
      </div>

      {#if errorMessage}
        <div class="text-sm text-red-500 mb-3">{errorMessage}</div>
      {/if}

      <div class="flex justify-between">
        <button
          type="button"
          class="inline-flex items-center justify-center font-medium rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed px-3 py-1.5 text-xs border border-gray-300 bg-transparent text-gray-700 hover:bg-gray-50 focus:ring-gray-400 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800"
          onclick={clearBackground}
          disabled={!previewUrl}
        >
          Clear
        </button>
        <button
          type="button"
          class="inline-flex items-center justify-center font-medium rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed px-3 py-1.5 text-xs bg-primary-500 text-white hover:bg-primary-600 focus:ring-primary-400 dark:bg-primary-600 dark:hover:bg-primary-700"
          onclick={togglePanel}
        >
          Done
        </button>
      </div>
    </div>
  {/if}
</div>
