/**
 * Image Preloader Utility
 *
 * This utility provides functions to preload images to improve page load performance.
 * Enhanced with priority loading, route-specific preloading, and performance tracking.
 */
import { browser } from '$app/environment';
import { mark } from './performance';

// Cache to track which images have been preloaded
const preloadedImages = new Set<string>();

// Cache to store loaded images
const imageCache = new Map<string, HTMLImageElement>();

// Priority levels for image loading
export enum ImagePriority {
  CRITICAL = 'critical',   // Must be loaded immediately (e.g., hero images, logos)
  HIGH = 'high',           // Should be loaded soon (e.g., above-the-fold images)
  MEDIUM = 'medium',       // Can be loaded after critical content (e.g., below-the-fold images)
  LOW = 'low',             // Can be loaded when idle (e.g., images in collapsed sections)
  LAZY = 'lazy'            // Only load when visible or nearly visible
}

// Interface for image preload options
interface PreloadOptions {
  priority?: ImagePriority;
  timeout?: number;
  cache?: boolean;
}

/**
 * Preloads an image by creating a new Image object and setting its src
 *
 * @param src - The URL of the image to preload
 * @param options - Options for preloading
 * @returns A promise that resolves when the image is loaded or rejects on error
 */
export function preloadImage(
  src: string,
  options: PreloadOptions = {}
): Promise<HTMLImageElement> {
  // Default options
  const {
    priority = ImagePriority.MEDIUM,
    timeout = 10000,
    cache = true
  } = options;

  // Skip if not in browser or already preloaded
  if (!browser) return Promise.resolve(new Image());
  if (preloadedImages.has(src)) {
    return Promise.resolve(imageCache.get(src) || new Image());
  }

  // Mark that we've started preloading this image
  preloadedImages.add(src);

  // Create performance mark
  mark(`image-preload-start-${src}`);

  // Create a promise that will resolve when the image is loaded
  const loadPromise = new Promise<HTMLImageElement>((resolve, reject) => {
    const img = new Image();

    // Set loading priority if supported
    if ('loading' in HTMLImageElement.prototype) {
      if (priority === ImagePriority.LAZY) {
        img.loading = 'lazy';
      } else if (priority === ImagePriority.CRITICAL || priority === ImagePriority.HIGH) {
        img.loading = 'eager';
      }
    }

    // Set fetchpriority if supported
    if ('fetchPriority' in HTMLImageElement.prototype) {
      if (priority === ImagePriority.CRITICAL) {
        (img as any).fetchPriority = 'high';
      } else if (priority === ImagePriority.LOW || priority === ImagePriority.LAZY) {
        (img as any).fetchPriority = 'low';
      }
    }

    // Set up event handlers
    img.onload = () => {
      mark(`image-preload-end-${src}`, `image-preload-${src}`);
      if (cache) {
        imageCache.set(src, img);
      }
      resolve(img);
    };

    img.onerror = (err) => {
      console.error(`Failed to preload image: ${src}`, err);
      preloadedImages.delete(src); // Allow retry
      reject(err);
    };

    // Add timeout
    if (timeout > 0) {
      setTimeout(() => {
        if (!img.complete) {
          console.warn(`Image preload timed out after ${timeout}ms: ${src}`);
          // Don't reject, as the image might still load
        }
      }, timeout);
    }

    // Start loading the image
    img.src = src;

    // If the image is already in the browser cache, it might be loaded synchronously
    if (img.complete) {
      mark(`image-preload-end-${src}`, `image-preload-${src}`);
      if (cache) {
        imageCache.set(src, img);
      }
      resolve(img);
    }
  });

  return loadPromise;
}

/**
 * Preloads multiple images in parallel with priority handling
 *
 * @param srcs - An array of image URLs to preload
 * @param options - Options for preloading
 * @returns A promise that resolves when all images are loaded
 */
