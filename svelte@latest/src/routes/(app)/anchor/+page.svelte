<script lang="ts">
    import { onMount } from 'svelte';
    import { anchorStore } from '$lib/store/anchorStore';
    import IdentityAnchorEditor from '$lib/components/anchor/IdentityAnchorEditor.svelte';

    // State for error handling
    let pageError = $state<string | null>(null);
    let isLoading = $state(true);

    onMount(async () => {
      try {
        console.log('Anchor page mounted, checking profile state');
        // Ensure the identity profile data is loaded when this page is mounted.
        // We check if it's not already loaded and not currently loading to avoid redundant calls.
        if (!$anchorStore.identityProfile.profile && !$anchorStore.identityProfile.isLoading) {
          console.log('Loading identity profile from anchor page');
          try {
            await anchorStore.loadIdentityProfile();
            console.log('Identity profile loaded successfully');
          } catch (loadError) {
            console.error('Error in loadIdentityProfile call:', loadError);
            if (loadError instanceof Error) {
              console.error('Error details:', {
                message: loadError.message,
                stack: loadError.stack,
                name: loadError.name
              });
            }
            throw loadError; // Re-throw to be caught by the outer catch
          }
        }
        console.log('Identity profile state after load:', {
          profile: $anchorStore.identityProfile.profile ? 'exists' : 'null',
          isLoading: $anchorStore.identityProfile.isLoading,
          error: $anchorStore.identityProfile.error
        });
      } catch (error) {
        console.error('Error loading identity profile from anchor page:', error);
        pageError = error instanceof Error ? error.message : 'An unexpected error occurred loading the profile';
      } finally {
        isLoading = false;
      }
    });
  </script>

  <div class="max-w-4xl mx-auto px-6 py-8">
    {#if isLoading}
      <div class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-500 mb-4"></div>
        <p class="text-gray-600 dark:text-gray-400">Loading your identity anchor...</p>
      </div>
    {:else if pageError}
      <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 text-center">
        <h2 class="text-xl font-semibold text-red-700 dark:text-red-400 mb-2">Error Loading Page</h2>
        <p class="text-red-600 dark:text-red-300 mb-4">{pageError}</p>
        <button
          class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md shadow-sm"
          onclick={() => window.location.reload()}
        >
          Reload Page
        </button>
      </div>
    {:else}
      <header class="text-center mb-10 pb-6 border-b border-gray-200 dark:border-gray-700">
        <span class="text-5xl block mb-2 text-primary-500" aria-hidden="true">⚓️</span>
        <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-3">My Identity Anchor</h1>
        <p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto leading-relaxed">
          This is your foundational space. Define "who you are" professionally to guide your actions,
          reflect on your journey, and plan your future with clarity.
        </p>
      </header>

      <section>
        <IdentityAnchorEditor />
      </section>
    {/if}
  </div>
