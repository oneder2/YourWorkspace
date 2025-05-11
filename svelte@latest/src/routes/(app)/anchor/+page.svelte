<script lang="ts">
    import { onMount } from 'svelte';
    import { anchorStore } from '$lib/store/anchorStore';
    import IdentityAnchorEditor from '$lib/components/anchor/IdentityAnchorEditor.svelte';

    onMount(async () => {
      // Ensure the identity profile data is loaded when this page is mounted.
      // We check if it's not already loaded and not currently loading to avoid redundant calls.
      if (!$anchorStore.identityProfile.profile && !$anchorStore.identityProfile.isLoading) {
        await anchorStore.loadIdentityProfile();
      }
    });
  </script>

  <div class="max-w-4xl mx-auto px-6 py-8">
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
  </div>
