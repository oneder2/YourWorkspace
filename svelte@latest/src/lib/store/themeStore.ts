// src/lib/store/themeStore.ts

/**
 * @file themeStore.ts
 * @description Manages theme settings including dark mode and custom background
 */

import { writable, type Writable, derived, type Readable } from 'svelte/store';
import { browser } from '$app/environment';

// Define the structure for theme settings
export interface ThemeSettings {
  darkMode: boolean;
  customBackground: string | null;
}

// Define the structure for the theme store
export interface ThemeStore extends Writable<ThemeSettings> {
  toggleDarkMode: () => void;
  setCustomBackground: (url: string | null) => void;
}

// Key for localStorage
const THEME_STORAGE_KEY = 'app_theme_settings';

// Get initial state from localStorage or use defaults
function getInitialState(): ThemeSettings {
  if (browser) {
    const storedSettings = localStorage.getItem(THEME_STORAGE_KEY);
    if (storedSettings) {
      try {
        const parsedSettings = JSON.parse(storedSettings);
        return parsedSettings;
      } catch (e) {
        console.error('Failed to parse theme settings from localStorage:', e);
      }
    }

    // If no stored settings, check for system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return { darkMode: true, customBackground: null };
    }
  }

  // Default settings
  return { darkMode: false, customBackground: null };
}

// Create the underlying writable store with the initial state
const { subscribe, set, update }: Writable<ThemeSettings> = writable<ThemeSettings>(getInitialState());

// Subscribe to changes in the store and update localStorage and DOM
if (browser) {
  subscribe((settings) => {
    // Save to localStorage
    localStorage.setItem(THEME_STORAGE_KEY, JSON.stringify(settings));

    // Update DOM
    if (settings.darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }

    // Apply custom background if set
    if (settings.customBackground) {
      document.documentElement.style.setProperty('--custom-background', `url(${settings.customBackground})`);
      document.documentElement.classList.add('has-custom-bg');
      document.body.classList.add('has-background');
    } else {
      document.documentElement.style.setProperty('--custom-background', 'none');
      document.documentElement.classList.remove('has-custom-bg');
      document.body.classList.remove('has-background');
    }
  });
}

// Create and export the theme store
export const themeStore: ThemeStore = {
  subscribe,
  set,
  update,
  toggleDarkMode: () => {
    update(settings => ({ ...settings, darkMode: !settings.darkMode }));
  },
  setCustomBackground: (url: string | null) => {
    update(settings => ({ ...settings, customBackground: url }));
  }
};

// Derived stores for individual settings
export const isDarkMode: Readable<boolean> = derived(
  themeStore,
  $settings => $settings.darkMode
);

export const customBackground: Readable<string | null> = derived(
  themeStore,
  $settings => $settings.customBackground
);
