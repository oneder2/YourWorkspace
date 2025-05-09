<script lang="ts">
    import { onMount } from 'svelte';
    import { anchorStore } from '$lib/store/anchorStore';
    import IdentityAnchorEditor from '$lib/components/anchor/IdentityAnchorEditor.svelte';
    import { page } from '$app/stores'; // For potential use, e.g., setting document title
  
    // Subscribe to relevant parts of the anchorStore if needed directly on this page,
    // though IdentityAnchorEditor handles most of its own data display from the store.
    // For example, to show a page-level loading/error state before the editor itself renders:
    // let isLoadingProfile = false;
    // let loadError: string | null = null;
    // anchorStore.subscribe(value => {
    //   isLoadingProfile = value.identityProfile.isLoading;
    //   loadError = value.identityProfile.error;
    // });
  
    onMount(async () => {
      // Ensure the identity profile data is loaded when this page is mounted.
      // We check if it's not already loaded and not currently loading to avoid redundant calls.
      if (!$anchorStore.identityProfile.profile && !$anchorStore.identityProfile.isLoading) {
        await anchorStore.loadIdentityProfile();
      }
    });
  
    // Optionally set the document title
    // $: if ($page.url.pathname === '/anchor') { // Or /app/anchor depending on final route
    //   document.title = 'My Identity Anchor - Personal Workspace';
    // }
  </script>
  
  <div class="identity-anchor-page-container">
    <header class="page-header">
      <span class="anchor-icon" aria-hidden="true">⚓️</span>
      <h1>My Identity Anchor</h1>
      <p class="page-subtitle">
        This is your foundational space. Define "who you are" professionally to guide your actions,
        reflect on your journey, and plan your future with clarity.
      </p>
    </header>
  
    <section class="editor-section">
      <IdentityAnchorEditor />
    </section>
  
    </div>
  
  <style>
    .identity-anchor-page-container {
      padding: 1.5rem 2rem; /* Page padding */
      max-width: 900px; /* Max width for the content */
      margin: 0 auto; /* Center the content */
    }
  
    .page-header {
      text-align: center;
      margin-bottom: 2.5rem;
      padding-bottom: 1.5rem;
      border-bottom: 1px solid var(--border-color-extra-light, #f0f0f0);
    }
  
    .anchor-icon {
      font-size: 3rem; /* Large anchor icon */
      display: block;
      margin-bottom: 0.5rem;
      color: var(--primary-color, #007bff);
    }
  
    .page-header h1 {
      font-size: 2.5rem; /* Prominent H1 */
      color: var(--text-heading, #1a202c); /* Darker heading color */
      margin-bottom: 0.75rem;
      font-weight: 700;
    }
  
    .page-subtitle {
      font-size: 1.1rem;
      color: var(--text-secondary, #5a6268);
      line-height: 1.6;
      max-width: 700px; /* Subtitle width */
      margin-left: auto;
      margin-right: auto;
    }
  
    .editor-section {
      /* The IdentityAnchorEditor.svelte component has its own card styling.
         This section is just a wrapper if needed for additional layout or spacing. */
    }
  </style>
  