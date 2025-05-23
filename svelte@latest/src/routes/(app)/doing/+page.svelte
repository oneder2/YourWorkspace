<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { authStore } from '$lib/store/authStore';
  // Import main store and specific derived stores
  import { todoStore, otherActiveTodos, completedTodos, currentFocusTodos } from '$lib/store/todoStore';
  import TodoListSidebar from '$lib/components/todo/TodoListSidebar.svelte';
  import CurrentFocusDisplay from '$lib/components/anchor/current_focus/CurrentFocusDisplay.svelte';
  import {
    pageContainer,
    colorSchemes,
    layouts,
    columnSpans,
    headings,
    scrollArea,
    cardBase,
    combineClasses
  } from '$lib/styles/pageStyles';

  // 获取当前页面的颜色方案
  const pageStyle = colorSchemes.doing;

  // State variables
  let authUnsubscribe: () => void;

  // State to toggle between active and completed tasks
  let showCompletedTasks = $state(false);

  // Force reactivity by creating reactive variables that depend on store state
  let activeTodos = $derived($otherActiveTodos);
  let completedTodosLocal = $derived($completedTodos);

  onMount(async () => {
    // Subscribe to auth store to keep track of authentication state
    authUnsubscribe = authStore.subscribe(async (authState) => {
      // Only load todos if user is authenticated and we don't have data yet
      if (authState.accessToken && $todoStore.todos.length === 0 && !$todoStore.isLoading && !$todoStore.error) {
        try {
          await todoStore.loadAllTodos();
        } catch (error) {
          console.error('Failed to load todos on auth state change:', error);
        }
      }
    });

    // Initial load if already authenticated
    const currentAuth = $authStore;
    if (currentAuth.accessToken && $todoStore.todos.length === 0 && !$todoStore.isLoading && !$todoStore.error) {
      try {
        await todoStore.loadAllTodos();
      } catch (error) {
        console.error('Failed to load todos on mount:', error);
      }
    }
  });

  onDestroy(() => {
    if (authUnsubscribe) {
      authUnsubscribe();
    }
  });
</script>

<div class={combineClasses(pageContainer, "h-[calc(100vh-180px)] flex flex-col")}>
  <div class="flex-grow overflow-hidden">
    <div class={combineClasses(layouts.twoColumnOneThree, "h-full")}>
      <!-- Todo Section - Takes up 1/4 of the width on large screens -->
      <div class={combineClasses(columnSpans.oneFourth, "h-full flex flex-col")}>
        <div class={combineClasses(cardBase, pageStyle.border, "h-full flex flex-col")}>
          <div class="p-4 border-b border-gray-200 dark:border-gray-700">
            <div class="flex justify-between items-center">
              <h2 class={combineClasses(headings.h2, pageStyle.text)}>
                <svg xmlns="http://www.w3.org/2000/svg" class={combineClasses("h-5 w-5 mr-2 inline", pageStyle.icon)} viewBox="0 0 20 20" fill="currentColor">
                  <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                  <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
                </svg>
                Todo
              </h2>
              <button
                id="add-todo-button"
                class={combineClasses("p-1 text-sm rounded-md focus:outline-none focus:ring-2", pageStyle.text, pageStyle.hover)}
                aria-label="Add new todo"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Scrollable container with scrollbar indicator -->
          <div class={combineClasses(scrollArea.container, "flex-grow relative")}>
            <!-- Scrollbar indicator on the left -->
            <div class={combineClasses(scrollArea.indicator, "left-0", pageStyle.scrollbar)}></div>

            <!-- Scrollable content with fixed height and internal scrolling -->
            <div class={combineClasses("pl-3", "absolute inset-0 overflow-y-auto pr-2")}>
              {#if !showCompletedTasks}
                <TodoListSidebar todos={activeTodos} addButtonId="add-todo-button" />
              {:else}
                <TodoListSidebar todos={completedTodosLocal} addButtonId="add-todo-button" />
              {/if}
            </div>
          </div>

          <div class={combineClasses("p-4 border-t", pageStyle.border)}>
            <button
              class={combineClasses("flex items-center justify-between w-full text-left p-2 rounded-md transition-colors", pageStyle.hover)}
              onclick={() => showCompletedTasks = !showCompletedTasks}
            >
              <h3 class={combineClasses("text-lg font-medium", pageStyle.text)}>
                {showCompletedTasks ? "ACTIVE" : "PAST"}
              </h3>
              <span class={combineClasses("text-sm", pageStyle.text)}>
                {showCompletedTasks ? "Show active tasks" : "Show completed tasks"}
              </span>
            </button>
          </div>
        </div>
      </div>

      <!-- Main Focus Section - Takes up 3/4 of the width on large screens -->
      <div class={combineClasses(columnSpans.threeFourths, "h-full flex flex-col")}>
        <div class={combineClasses(cardBase, pageStyle.border, "h-full flex flex-col")}>
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <h1 class={combineClasses(headings.h1, pageStyle.text)}>
              <span class={combineClasses(pageStyle.icon, "mr-2")}>⭐</span>
              Main Focus:
            </h1>
          </div>
          <div class="p-6 flex-grow overflow-auto">
            <CurrentFocusDisplay />
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
