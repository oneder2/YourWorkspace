/**
 * Application Initializer
 *
 * This utility handles application initialization tasks like preloading assets,
 * setting up performance monitoring, and initializing stores.
 */
import { browser } from '$app/environment';
import { preloadCriticalImages } from './imagePreloader';
import { preloadSvgIcons } from './svgUtils';
import { mark } from './performance';
import { themeStore } from '$lib/store/themeStore';

/**
 * Initialize the application
 * This should be called once when the app starts
 */
export async function initializeApp(): Promise<void> {
  if (!browser) return;

  // Start performance measurement
  mark('app-initialization-start');

  // Initialize theme from localStorage
  initializeTheme();

  // Preload critical images
  try {
    await preloadCriticalImages();
  } catch (error) {
    console.error('Failed to preload critical images:', error);
  }

  // Preload SVG icons
  try {
    await preloadSvgIcons();
  } catch (error) {
    console.error('Failed to preload SVG icons:', error);
  }

  // Register service worker if available
  registerServiceWorker();

  // End performance measurement
  mark('app-initialization-end', 'app-initialization');

  console.log('Application initialized');
}

/**
 * Initialize theme settings
 */
function initializeTheme(): void {
  // The themeStore automatically initializes from localStorage
  // Subscribe to changes to ensure DOM is updated
  const unsubscribe = themeStore.subscribe((settings) => {
    if (settings.darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }

    if (settings.customBackground) {
      document.documentElement.style.setProperty(
        '--custom-background',
        `url(${settings.customBackground})`
      );
      document.documentElement.classList.add('has-custom-bg');
      document.body.classList.add('has-background');

      // 确保背景可见
      document.body.style.backgroundColor = 'transparent';
      document.documentElement.style.backgroundColor = 'transparent';

      // 如果是暗色模式，添加特殊类
      if (settings.darkMode) {
        document.body.classList.add('dark-with-background');
      } else {
        document.body.classList.remove('dark-with-background');
      }
    } else {
      document.documentElement.style.setProperty('--custom-background', 'none');
      document.documentElement.classList.remove('has-custom-bg');
      document.body.classList.remove('has-background');

      // 恢复默认背景色
      document.body.style.backgroundColor = '';
      document.documentElement.style.backgroundColor = '';
    }
  });

  // No need to unsubscribe as we want this to persist for the app lifetime
}

/**
 * Register service worker for offline support and caching
 */
function registerServiceWorker(): void {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/service-worker.js')
        .then(registration => {
          console.log('ServiceWorker registration successful with scope:', registration.scope);
        })
        .catch(error => {
          console.error('ServiceWorker registration failed:', error);
        });
    });
  }
}
