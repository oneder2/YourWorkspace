<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { authStore, type UserProfile } from '$lib/store/authStore';
  // Import main store and specific derived stores
  import { todoStore, otherActiveTodos, completedTodos } from '$lib/store/todoStore';
  import TodoList from '$lib/components/todo/TodoList.svelte';
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
  let currentUser: UserProfile | null = null;
  let authUnsubscribe: () => void;

  // State to toggle between active and completed tasks
  let showCompletedTasks = $state(false);

  onMount(async () => {
    if ($todoStore.todos.length === 0 && !$todoStore.isLoading) {
      await todoStore.loadAllTodos();
    }
  });

  function handleTodoAdded() {
    showAddTodoForm = false;
    console.log("Todo added successfully from page, hiding form.");
  }

  /**
   * Handles edit requests. Now receives the item directly.
   * @param {TodoItemType} item - The todo item to edit.
   */
  function handleGlobalEditRequest(item: TodoItemType) { // No longer CustomEvent
    console.log('Global Edit Request for:', item);
    if (item && typeof item === 'object' && 'id' in item) {
        todoToEditGlobal = item;
        isEditModalOpenGlobal = true;
    } else {
        console.error("Invalid item passed to handleGlobalEditRequest:", item);
        handleActionError({ message: "无法编辑该项目：数据无效。" });
    }
  }

  function closeGlobalEditModal() {
    isEditModalOpenGlobal = false;
    todoToEditGlobal = null;
  }

  function handleGlobalEditSaveSuccess(event: CustomEvent<TodoItemType>) {
    console.log('Global Edit Saved:', event.detail);
    closeGlobalEditModal();
  }

  function handleGlobalEditError(event: CustomEvent<{ message: string }>) {
    console.error('Global Edit Error:', event.detail.message);
    handleActionError({ message: `编辑失败: ${event.detail.message}` });
  }

  /**
   * Handles delete requests. Now receives the id directly.
   * @param {number} id - The ID of the todo item to delete.
   */
  async function handleDeleteRequest(id: number) { // No longer CustomEvent
    console.log('Request to delete todo in /doing page with id:', id);
    try {
      await todoStore.removeTodo(id);
    } catch (e: unknown) {
      console.error('Failed to delete todo from page:', e);
      const message = e instanceof Error ? `删除待办事项失败: ${e.message}` : `删除待办事项失败: 未知错误`;
      handleActionError({ message });
    }
  }
  
  /**
   * Handles generic action errors. Now receives the detail object directly.
   * @param {{ message: string }} detail - An object containing the error message.
   */
  function handleActionError(detail: { message: string }) { // No longer CustomEvent
    console.error('Action Error on /doing page:', detail.message);
    alert(`操作错误: ${detail.message}`);
  }
</script>

<div class={pageContainer}>
  <div class={layouts.threeColumn}>
    <!-- Main Focus Section - Takes up 2/3 of the width on medium screens and up -->
    <div class={columnSpans.twoThirds}>
      <section id="current-focus-section" class={combineClasses("mb-6 p-6 rounded-lg shadow", cardBase, pageStyle.bg, pageStyle.border)}>
        <h2 class={combineClasses(headings.h2, pageStyle.text)}>
          <span class={combineClasses(pageStyle.icon, "mr-2")}>⭐</span>
          Main Focus:
        </h2>
        <CurrentFocusDisplay />
      </section>
    </div>

    <!-- Todo Section - Takes up 1/3 of the width on medium screens and up -->
    <div class={columnSpans.oneThird}>
      <section id="todo-section" class={combineClasses("mb-6 p-6 rounded-lg shadow", cardBase, pageStyle.bg, pageStyle.border)}>
        <h2 class={combineClasses(headings.h2, pageStyle.text)}>
          <svg xmlns="http://www.w3.org/2000/svg" class={combineClasses("h-5 w-5 mr-2", pageStyle.icon)} viewBox="0 0 20 20" fill="currentColor">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
          </svg>
          Todo
        </h2>
        <div>
          <!-- Scrollable container with scrollbar indicator -->
          <div class={scrollArea.container}>
            <!-- Scrollbar indicator on the right -->
            <div class={combineClasses("absolute right-0 top-0 bottom-0 w-1 opacity-50", pageStyle.scrollbar)}></div>

            <!-- Scrollable content -->
            <div class={combineClasses("pr-3", scrollArea.content)}>
              {#if !showCompletedTasks}
                <TodoList todos={$otherActiveTodos} />
              {:else}
                <TodoList todos={$completedTodos} />
              {/if}
            </div>
          </div>

          <div class={combineClasses("mt-4 pt-4 border-t", pageStyle.border)}>
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
      </section>
    </div>
  </div>
</div>
