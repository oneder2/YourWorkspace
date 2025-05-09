<script lang="ts">
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    // import { uiStore } from '$lib/store/uiStore'; // If using uiStore for navigation logic
  
    // Define the order of views for navigation
    const viewOrder = ['done', 'doing', 'plan']; // Corresponds to route paths like /done, /doing, /plan
  
    function getCurrentViewIndex(): number {
      const currentPathBase = $page.url.pathname.split('/').pop() || '';
      return viewOrder.indexOf(currentPathBase);
    }
  
    function navigateTo(direction: 'prev' | 'next') {
      const currentIndex = getCurrentViewIndex();
      if (currentIndex === -1) return; // Current path not in viewOrder
  
      let nextIndex;
      if (direction === 'prev') {
        nextIndex = (currentIndex - 1 + viewOrder.length) % viewOrder.length;
      } else {
        nextIndex = (currentIndex + 1) % viewOrder.length;
      }
      goto(`/${viewOrder[nextIndex]}`); // Assumes routes are like /app/done, /app/doing, /app/plan
                                        // If your routes are directly /done, /doing, /plan under (app) group, this is fine.
                                        // If they are nested like /app/done, adjust goto path.
    }
  
    // For uiStore based navigation (as per phase1frame.txt):
    // function handlePrev() {
    //   uiStore.goPreviousView($page.url.pathname);
    // }
    // function handleNext() {
    //   uiStore.goNextView($page.url.pathname);
    // }
  </script>
  
  <div class="arrow-navigation">
    <button class="arrow-button prev-button" on:click={() => navigateTo('prev')} title="Previous View">
      &larr; </button>
    <span class="current-view-indicator">
      Page: {$page.url.pathname.split('/').pop() || 'N/A'}
    </span>
    <button class="arrow-button next-button" on:click={() => navigateTo('next')} title="Next View">
      &rarr; </button>
  </div>
  
  <style>
    .arrow-navigation {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 1rem 0;
      margin-bottom: 1rem; /* Space below the arrows */
      background-color: var(--light-color, #f8f9fa); /* Light background for the nav bar */
      border-bottom: 1px solid #e0e0e0;
    }
  
    .arrow-button {
      background-color: var(--primary-color, #007bff);
      color: white;
      border: none;
      padding: 0.6rem 1.2rem;
      font-size: 1.2rem; /* Larger arrows */
      font-weight: bold;
      border-radius: var(--border-radius, 0.375rem);
      cursor: pointer;
      transition: background-color 0.2s ease;
      margin: 0 1rem; /* Space around buttons */
    }
  
    .arrow-button:hover {
      background-color: #0056b3; /* Darker primary color */
    }
  
    .current-view-indicator {
      font-size: 1rem;
      font-weight: 500;
      color: var(--text-primary, #333);
      padding: 0.5rem 1rem;
      border: 1px solid #ccc;
      border-radius: var(--border-radius, 0.375rem);
      background-color: white;
      min-width: 100px; /* Give it some space */
      text-align: center;
      text-transform: capitalize;
    }
  </style>
  