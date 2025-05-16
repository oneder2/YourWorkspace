<script lang="ts">
  import { page } from '$app/state'; // Updated from $app/stores to $app/state
  import { onMount } from 'svelte';

  // Define the order and display names of views for navigation
  const views = [
    { path: 'done', display: 'Done' },
    { path: 'doing', display: 'Doing' },
    { path: 'plan', display: 'Plan' }
  ];

  // Use $props rune for Svelte 5 with bindable property
  let { currentViewDisplay = $bindable('N/A') } = $props();
  let currentIndex = $state(-1);

  // Update the current view based on the pathname
  function updateCurrentView(pathname: string) {
    console.log("Current path:", pathname);

    // Try exact match first
    for (let i = 0; i < views.length; i++) {
      if (pathname === `/${views[i].path}`) {
        currentIndex = i;
        currentViewDisplay = views[i].display;
        console.log(`Exact match found: ${views[i].path}, index: ${i}`);
        return;
      }
    }

    // Try includes match if exact match fails
    for (let i = 0; i < views.length; i++) {
      if (pathname.includes(`/${views[i].path}`)) {
        currentIndex = i;
        currentViewDisplay = views[i].display;
        console.log(`Partial match found: ${views[i].path}, index: ${i}`);
        return;
      }
    }

    // No match found
    currentIndex = -1;
    currentViewDisplay = 'N/A';
    console.log("No match found");
  }

  // Initial update on mount
  onMount(() => {
    updateCurrentView(page.url.pathname);
  });

  // Update when page changes
  $effect(() => {
    updateCurrentView(page.url.pathname);
  });

  function navigateTo(direction: 'prev' | 'next') {
    try {
      // Calculate the next view index
      let nextViewIndex;

      if (currentIndex === -1) {
        // If current path is not in views array, default to first view for next, last view for prev
        nextViewIndex = direction === 'next' ? 0 : views.length - 1;
      } else {
        if (direction === 'prev') {
          nextViewIndex = (currentIndex - 1 + views.length) % views.length;
        } else { // next
          nextViewIndex = (currentIndex + 1) % views.length;
        }
      }

      // Navigate to the selected view
      const targetPath = `/${views[nextViewIndex].path}`;
      console.log(`Navigating to: ${targetPath}`);

      // 使用 try-catch 包裹导航逻辑，确保即使导航失败也不会阻塞用户界面
      try {
        // 使用 window.location 进行直接导航，确保它能正常工作
        window.location.href = targetPath;
      } catch (navError) {
        console.error('Navigation error:', navError);
        // 如果导航失败，尝试使用 history API
        window.history.pushState({}, '', targetPath);
        // 触发一个 popstate 事件，让 SvelteKit 路由器知道 URL 已更改
        window.dispatchEvent(new Event('popstate'));
      }
    } catch (error) {
      console.error('Error in navigateTo function:', error);
      // 最后的备用方案：直接设置 location.href
      window.location.href = direction === 'next' ? '/doing' : '/done';
    }
  }
</script>

<!-- Left arrow button (fixed position) -->
<div class="fixed left-8 top-1/2 transform -translate-y-1/2 z-40">
  <button
    class="inline-flex items-center justify-center p-4 bg-teal-100 hover:bg-teal-200 active:bg-teal-300 dark:bg-teal-800 dark:hover:bg-teal-700 dark:active:bg-teal-600 text-teal-800 dark:text-teal-100 font-medium rounded-full border border-teal-300 dark:border-teal-600 transition-colors shadow-lg"
    onclick={() => navigateTo('prev')}
    title="Previous: {currentIndex !== -1 && currentIndex > 0 ? views[(currentIndex - 1 + views.length) % views.length].display : views[views.length - 1].display}"
    aria-label="Go to previous section"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
  </button>
</div>

<!-- Right arrow button (fixed position) -->
<div class="fixed right-8 top-1/2 transform -translate-y-1/2 z-40">
  <button
    class="inline-flex items-center justify-center p-4 bg-teal-100 hover:bg-teal-200 active:bg-teal-300 dark:bg-teal-800 dark:hover:bg-teal-700 dark:active:bg-teal-600 text-teal-800 dark:text-teal-100 font-medium rounded-full border border-teal-300 dark:border-teal-600 transition-colors shadow-lg"
    onclick={() => navigateTo('next')}
    title="Next: {currentIndex !== -1 ? views[(currentIndex + 1) % views.length].display : views[0].display}"
    aria-label="Go to next section"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
  </button>
</div>
