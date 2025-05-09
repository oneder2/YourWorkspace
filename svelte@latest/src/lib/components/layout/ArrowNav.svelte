<script lang="ts">
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { onDestroy } from 'svelte';

  // Define the order and display names of views for navigation
  const views = [
    { path: 'done', display: 'Done' },
    { path: 'doing', display: 'Doing' },
    { path: 'plan', display: 'Plan' }
  ];

  let currentViewDisplay = '';
  let currentIndex = -1;

  const unsubscribePage = page.subscribe(currentPage => {
    const currentPathBase = currentPage.url.pathname.split('/').pop() || '';
    currentIndex = views.findIndex(v => v.path === currentPathBase);
    if (currentIndex !== -1) {
      currentViewDisplay = views[currentIndex].display;
    } else {
      currentViewDisplay = 'N/A'; // Fallback if path doesn't match
    }
  });

  onDestroy(() => {
    unsubscribePage();
  });

  function navigateTo(direction: 'prev' | 'next') {
    if (currentIndex === -1) return; // Current path not in views array

    let nextViewIndex;
    if (direction === 'prev') {
      nextViewIndex = (currentIndex - 1 + views.length) % views.length;
    } else { // next
      nextViewIndex = (currentIndex + 1) % views.length;
    }
    // Assumes routes are like /done, /doing, /plan directly under the (app) group
    goto(`/${views[nextViewIndex].path}`);
  }
</script>

<div class="arrow-navigation-container">
  <div class="arrow-navigation">
    <button
      class="arrow-button prev-button"
      on:click={() => navigateTo('prev')}
      title="Previous: {currentIndex !== -1 && currentIndex > 0 ? views[(currentIndex - 1 + views.length) % views.length].display : views[views.length - 1].display}"
      aria-label="Go to previous section"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
      <span class="arrow-text">Prev</span>
    </button>

    <div class="current-view-indicator" aria-live="polite" aria-atomic="true">
      {currentViewDisplay}
    </div>

    <button
      class="arrow-button next-button"
      on:click={() => navigateTo('next')}
      title="Next: {currentIndex !== -1 ? views[(currentIndex + 1) % views.length].display : views[0].display}"
      aria-label="Go to next section"
    >
      <span class="arrow-text">Next</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
    </button>
  </div>
</div>

<style>
  .arrow-navigation-container {
    padding: 0.75rem 1rem; /* Padding for the container */
    background-color: var(--arrownav-bg, #ffffff); /* Background for the bar */
    border-bottom: 1px solid var(--border-color-light, #e9ecef);
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem; /* Space below the navigation */
  }
  .arrow-navigation {
    display: flex;
    justify-content: space-between; /* Pushes arrows to sides, indicator to center */
    align-items: center;
    width: 100%;
    max-width: 600px; /* Max width for the navigation itself */
    margin: 0 auto; /* Center the navigation controls */
  }

  .arrow-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: var(--arrow-button-bg, var(--primary-color, #007bff));
    color: var(--arrow-button-text-color, white);
    border: none;
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
    font-weight: 500;
    border-radius: var(--border-radius-lg, 0.5rem); /* Slightly larger radius */
    cursor: pointer;
    transition: background-color 0.2s ease-in-out, transform 0.1s ease-in-out;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
  }

  .arrow-button:hover {
    background-color: var(--arrow-button-hover-bg, #0056b3); /* Darker primary */
    transform: translateY(-1px);
  }

  .arrow-button:active {
    transform: translateY(0px);
    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
  }

  .arrow-button svg {
    width: 18px; /* Consistent icon size */
    height: 18px;
  }

  .arrow-button.prev-button svg {
    margin-right: 0.4em;
  }
  .arrow-button.next-button svg {
    margin-left: 0.4em;
  }

  .current-view-indicator {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary, #2c3e50);
    padding: 0.5rem 1.5rem;
    border: 1px solid var(--border-color, #ced4da);
    background-color: var(--indicator-bg, white);
    border-radius: var(--border-radius, 0.375rem);
    text-align: center;
    min-width: 120px; /* Ensure it has some width */
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
  }

  /* Hide text on smaller screens to save space, show only icons */
  @media (max-width: 600px) {
    .arrow-text {
      display: none;
    }
    .arrow-button svg {
      margin: 0; /* Remove margin when text is hidden */
    }
    .arrow-button {
      padding: 0.6rem 0.8rem; /* Adjust padding for icon-only button */
    }
    .current-view-indicator {
      font-size: 1rem;
      padding: 0.5rem 1rem;
      min-width: 100px;
    }
  }
</style>
