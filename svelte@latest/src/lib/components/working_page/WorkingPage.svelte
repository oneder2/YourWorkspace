<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  
  // Props for the component
  let {
    pageType = 'doing' // Default to 'doing' page
  } = $props<{
    pageType: 'doing' | 'done' | 'plan' | 'anchor'
  }>();
  
  // Reactive state to track the current page
  let currentPage = $derived(pageType);
  
  // Update the current page when the route changes
  $effect(() => {
    const path = $page.url.pathname;
    if (path.includes('/doing')) {
      currentPage = 'doing';
    } else if (path.includes('/done')) {
      currentPage = 'done';
    } else if (path.includes('/plan')) {
      currentPage = 'plan';
    } else if (path.includes('/anchor')) {
      currentPage = 'anchor';
    }
  });
  
  // Lifecycle hook
  onMount(() => {
    console.log('WorkingPage component mounted with page type:', currentPage);
  });
</script>

<div class="working-page-container" transition:fade={{ duration: 200 }}>
  <slot />
</div>

<style>
  .working-page-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
</style>
