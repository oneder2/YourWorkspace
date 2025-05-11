/**
 * Image Preloader Utility
 * 
 * This utility provides functions to preload images to improve page load performance.
 */

/**
 * Preloads an image by creating a new Image object and setting its src
 * 
 * @param src - The URL of the image to preload
 * @returns A promise that resolves when the image is loaded or rejects on error
 */
export function preloadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = (err) => reject(err);
    img.src = src;
  });
}

/**
 * Preloads multiple images in parallel
 * 
 * @param srcs - An array of image URLs to preload
 * @returns A promise that resolves when all images are loaded
 */
export function preloadImages(srcs: string[]): Promise<HTMLImageElement[]> {
  return Promise.all(srcs.map(preloadImage));
}

/**
 * Preloads images from CSS background properties in the DOM
 * 
 * @param selector - CSS selector to find elements with background images
 * @returns A promise that resolves when all background images are preloaded
 */
export function preloadBackgroundImages(selector: string = '[style*="background-image"]'): Promise<HTMLImageElement[]> {
  if (typeof window === 'undefined') return Promise.resolve([]);
  
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
  
  return preloadImages(urls);
}

/**
 * Preloads critical images for the application
 * This can be called on app initialization to preload common images
 */
export function preloadCriticalImages(): Promise<HTMLImageElement[]> {
  // Add paths to critical images here
  const criticalImages: string[] = [
    // Example: '/images/logo.png',
    // Example: '/images/icons/home.svg',
  ];
  
  return preloadImages(criticalImages);
}
