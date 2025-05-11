<script lang="ts">
  import { onMount, onDestroy, tick } from 'svelte';
  import Icon from '$lib/components/common/Icon.svelte';

  // --- Props ---
  export let isOpen: boolean = false;
  export let title: string = '通知'; // Default title
  export let modalWidth: string = 'max-w-lg'; // Default width
  export let showCloseButton: boolean = true;
  export let closeOnEscape: boolean = true;
  export let closeOnClickOutside: boolean = true;

  // --- Callback Props ---
  /**
   * Callback function invoked when the modal requests to be closed.
   */
  export let onClose: () => void = () => {
    console.warn("Modal: onClose prop was not provided.");
  };

  // --- Internal Functions ---
  /**
   * Closes the modal by calling the onClose prop.
   * The parent component is responsible for setting isOpen to false.
   */
  function requestCloseModal() {
    onClose(); // Call the callback prop
  }

  /**
   * Handles Escape key press to close the modal.
   */
  function handleGlobalKeydown(event: KeyboardEvent) {
    if (closeOnEscape && event.key === 'Escape' && isOpen) {
      requestCloseModal();
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
    // Ensure body overflow is reset if modal is destroyed while open
    if (typeof document !== 'undefined') {
        document.body.style.overflow = '';
    }
  });

  let previousActiveElement: HTMLElement | null = null;
  let modalElementRef: HTMLElement | null = null; // For targeting focus and backdrop interaction

  $: if (isOpen && typeof document !== 'undefined') {
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
    previousActiveElement = document.activeElement as HTMLElement; // Store previously focused element
    
    tick().then(() => { // Ensure elements are rendered
        if (modalElementRef) {
            const focusableSelector = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
            const modalContent = modalElementRef.querySelector('.modal-content-area');
            const firstFocusable = modalContent?.querySelector(focusableSelector) as HTMLElement | null;
            
            if (firstFocusable) {
                firstFocusable.focus();
            } else if (modalElementRef) {
                modalElementRef.focus();
            }
        }
    });

  } else if (!isOpen && typeof document !== 'undefined') { 
    document.body.style.overflow = ''; 
    if (previousActiveElement) {
        previousActiveElement.focus(); 
        previousActiveElement = null; 
    }
  }

  const uniqueModalIdPart = Math.random().toString(36).substring(2, 9);

</script>

{#if isOpen}
  <div
    bind:this={modalElementRef}
    id="modal-container-{uniqueModalIdPart}"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm transition-opacity duration-300 ease-in-out"
    on:click={handleBackdropClick}
    on:keydown={handleBackdropKeydown}
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-title-{uniqueModalIdPart}"
    aria-describedby={$$slots.default ? `modal-description-${uniqueModalIdPart}` : undefined}
    tabindex="-1" 
  >
    <div 
         class="modal-content-area bg-neutral-bg-card rounded-xl shadow-2xl overflow-hidden flex flex-col {modalWidth} w-full transition-transform duration-300 ease-in-out transform scale-100"
         role="document" 
         >
      <header class="flex items-center justify-between p-4 md:p-5 border-b border-neutral-border-soft">
        <h3 id="modal-title-{uniqueModalIdPart}" class="text-xl font-semibold text-neutral-text-primary">
          {title}
        </h3>
        {#if showCloseButton}
          <button
            type="button"
            on:click={requestCloseModal} 
            class="text-neutral-text-muted hover:bg-neutral-bg-hover hover:text-neutral-text-primary rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center transition-colors"
            aria-label="关闭模态框"
          >
            <Icon name="close" size="w-5 h-5" />
          </button>
        {/if}
      </header>

      <div id={$$slots.default ? `modal-description-${uniqueModalIdPart}` : undefined} class="p-4 md:p-5 space-y-4 overflow-y-auto max-h-[70vh]">
        <slot />
      </div>

      {#if $$slots.footer}
        <footer class="border-t border-neutral-border-soft">
          <slot name="footer" />
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

