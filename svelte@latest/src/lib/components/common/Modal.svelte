<script lang="ts">
  import { createEventDispatcher, onMount, onDestroy, tick } from 'svelte';
  import { fly, fade } from 'svelte/transition';

  export let isOpen: boolean = false;
  export let closeOnBackdropClick: boolean = true;
  export let title: string | null = null;
  export let modalWidth: string = 'max-w-lg';

  const dispatch = createEventDispatcher();
  let modalContentElement: HTMLElement; // To help manage focus

  function closeModal() {
    dispatch('close');
  }

  // Updated to check if the click was directly on the backdrop
  function handleBackdropClick(event: MouseEvent | KeyboardEvent) { // Accept KeyboardEvent too
    if (event.currentTarget && (event.target === event.currentTarget) && closeOnBackdropClick) {
      closeModal();
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape' && isOpen) {
      closeModal();
    }
    // Basic focus trapping (can be made more robust)
    if (event.key === 'Tab' && isOpen && modalContentElement) {
      const focusableElements = Array.from(
        modalContentElement.querySelectorAll(
          'a[href]:not([disabled]), button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled]), details:not([disabled]), [tabindex]:not([tabindex="-1"])'
        )
      ).filter(
        (el): el is HTMLElement => el instanceof HTMLElement && el.offsetParent !== null // Check if visible
      );

      if (focusableElements.length === 0) return;

      const firstFocusableElement = focusableElements[0];
      const lastFocusableElement = focusableElements[focusableElements.length - 1];

      if (event.shiftKey) { // Shift + Tab
        if (document.activeElement === firstFocusableElement) {
          lastFocusableElement.focus();
          event.preventDefault();
        }
      } else { // Tab
        if (document.activeElement === lastFocusableElement) {
          firstFocusableElement.focus();
          event.preventDefault();
        }
      }
    }
  }
  
  let previousActiveElement: HTMLElement | null = null;

  onMount(() => {
    window.addEventListener('keydown', handleKeydown);
  });

  onDestroy(() => {
    window.removeEventListener('keydown', handleKeydown);
    if (typeof document !== 'undefined') {
        document.body.classList.remove('overflow-hidden-modal'); // Ensure cleanup
    }
    if (previousActiveElement && typeof previousActiveElement.focus === 'function') { 
        previousActiveElement.focus(); 
    }
  });

  $: if (isOpen && typeof document !== 'undefined') {
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

</script>

{#if isOpen}
<div
  class="modal-backdrop"
  on:click={handleBackdropClick}
  on:keydown={(event) => {
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
    bind:this={modalContentElement} class="modal-content-wrapper {modalWidth}"
    role="document" 
    tabindex="-1"
    transition:fly={{ y: -30, duration: 300 }}
    aria-labelledby={title ? 'modal-title' : undefined} 
  >
    <header class="modal-header">
      {#if title}
        <h2 id="modal-title" class="modal-title-text">{title}</h2>
      {/if}
      <button
        class="modal-close-button"
        on:click={closeModal}
        aria-label="Close modal"
      >
        &times; 
      </button>
    </header>

    <main class="modal-body">
      <slot>
        <p>This is the modal body. Pass content to the default slot to override this.</p>
      </slot>
    </main>

    {#if $$slots.footer}
      <footer class="modal-footer">
        <slot name="footer"></slot>
      </footer>
    {/if}
  </div>
</div>
{/if}

<style>
/* Ensure body.overflow-hidden-modal is in global.css or a global style block */
/*
:global(body.overflow-hidden-modal) {
  overflow: hidden;
}
*/

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050; 
  padding: 1rem; 
}

.modal-content-wrapper {
  background-color: #ffffff; 
  border-radius: var(--border-radius-lg, 0.5rem); 
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  width: 100%; 
  max-height: 90vh; 
  overflow: hidden; 
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color-light, #e9ecef);
  flex-shrink: 0; 
}

.modal-title-text {
  font-size: 1.25rem; 
  font-weight: 600;   
  color: var(--text-primary, #212529);
  margin: 0;
}

.modal-close-button {
  background: none;
  border: none;
  font-size: 1.75rem;
  font-weight: 300;
  color: var(--text-secondary, #6c757d);
  cursor: pointer;
  padding: 0.25rem 0.5rem; 
  line-height: 1;
  opacity: 0.7;
  transition: opacity 0.15s ease-in-out;
}

.modal-close-button:hover {
  opacity: 1;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto; 
  flex-grow: 1;     
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border-color-light, #e9ecef);
  display: flex;
  justify-content: flex-end; 
  gap: 0.75rem; 
  background-color: var(--footer-bg, #f8f9fa); 
  flex-shrink: 0; 
}
</style>
