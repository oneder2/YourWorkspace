/**
 * Lazy Loading Utility
 * 
 * This utility provides functions to lazy load components and other resources.
 */
import { mark } from './performance';

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

/**
 * Creates a lazy loaded component with a loading fallback
 * 
 * @param loader - A function that returns a promise resolving to a component
 * @param loadingComponent - Optional component to show while loading
 * @returns A function that can be used with Svelte's dynamic imports
 */
export function lazyLoadWithFallback(
  loader: () => Promise<any>,
  loadingComponent?: any
): () => Promise<any> {
  return () => {
    mark('component-lazy-load-start');
    
    // If a loading component is provided, return it immediately
    if (loadingComponent) {
      return Promise.resolve({
        component: loadingComponent,
        loading: true
      });
    }
    
    // Otherwise, load the actual component
    return loader().then(component => {
      mark('component-lazy-load-end', 'component-lazy-load');
      return {
        component,
        loading: false
      };
    });
  };
}
