/**
 * Keyboard Shortcuts Utility
 * 
 * This utility provides functions to handle keyboard shortcuts.
 */
import { browser } from '$app/environment';

export type KeyboardShortcut = {
  key: string;
  ctrlKey?: boolean;
  altKey?: boolean;
  shiftKey?: boolean;
  metaKey?: boolean;
  callback: () => void;
  description: string;
};

export type KeyboardShortcutGroup = {
  name: string;
  shortcuts: KeyboardShortcut[];
};

// Store for registered shortcuts
const shortcuts: KeyboardShortcut[] = [];
const shortcutGroups: KeyboardShortcutGroup[] = [];

/**
 * Register a keyboard shortcut
 * 
 * @param shortcut - The keyboard shortcut to register
 */
export function registerShortcut(shortcut: KeyboardShortcut): void {
  shortcuts.push(shortcut);
}

/**
 * Register a group of keyboard shortcuts
 * 
 * @param group - The keyboard shortcut group to register
 */
export function registerShortcutGroup(group: KeyboardShortcutGroup): void {
  shortcutGroups.push(group);
  group.shortcuts.forEach(shortcut => registerShortcut(shortcut));
}

/**
 * Unregister a keyboard shortcut
 * 
 * @param key - The key of the shortcut to unregister
 * @param ctrlKey - Whether the Ctrl key is required
 * @param altKey - Whether the Alt key is required
 * @param shiftKey - Whether the Shift key is required
 * @param metaKey - Whether the Meta key is required
 */
export function unregisterShortcut(
  key: string,
  ctrlKey: boolean = false,
  altKey: boolean = false,
  shiftKey: boolean = false,
  metaKey: boolean = false
): void {
  const index = shortcuts.findIndex(
    shortcut =>
      shortcut.key === key &&
      shortcut.ctrlKey === ctrlKey &&
      shortcut.altKey === altKey &&
      shortcut.shiftKey === shiftKey &&
      shortcut.metaKey === metaKey
  );
  
  if (index !== -1) {
    shortcuts.splice(index, 1);
  }
}

/**
 * Unregister a group of keyboard shortcuts
 * 
 * @param name - The name of the shortcut group to unregister
 */
export function unregisterShortcutGroup(name: string): void {
  const groupIndex = shortcutGroups.findIndex(group => group.name === name);
  
  if (groupIndex !== -1) {
    const group = shortcutGroups[groupIndex];
    group.shortcuts.forEach(shortcut => {
      unregisterShortcut(
        shortcut.key,
        shortcut.ctrlKey,
        shortcut.altKey,
        shortcut.shiftKey,
        shortcut.metaKey
      );
    });
    
    shortcutGroups.splice(groupIndex, 1);
  }
}

/**
 * Get all registered keyboard shortcuts
 * 
 * @returns All registered keyboard shortcuts
 */
export function getShortcuts(): KeyboardShortcut[] {
  return [...shortcuts];
}

/**
 * Get all registered keyboard shortcut groups
 * 
 * @returns All registered keyboard shortcut groups
 */
export function getShortcutGroups(): KeyboardShortcutGroup[] {
  return [...shortcutGroups];
}

/**
 * Format a keyboard shortcut for display
 * 
 * @param shortcut - The keyboard shortcut to format
 * @returns A formatted string representation of the shortcut
 */
export function formatShortcut(shortcut: KeyboardShortcut): string {
  const parts: string[] = [];
  
  if (shortcut.ctrlKey) parts.push('Ctrl');
  if (shortcut.altKey) parts.push('Alt');
  if (shortcut.shiftKey) parts.push('Shift');
  if (shortcut.metaKey) parts.push('Meta');
  
  parts.push(shortcut.key.toUpperCase());
  
  return parts.join(' + ');
}

/**
 * Initialize keyboard shortcuts
 * 
 * @returns A cleanup function to remove the event listener
 */
export function initKeyboardShortcuts(): () => void {
  if (!browser) return () => {};
  
  const handleKeyDown = (event: KeyboardEvent) => {
    // Ignore if the event target is an input, textarea, or select
    if (
      event.target instanceof HTMLInputElement ||
      event.target instanceof HTMLTextAreaElement ||
      event.target instanceof HTMLSelectElement
    ) {
      return;
    }
    
    const matchingShortcut = shortcuts.find(
      shortcut =>
        shortcut.key.toLowerCase() === event.key.toLowerCase() &&
        (shortcut.ctrlKey === undefined || shortcut.ctrlKey === event.ctrlKey) &&
        (shortcut.altKey === undefined || shortcut.altKey === event.altKey) &&
        (shortcut.shiftKey === undefined || shortcut.shiftKey === event.shiftKey) &&
        (shortcut.metaKey === undefined || shortcut.metaKey === event.metaKey)
    );
    
    if (matchingShortcut) {
      event.preventDefault();
      matchingShortcut.callback();
    }
  };
  
  window.addEventListener('keydown', handleKeyDown);
  
  return () => {
    window.removeEventListener('keydown', handleKeyDown);
  };
}