export function preloadImages(
  srcs: string[],
  options: PreloadOptions = {}
): Promise<HTMLImageElement[]> {
  if (!browser || srcs.length === 0) return Promise.resolve([]);

  // Group images by priority
  const priorityGroups: Record<ImagePriority, string[]> = {
    [ImagePriority.CRITICAL]: [],
    [ImagePriority.HIGH]: [],
    [ImagePriority.MEDIUM]: [],
    [ImagePriority.LOW]: [],
    [ImagePriority.LAZY]: []
  };

  // Default all images to the provided priority
  const priority = options.priority || ImagePriority.MEDIUM;
  srcs.forEach(src => {
    priorityGroups[priority].push(src);
  });

  // Load critical and high priority images first
  const criticalPromise = Promise.all([
    ...priorityGroups[ImagePriority.CRITICAL].map(src =>
      preloadImage(src, { ...options, priority: ImagePriority.CRITICAL })
    ),
    ...priorityGroups[ImagePriority.HIGH].map(src =>
      preloadImage(src, { ...options, priority: ImagePriority.HIGH })
    )
  ]);

  // Then load medium priority images
  const mediumPromise = criticalPromise.then(() =>
    Promise.all(
      priorityGroups[ImagePriority.MEDIUM].map(src =>
        preloadImage(src, { ...options, priority: ImagePriority.MEDIUM })
      )
    )
  );

  // Finally load low and lazy priority images
  const lowPromise = mediumPromise.then(() =>
    Promise.all([
      ...priorityGroups[ImagePriority.LOW].map(src =>
        preloadImage(src, { ...options, priority: ImagePriority.LOW })
      ),
      ...priorityGroups[ImagePriority.LAZY].map(src =>
        preloadImage(src, { ...options, priority: ImagePriority.LAZY })
      )
    ])
  );

  // Return a promise that resolves when all images are loaded
  return lowPromise.then(lowImages => {
    return criticalPromise.then(criticalImages => {
      return mediumPromise.then(mediumImages => {
        return [...criticalImages, ...mediumImages, ...lowImages];
      });
    });
  });
}

/**
 * Preloads images from CSS background properties in the DOM
 *
 * @param selector - CSS selector to find elements with background images
 * @param options - Options for preloading
 * @returns A promise that resolves when all background images are preloaded
 */
export function preloadBackgroundImages(
  selector: string = '[style*="background-image"]',
  options: PreloadOptions = {}
): Promise<HTMLImageElement[]> {
  if (!browser) return Promise.resolve([]);

  const elements = document.querySelectorAll<HTMLElement>(selector);
  const urls: string[] = [];

  elements.forEach(el => {
    const style = window.getComputedStyle(el);
    const backgroundImage = style.backgroundImage;

    if (backgroundImage && backgroundImage !== 'none') {
      // Extract URL from the background-image property
      const match = /url\(['"]?([^'"]+)['"]?\)/g.exec(backgroundImage);
      if (match && match[1]) {
        urls.push(match[1]);
      }
    }
  });

  return preloadImages(urls, options);
}

/**
 * Preloads critical images for the application
 * This can be called on app initialization to preload common images
 */
export function preloadCriticalImages(): Promise<HTMLImageElement[]> {
  if (!browser) return Promise.resolve([]);

  mark('critical-images-preload-start');

  // Add paths to critical images here
  const criticalImages: string[] = [
    '/favicon.png',
    '/images/default-background.jpg',
    '/images/icons/todo.svg',
    '/images/icons/doing.svg',
    '/images/icons/done.svg',
    '/images/icons/plan.svg',
    '/images/icons/anchor.svg'
  ];

  return preloadImages(criticalImages, {
    priority: ImagePriority.CRITICAL,
    cache: true
  }).then(images => {
    mark('critical-images-preload-end', 'critical-images-preload');
    return images;
  });
}

/**
 * Preloads images for a specific route
 * This can be called when navigating to a new route
 *
 * @param route - The route to preload images for
 * @returns A promise that resolves when all route-specific images are preloaded
 */
export function preloadRouteImages(route: string): Promise<HTMLImageElement[]> {
  if (!browser) return Promise.resolve([]);

  // Map routes to images that should be preloaded
  const routeImageMap: Record<string, string[]> = {
    '/doing': [
      '/images/icons/todo.svg',
      '/images/icons/add.svg',
      '/images/icons/edit.svg'
    ],
    '/done': [
      '/images/icons/done.svg',
      '/images/icons/add.svg'
    ],
    '/plan': [
      '/images/icons/plan.svg',
      '/images/icons/add.svg'
    ],
    '/anchor': [
      '/images/icons/anchor.svg',
      '/images/icons/edit.svg'
    ]
  };

  // Get images to preload for this route
  const routeImages = routeImageMap[route] || [];

  // Skip if no images to preload
  if (routeImages.length === 0) return Promise.resolve([]);

  mark(`route-images-preload-start-${route}`);

  return preloadImages(routeImages, {
    priority: ImagePriority.HIGH,
    cache: true
  }).then(images => {
    mark(`route-images-preload-end-${route}`, `route-images-preload-${route}`);
    return images;
  });
}
