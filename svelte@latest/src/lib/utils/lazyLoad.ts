/**
 * Lazy Loading Utility
 *
 * This utility provides functions to lazy load components and other resources.
 * Enhanced with prefetching capabilities for improved performance.
 */
import { mark } from './performance';
import { browser } from '$app/environment';

// Cache for loaded components
const componentCache = new Map<string, Promise<any>>();

// Track components that are being prefetched
const prefetchingComponents = new Set<string>();

/**
 * Prefetches a component without rendering it
 * This can be called in advance to load components that will be needed soon
 *
 * @param loader - A function that returns a promise resolving to a component
 * @param componentId - A unique identifier for the component (for caching)
 */
export function prefetchComponent(loader: () => Promise<any>, componentId: string): void {
  if (!browser) return;

  // Skip if already cached or prefetching
  if (componentCache.has(componentId) || prefetchingComponents.has(componentId)) {
    return;
  }

  // Mark as prefetching
  prefetchingComponents.add(componentId);

  // Start prefetching in the background
  setTimeout(() => {
    mark(`prefetch-${componentId}-start`);

    const componentPromise = loader()
      .then(component => {
        mark(`prefetch-${componentId}-end`, `prefetch-${componentId}`);
        prefetchingComponents.delete(componentId);
        return component;
      })
      .catch(error => {
        console.error(`Error prefetching component ${componentId}:`, error);
        prefetchingComponents.delete(componentId);
        throw error;
      });

    // Store in cache
    componentCache.set(componentId, componentPromise);
  }, 0);
}

/**
 * Lazy loads a component with caching
 *
 * @param loader - A function that returns a promise resolving to a component
 * @param componentId - A unique identifier for the component (for caching)
 * @returns A function that can be used with Svelte's dynamic imports
 */
export function lazyLoad(
  loader: () => Promise<any>,
  componentId?: string
): () => Promise<any> {
  return () => {
    mark('component-lazy-load-start');

    // Use cache if available and component ID is provided
    if (componentId && componentCache.has(componentId)) {
      return componentCache.get(componentId)!;
    }

    // Load the component
    const componentPromise = loader().then(component => {
      mark('component-lazy-load-end', 'component-lazy-load');
      return component;
    });

    // Cache the component if ID is provided
    if (componentId) {
      componentCache.set(componentId, componentPromise);
    }

    return componentPromise;
  };
}

/**
 * Creates a lazy loaded component with a loading fallback
 *
 * @param loader - A function that returns a promise resolving to a component
 * @param options - Configuration options
 * @returns A function that can be used with Svelte's dynamic imports
 */
export function lazyLoadWithFallback(
  loader: () => Promise<any>,
  options?: {
    loadingComponent?: any;
    componentId?: string;
    timeout?: number;
    errorComponent?: any;
  }
): () => Promise<any> {
  const {
    loadingComponent,
    componentId,
    timeout = 10000,
    errorComponent
  } = options || {};

  return () => {
    mark('component-lazy-load-start');

    // If a loading component is provided, return it immediately
    if (loadingComponent) {
      // Use cache if available and component ID is provided
      if (componentId && componentCache.has(componentId)) {
        return componentCache.get(componentId)!.then(component => ({
          component,
          loading: false
        })).catch(error => {
          console.error(`Error loading component ${componentId}:`, error);
          return {
            component: errorComponent || loadingComponent,
            loading: false,
            error
          };
        });
      }

      // Create a promise that will resolve with the loaded component
      const componentPromise = new Promise((resolve, reject) => {
        // Start loading the component
        const loadPromise = loader().then(component => {
          mark('component-lazy-load-end', 'component-lazy-load');
          resolve({
            component,
            loading: false
          });
        }).catch(error => {
          console.error('Error lazy loading component:', error);
          if (errorComponent) {
            resolve({
              component: errorComponent,
              loading: false,
              error
            });
          } else {
            reject(error);
          }
        });

        // Add timeout if specified
        if (timeout > 0) {
          setTimeout(() => {
            loadPromise.catch(() => {
              // Only reject if the component hasn't loaded yet
              reject(new Error(`Component loading timed out after ${timeout}ms`));
            });
          }, timeout);
        }
      });

      // Cache the component if ID is provided
      if (componentId) {
        componentCache.set(componentId, componentPromise);
      }

      // Return the loading component immediately
      return Promise.resolve({
        component: loadingComponent,
        loading: true,
        promise: componentPromise
      });
    }

    // Otherwise, load the actual component
    return loader().then(component => {
      mark('component-lazy-load-end', 'component-lazy-load');
      return component;
    }).catch(error => {
      console.error('Error lazy loading component:', error);
      if (errorComponent) {
        return errorComponent;
      }
      throw error;
    });
  };
}

/**
 * Prefetches components for a specific route
 * Call this when hovering over links or when a route is likely to be visited soon
 *
 * @param route - The route to prefetch components for
 */
export function prefetchRoute(route: string): void {
  if (!browser) return;

  // Map routes to component IDs that should be prefetched
  const routeComponentMap: Record<string, string[]> = {
    '/doing': ['todo-page', 'todo-list', 'todo-item'],
    '/done': ['done-page', 'achievement-list', 'achievement-item'],
    '/plan': ['plan-page', 'plan-list', 'plan-item'],
    '/anchor': ['anchor-page', 'identity-editor']
  };

  // Get components to prefetch for this route
  const componentIds = routeComponentMap[route] || [];

  // Prefetch each component
  componentIds.forEach(componentId => {
    // This would need to be mapped to actual loaders in a real implementation
    // For now, we'll just log that we would prefetch these components
    console.log(`Would prefetch component: ${componentId} for route: ${route}`);

    // Example of how this would be used:
    // prefetchComponent(() => import(`$lib/components/${componentId}.svelte`), componentId);
  });
}
