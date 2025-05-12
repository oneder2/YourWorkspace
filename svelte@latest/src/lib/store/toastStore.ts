/**
 * Toast Store
 * 
 * This store manages toast notifications.
 */
import { writable } from 'svelte/store';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface Toast {
  id: string;
  type: ToastType;
  message: string;
  title?: string;
  duration?: number;
}

// Default duration in milliseconds
const DEFAULT_DURATION = 5000;

// Create the store
const { subscribe, update } = writable<Toast[]>([]);

// Generate a unique ID
function generateId(): string {
  return Math.random().toString(36).substring(2, 9);
}

/**
 * Add a toast notification
 * 
 * @param type - The type of toast
 * @param message - The message to display
 * @param title - Optional title
 * @param duration - Optional duration in milliseconds
 * @returns The ID of the toast
 */
function add(type: ToastType, message: string, title?: string, duration: number = DEFAULT_DURATION): string {
  const id = generateId();
  const toast: Toast = { id, type, message, title, duration };
  
  update(toasts => [...toasts, toast]);
  
  if (duration > 0) {
    setTimeout(() => {
      dismiss(id);
    }, duration);
  }
  
  return id;
}

/**
 * Add a success toast notification
 * 
 * @param message - The message to display
 * @param title - Optional title
 * @param duration - Optional duration in milliseconds
 * @returns The ID of the toast
 */
function success(message: string, title?: string, duration?: number): string {
  return add('success', message, title, duration);
}

/**
 * Add an error toast notification
 * 
 * @param message - The message to display
 * @param title - Optional title
 * @param duration - Optional duration in milliseconds
 * @returns The ID of the toast
 */
function error(message: string, title?: string, duration?: number): string {
  return add('error', message, title, duration);
}

/**
 * Add a warning toast notification
 * 
 * @param message - The message to display
 * @param title - Optional title
 * @param duration - Optional duration in milliseconds
 * @returns The ID of the toast
 */
function warning(message: string, title?: string, duration?: number): string {
  return add('warning', message, title, duration);
}

/**
 * Add an info toast notification
 * 
 * @param message - The message to display
 * @param title - Optional title
 * @param duration - Optional duration in milliseconds
 * @returns The ID of the toast
 */
function info(message: string, title?: string, duration?: number): string {
  return add('info', message, title, duration);
}

/**
 * Dismiss a toast notification
 * 
 * @param id - The ID of the toast to dismiss
 */
function dismiss(id: string): void {
  update(toasts => toasts.filter(toast => toast.id !== id));
}

/**
 * Dismiss all toast notifications
 */
function dismissAll(): void {
  update(() => []);
}

// Export the store
export const toastStore = {
  subscribe,
  success,
  error,
  warning,
  info,
  dismiss,
  dismissAll
};
