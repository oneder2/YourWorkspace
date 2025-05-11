/**
 * Performance Utilities
 * 
 * This utility provides functions to optimize and measure performance.
 */
import { browser } from '$app/environment';

/**
 * Debounce function to limit how often a function can be called
 * 
 * @param func - The function to debounce
 * @param wait - The number of milliseconds to wait
 * @returns A debounced version of the function
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout> | null = null;
  
  return function(...args: Parameters<T>): void {
    const later = () => {
      timeout = null;
      func(...args);
    };
    
    if (timeout !== null) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function to limit how often a function can be called
 * 
 * @param func - The function to throttle
 * @param limit - The number of milliseconds to wait between calls
 * @returns A throttled version of the function
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false;
  let lastFunc: ReturnType<typeof setTimeout>;
  let lastRan: number;
  
  return function(...args: Parameters<T>): void {
    if (!inThrottle) {
      func(...args);
      lastRan = Date.now();
      inThrottle = true;
      
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    } else {
      clearTimeout(lastFunc);
      lastFunc = setTimeout(() => {
        if (Date.now() - lastRan >= limit) {
          func(...args);
          lastRan = Date.now();
        }
      }, limit - (Date.now() - lastRan));
    }
  };
}

/**
 * Measures the execution time of a function
 * 
 * @param fn - The function to measure
 * @param name - Optional name for logging
 * @returns The result of the function
 */
export function measurePerformance<T>(fn: () => T, name: string = 'Function'): T {
  if (!browser) return fn();
  
  const start = performance.now();
  const result = fn();
  const end = performance.now();
  
  console.log(`${name} execution time: ${(end - start).toFixed(2)}ms`);
  
  return result;
}

/**
 * Creates a performance mark and measure
 * 
 * @param markName - The name of the mark
 * @param measureName - Optional name for the measure
 */
export function mark(markName: string, measureName?: string): void {
  if (!browser) return;
  
  performance.mark(markName);
  
  if (measureName) {
    try {
      performance.measure(measureName, markName);
    } catch (e) {
      console.error('Error creating performance measure:', e);
    }
  }
}

/**
 * Lazy loads a component
 * 
 * @param loader - A function that returns a promise resolving to a component
 * @returns A function that can be used with Svelte's dynamic imports
 */
export function lazyLoad(loader: () => Promise<any>): () => Promise<any> {
  return () => {
    mark('component-lazy-load-start');
    return loader().then(component => {
      mark('component-lazy-load-end', 'component-lazy-load');
      return component;
    });
  };
}
