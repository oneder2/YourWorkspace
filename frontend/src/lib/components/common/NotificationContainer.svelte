<!-- src/lib/components/common/NotificationContainer.svelte -->
<script lang="ts">
  import { notificationStore, type Notification, type NotificationType } from '$lib/store/notificationStore';
  import { fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';

  // 使用$derived安全地获取通知状态
  const notifications = $derived.by(() => {
    try {
      const state = $notificationStore;
      return state?.notifications || [];
    } catch (error) {
      console.error('NotificationContainer: 获取通知状态时发生错误', error);
      return [];
    }
  });

  function getNotificationClasses(type: NotificationType): string {
    const baseClasses = 'flex items-center justify-between p-4 rounded-lg shadow-lg border max-w-md w-full';

    switch (type) {
      case 'success':
        return `${baseClasses} bg-green-100 dark:bg-green-800/80 text-green-900 dark:text-green-100 border-green-300 dark:border-green-600`;
      case 'error':
        return `${baseClasses} bg-red-100 dark:bg-red-800/80 text-red-900 dark:text-red-100 border-red-300 dark:border-red-600`;
      case 'warning':
        return `${baseClasses} bg-yellow-100 dark:bg-yellow-800/80 text-yellow-900 dark:text-yellow-100 border-yellow-300 dark:border-yellow-600`;
      case 'info':
        return `${baseClasses} bg-blue-100 dark:bg-blue-800/80 text-blue-900 dark:text-blue-100 border-blue-300 dark:border-blue-600`;
      default:
        return `${baseClasses} bg-gray-100 dark:bg-gray-800/80 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600`;
    }
  }

  function getIconClasses(type: NotificationType): string {
    switch (type) {
      case 'success':
        return 'text-green-700 dark:text-green-200';
      case 'error':
        return 'text-red-700 dark:text-red-200';
      case 'warning':
        return 'text-yellow-700 dark:text-yellow-200';
      case 'info':
        return 'text-blue-700 dark:text-blue-200';
      default:
        return 'text-gray-700 dark:text-gray-200';
    }
  }

  function getIcon(type: NotificationType): string {
    switch (type) {
      case 'success':
        return '✓';
      case 'error':
        return '✕';
      case 'warning':
        return '⚠';
      case 'info':
        return 'ℹ';
      default:
        return '•';
    }
  }

  function handleDismiss(id: string): void {
    try {
      if (!id) {
        console.warn('NotificationContainer: 尝试关闭无效的通知ID');
        return;
      }
      notificationStore.removeNotification(id);
    } catch (error) {
      console.error('NotificationContainer: 关闭通知时发生错误', error);
    }
  }
</script>

<!-- 通知容器 -->
<div class="notification-container fixed top-4 left-1/2 transform -translate-x-1/2 flex flex-col gap-2 pointer-events-none">
  {#each notifications as notification (notification.id)}
    <div
      class="{getNotificationClasses(notification.type)} pointer-events-auto"
      transition:fly={{ y: -20, duration: 300, easing: quintOut }}
    >
      <!-- 图标和消息 -->
      <div class="flex items-center gap-3">
        <div class="{getIconClasses(notification.type)} text-lg font-bold">
          {getIcon(notification.type)}
        </div>
        <span class="text-sm font-medium flex-1">
          {notification.message}
        </span>
      </div>

      <!-- 关闭按钮 -->
      {#if notification.dismissible}
        <button
          type="button"
          onclick={() => handleDismiss(notification.id)}
          class="ml-3 flex-shrink-0 rounded-full p-1 hover:bg-black/10 dark:hover:bg-white/10 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-current"
          aria-label="关闭通知"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
          </svg>
        </button>
      {/if}
    </div>
  {/each}
</div>

<style>
  /* 确保通知在所有内容之上 */
  :global(.notification-container) {
    z-index: 999999 !important;
    position: fixed !important;
    top: 1rem !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    pointer-events: none !important;
  }

  /* 确保通知项本身可以交互 */
  :global(.notification-container > *) {
    pointer-events: auto !important;
    z-index: 999999 !important;
    position: relative !important;
  }

  /* 确保在所有可能的容器之上 */
  :global(body .notification-container) {
    z-index: 999999 !important;
  }
</style>
