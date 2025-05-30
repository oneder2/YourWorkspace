// src/lib/store/notificationStore.ts

import { writable } from 'svelte/store';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface Notification {
  id: string;
  type: NotificationType;
  message: string;
  duration?: number; // 自动消失时间（毫秒），0 表示不自动消失
  dismissible?: boolean; // 是否可手动关闭
}

export interface NotificationOptions {
  duration?: number;
  dismissible?: boolean;
}

interface NotificationState {
  notifications: Notification[];
}

const initialState: NotificationState = {
  notifications: []
};

const notificationWritable = writable<NotificationState>(initialState);

// 生成唯一ID
function generateId(): string {
  return `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// 添加通知
function addNotification(
  type: NotificationType,
  message: string,
  options: NotificationOptions = {}
): string {
  // 输入验证
  if (!message || typeof message !== 'string') {
    console.warn('NotificationStore: 无效的消息内容', message);
    return '';
  }

  if (!['success', 'error', 'warning', 'info'].includes(type)) {
    console.warn('NotificationStore: 无效的通知类型', type);
    type = 'info'; // 默认为info类型
  }

  const id = generateId();
  const notification: Notification = {
    id,
    type,
    message: message.trim(),
    duration: options.duration ?? (type === 'success' ? 3000 : type === 'error' ? 5000 : 4000),
    dismissible: options.dismissible ?? true
  };

  try {
    notificationWritable.update(state => {
      // 限制同时显示的通知数量（最多5个）
      const maxNotifications = 5;
      let notifications = [...state.notifications, notification];

      if (notifications.length > maxNotifications) {
        notifications = notifications.slice(-maxNotifications);
      }

      return {
        ...state,
        notifications
      };
    });

    // 自动移除通知
    if (notification.duration && notification.duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, notification.duration);
    }
  } catch (error) {
    console.error('NotificationStore: 添加通知时发生错误', error);
    return '';
  }

  return id;
}

// 移除通知
function removeNotification(id: string): void {
  if (!id || typeof id !== 'string') {
    console.warn('NotificationStore: 无效的通知ID', id);
    return;
  }

  try {
    notificationWritable.update(state => ({
      ...state,
      notifications: state.notifications.filter(n => n.id !== id)
    }));
  } catch (error) {
    console.error('NotificationStore: 移除通知时发生错误', error);
  }
}

// 清除所有通知
function clearAllNotifications(): void {
  try {
    notificationWritable.update(state => ({
      ...state,
      notifications: []
    }));
  } catch (error) {
    console.error('NotificationStore: 清除所有通知时发生错误', error);
  }
}

// 便捷方法
const success = (message: string, options?: NotificationOptions) =>
  addNotification('success', message, options);

const error = (message: string, options?: NotificationOptions) =>
  addNotification('error', message, options);

const warning = (message: string, options?: NotificationOptions) =>
  addNotification('warning', message, options);

const info = (message: string, options?: NotificationOptions) =>
  addNotification('info', message, options);

export const notificationStore = {
  subscribe: notificationWritable.subscribe,
  addNotification,
  removeNotification,
  clearAllNotifications,
  success,
  error,
  warning,
  info
};
