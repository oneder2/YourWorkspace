/**
 * Memoization Utility
 * 
 * This utility provides functions to memoize expensive computations.
 */

/**
 * Creates a memoized version of a function
 * 
 * @param fn - The function to memoize
 * @param keyFn - Optional function to generate a cache key from the arguments
 * @returns A memoized version of the function
 */
export function memoize<T extends (...args: any[]) => any>(
  fn: T,
  keyFn: (...args: Parameters<T>) => string = (...args) => JSON.stringify(args)
): T {
  const cache = new Map<string, ReturnType<T>>();
  
  return ((...args: Parameters<T>): ReturnType<T> => {
    const key = keyFn(...args);
    
    if (cache.has(key)) {
      return cache.get(key) as ReturnType<T>;
    }
    
    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
}

/**
 * Creates a memoized version of an async function
 * 
 * @param fn - The async function to memoize
 * @param keyFn - Optional function to generate a cache key from the arguments
 * @returns A memoized version of the async function
 */
export function memoizeAsync<T extends (...args: any[]) => Promise<any>>(
  fn: T,
  keyFn: (...args: Parameters<T>) => string = (...args) => JSON.stringify(args)
): T {
  const cache = new Map<string, Promise<Awaited<ReturnType<T>>>>();
  
  return (async (...args: Parameters<T>): Promise<Awaited<ReturnType<T>>> => {
    const key = keyFn(...args);
    
    if (cache.has(key)) {
      return cache.get(key) as Promise<Awaited<ReturnType<T>>>;
    }
    
    try {
      const resultPromise = fn(...args);
      cache.set(key, resultPromise);
      const result = await resultPromise;
      return result;
    } catch (error) {
      cache.delete(key);
      throw error;
    }
  }) as T;
}

/**
 * Creates a memoized version of a function with a time-based cache expiration
 * 
 * @param fn - The function to memoize
 * @param maxAge - The maximum age of the cache in milliseconds
 * @param keyFn - Optional function to generate a cache key from the arguments
 * @returns A memoized version of the function with time-based cache expiration
 */
export function memoizeWithExpiration<T extends (...args: any[]) => any>(
  fn: T,
  maxAge: number,
  keyFn: (...args: Parameters<T>) => string = (...args) => JSON.stringify(args)
): T {
  const cache = new Map<string, { value: ReturnType<T>; timestamp: number }>();
  
  return ((...args: Parameters<T>): ReturnType<T> => {
    const key = keyFn(...args);
    const now = Date.now();
    
    const cached = cache.get(key);
    if (cached && now - cached.timestamp < maxAge) {
      return cached.value;
    }
    
    const result = fn(...args);
    cache.set(key, { value: result, timestamp: now });
    return result;
  }) as T;
}
