<script lang="ts">
  import Modal from './Modal.svelte';
  import { getShortcutGroups, formatShortcut } from '$lib/utils/keyboardShortcuts';

  // Props
  let { isOpen = false } = $props<{
    isOpen: boolean;
  }>();

  // Events
  let { close } = $props<{
    close: () => void;
  }>();

  // Get all shortcut groups
  const shortcutGroups = getShortcutGroups();
</script>

<Modal {isOpen} {close} title="Keyboard Shortcuts" modalWidth="max-w-2xl">
  <div class="p-4">
    {#if shortcutGroups.length === 0}
      <p class="text-gray-500 dark:text-gray-400 text-center py-4">No keyboard shortcuts registered.</p>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        {#each shortcutGroups as group}
          <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-3">{group.name}</h3>
            <ul class="space-y-2">
              {#each group.shortcuts as shortcut}
                <li class="flex justify-between items-center">
                  <span class="text-gray-700 dark:text-gray-300">{shortcut.description}</span>
                  <kbd class="px-2 py-1 text-xs font-semibold text-gray-800 bg-gray-200 dark:text-gray-200 dark:bg-gray-700 rounded">
                    {formatShortcut(shortcut)}
                  </kbd>
                </li>
              {/each}
            </ul>
          </div>
        {/each}
      </div>
    {/if}
    
    <div class="mt-6 text-center">
      <button
        onclick={close}
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
      >
        Close
      </button>
    </div>
  </div>
</Modal>
