<script lang="ts">
  import { onMount, onDestroy, tick } from 'svelte';
  import { fly, fade } from 'svelte/transition';

  let {
    isOpen = false,
    closeOnBackdropClick = true,
    title = null,
    modalWidth = 'max-w-lg',
    close,
    onClose = () => {}, // Event handler prop for Svelte 5
    children
  } = $props<{
    isOpen: boolean;
    closeOnBackdropClick?: boolean;
    title?: string | null;
    modalWidth?: string;
    close?: () => void;
    onClose?: () => void;
    children?: any;
  }>();

  let modalContentElement = $state<HTMLElement | null>(null); // To help manage focus

  function closeModal() {
    // Support both callback prop approaches
    close?.();
    onClose?.();
  }

  // No default export in Svelte 5 components

  // Updated to check if the click was directly on the backdrop
  function handleBackdropClick(event: MouseEvent | KeyboardEvent) { // Accept KeyboardEvent too
    if (event.currentTarget && (event.target === event.currentTarget) && closeOnBackdropClick) {
      closeModal();
    }
  }

  /**
   * Handles clicks on the backdrop to close the modal.
   * Closes only if the click is directly on the backdrop (event.target === event.currentTarget).
   */
  function handleBackdropClick(event: MouseEvent) {
    if (closeOnClickOutside && isOpen && event.target === event.currentTarget) {
      requestCloseModal();
    }
  }

  /**
   * Handles keydown on the backdrop. If Enter or Space is pressed while backdrop is focused, close modal.
   */
  function handleBackdropKeydown(event: KeyboardEvent) {
    // Check if the event target is the backdrop itself
    if (closeOnClickOutside && isOpen && event.target === event.currentTarget) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault(); // Prevent scrolling on Space
        requestCloseModal();
      }
    }
  }

  let previousActiveElement: HTMLElement | null = null;

  onMount(() => {
    if (typeof window !== 'undefined') {
      // Use global keydown for Escape as it should work regardless of focus.
      window.addEventListener('keydown', handleGlobalKeydown);
    }
  });

  onDestroy(() => {
    if (typeof window !== 'undefined') {
      window.removeEventListener('keydown', handleGlobalKeydown);
    }
    if (previousActiveElement && typeof previousActiveElement.focus === 'function') {
        previousActiveElement.focus();
    }
  });

  $effect(() => {
    if (isOpen && typeof document !== 'undefined') {
      document.body.classList.add('overflow-hidden-modal');
      if (document.activeElement instanceof HTMLElement) {
        previousActiveElement = document.activeElement;
      }
      tick().then(() => {
        if (modalContentElement) {
          const firstFocusable = modalContentElement.querySelector(
            'a[href]:not([disabled]), button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled]), details:not([disabled]), [tabindex]:not([tabindex="-1"])'
          ) as HTMLElement | null;
          if (firstFocusable) {
            firstFocusable.focus();
          } else {
            // If no focusable elements, consider focusing modalContentElement itself.
            // For this to work effectively, modalContentElement should have tabindex="-1".
            // (modalContentElement as HTMLElement).focus(); // Add tabindex="-1" to modalContentElement for this
          }
        }
      });
    } else if (!isOpen && typeof document !== 'undefined') {
      document.body.classList.remove('overflow-hidden-modal');
      if (previousActiveElement && typeof previousActiveElement.focus === 'function') {
          tick().then(() => previousActiveElement?.focus());
      }
    }
  });

  const uniqueModalIdPart = Math.random().toString(36).substring(2, 9);

</script>

{#if isOpen}
<div
  class="fixed inset-0 bg-black/60 flex justify-center items-center p-4 z-modal"
  onclick={handleBackdropClick}
  onkeydown={(event) => {
    if (event.key === 'Enter' || event.key === 'Space') {
      // Ensure the event originated from the backdrop itself if it's focused
      if (event.target === event.currentTarget) {
          handleBackdropClick(event);
          event.preventDefault(); // Prevent default space scroll, etc.
      }
    }
  }}
  transition:fade={{ duration: 200 }}
  role="dialog"
  tabindex="-1"
  aria-modal="true"
  aria-labelledby={title ? 'modal-title' : undefined}
  >
  <div
    bind:this={modalContentElement}
    class="bg-white dark:bg-gray-800 rounded-lg shadow-xl flex flex-col w-full max-h-[90vh] overflow-hidden {modalWidth}"
    role="document"
    tabindex="-1"
    transition:fly={{ y: -30, duration: 300 }}
    aria-labelledby={title ? 'modal-title' : undefined}
  >
    <header class="flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
      {#if title}
        <h2 id="modal-title" class="text-xl font-semibold text-gray-900 dark:text-white m-0">{title}</h2>
      {/if}
      <button
        class="bg-transparent border-none text-3xl font-light text-gray-500 dark:text-gray-400 cursor-pointer p-1 leading-none opacity-70 hover:opacity-100 transition-opacity"
        onclick={closeModal}
        aria-label="Close modal"
      >
        &times;
      </button>
    </header>

    <main class="p-6 overflow-y-auto flex-grow">
      {#if children?.default}
        {children.default}
      {:else}
        <p class="text-gray-700 dark:text-gray-300">This is the modal body. Pass content to override this.</p>
      {/if}
    </main>

    {#if children?.footer}
      {children.footer}
    {/if}
  </div>
{/if}

