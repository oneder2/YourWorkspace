/**
 * Data Cache Utility
 * 
 * This utility provides a caching mechanism for API data to improve performance
 * and reduce unnecessary network requests.
 */
import { browser } from '$app/environment';
import { mark } from './performance';

// Cache entry interface
interface CacheEntry<T> {
  data: T;
  timestamp: number;
  expiresAt: number;
}

// Cache options interface
export interface CacheOptions {
  /** Time in milliseconds before the cache entry expires (default: 5 minutes) */
  ttl?: number;
  /** Whether to persist the cache in localStorage (default: false) */
  persist?: boolean;
  /** Custom key prefix for localStorage (default: 'app_data_cache') */
  storageKeyPrefix?: string;
  /** Whether to use the cache when offline (default: true) */
  useWhenOffline?: boolean;
  /** Whether to refresh the cache in the background (default: true) */
  backgroundRefresh?: boolean;
}

// Default cache options
const DEFAULT_OPTIONS: CacheOptions = {
  ttl: 5 * 60 * 1000, // 5 minutes
  persist: false,
  storageKeyPrefix: 'app_data_cache',
  useWhenOffline: true,
  backgroundRefresh: true
};

// In-memory cache
const memoryCache = new Map<string, CacheEntry<any>>();

/**
 * Generates a cache key from the endpoint and params
 * 
 * @param endpoint - The API endpoint
 * @param params - Optional parameters
 * @returns A unique cache key
 */
function generateCacheKey(endpoint: string, params?: any): string {
  if (!params) return endpoint;
  
  // Sort keys to ensure consistent cache keys
  const sortedParams = Object.keys(params).sort().reduce(
    (result, key) => {
      result[key] = params[key];
      return result;
    },
    {} as Record<string, any>
  );
  
  return `${endpoint}:${JSON.stringify(sortedParams)}`;
}

/**
 * Saves data to the cache
 * 
 * @param key - The cache key
 * @param data - The data to cache
 * @param options - Cache options
 */
function saveToCache<T>(key: string, data: T, options: CacheOptions): void {
  const { ttl, persist, storageKeyPrefix } = { ...DEFAULT_OPTIONS, ...options };
  
  const now = Date.now();
  const entry: CacheEntry<T> = {
    data,
    timestamp: now,
    expiresAt: now + (ttl || 0)
  };
  
  // Save to memory cache
  memoryCache.set(key, entry);
  
  // Save to localStorage if persistence is enabled
  if (browser && persist && storageKeyPrefix) {
    try {
      localStorage.setItem(`${storageKeyPrefix}:${key}`, JSON.stringify(entry));
    } catch (error) {
      console.error('Failed to save cache to localStorage:', error);
    }
  }
}

/**
 * Gets data from the cache
 * 
 * @param key - The cache key
 * @param options - Cache options
 * @returns The cached data or null if not found or expired
 */
function getFromCache<T>(key: string, options: CacheOptions): T | null {
  const { persist, storageKeyPrefix, useWhenOffline } = { ...DEFAULT_OPTIONS, ...options };
  
  // Check memory cache first
  if (memoryCache.has(key)) {
    const entry = memoryCache.get(key) as CacheEntry<T>;
    
    // Check if entry is expired
    if (entry.expiresAt > Date.now() || (useWhenOffline && !navigator.onLine)) {
      return entry.data;
    }
    
    // Remove expired entry
    memoryCache.delete(key);
  }
  
  // Check localStorage if persistence is enabled
  if (browser && persist && storageKeyPrefix) {
    try {
      const storedEntry = localStorage.getItem(`${storageKeyPrefix}:${key}`);
      
      if (storedEntry) {
        const entry = JSON.parse(storedEntry) as CacheEntry<T>;
        
        // Check if entry is expired
        if (entry.expiresAt > Date.now() || (useWhenOffline && !navigator.onLine)) {
          // Restore to memory cache
          memoryCache.set(key, entry);
          return entry.data;
        }
        
        // Remove expired entry
        localStorage.removeItem(`${storageKeyPrefix}:${key}`);
      }
    } catch (error) {
      console.error('Failed to get cache from localStorage:', error);
    }
  }
  
  return null;
}

/**
 * Clears the cache for a specific key or all cache if no key is provided
 * 
 * @param key - Optional cache key to clear
 * @param options - Cache options
 */
export function clearCache(key?: string, options?: CacheOptions): void {
  const { persist, storageKeyPrefix } = { ...DEFAULT_OPTIONS, ...options };
  
  if (key) {
    // Clear specific key
    memoryCache.delete(key);
    
    if (browser && persist && storageKeyPrefix) {
      localStorage.removeItem(`${storageKeyPrefix}:${key}`);
    }
  } else {
    // Clear all cache
    memoryCache.clear();
    
    if (browser && persist && storageKeyPrefix) {
      // Clear only items with the specified prefix
      for (let i = 0; i < localStorage.length; i++) {
        const storageKey = localStorage.key(i);
        if (storageKey && storageKey.startsWith(`${storageKeyPrefix}:`)) {
          localStorage.removeItem(storageKey);
        }
      }
    }
  }
}

/**
 * Fetches data with caching
 * 
 * @param endpoint - The API endpoint
 * @param fetchFn - The function to fetch data if not in cache
 * @param params - Optional parameters
 * @param options - Cache options
 * @returns A promise that resolves with the data
 */
export async function fetchWithCache<T>(
  endpoint: string,
  fetchFn: () => Promise<T>,
  params?: any,
  options: CacheOptions = {}
): Promise<T> {
  const mergedOptions = { ...DEFAULT_OPTIONS, ...options };
  const cacheKey = generateCacheKey(endpoint, params);
  
  mark(`cache-fetch-start-${cacheKey}`);
  
  // Try to get from cache first
  const cachedData = getFromCache<T>(cacheKey, mergedOptions);
  
  if (cachedData) {
    mark(`cache-fetch-hit-${cacheKey}`, `cache-fetch-${cacheKey}`);
    console.log(`Cache hit for ${cacheKey}`);
    
    // Refresh cache in background if enabled and online
    if (mergedOptions.backgroundRefresh && browser && navigator.onLine) {
      setTimeout(async () => {
        try {
          const freshData = await fetchFn();
          saveToCache(cacheKey, freshData, mergedOptions);
          console.log(`Background refresh completed for ${cacheKey}`);
        } catch (error) {
          console.error(`Background refresh failed for ${cacheKey}:`, error);
        }
      }, 0);
    }
    
    return cachedData;
  }
  
  // Cache miss, fetch fresh data
  mark(`cache-fetch-miss-${cacheKey}`);
  console.log(`Cache miss for ${cacheKey}`);
  
  try {
    const data = await fetchFn();
    saveToCache(cacheKey, data, mergedOptions);
    mark(`cache-fetch-end-${cacheKey}`, `cache-fetch-${cacheKey}`);
    return data;
  } catch (error) {
    mark(`cache-fetch-error-${cacheKey}`, `cache-fetch-${cacheKey}`);
    console.error(`Fetch failed for ${cacheKey}:`, error);
    throw error;
  }
}

/**
 * Prefetches data and stores it in the cache
 * 
 * @param endpoint - The API endpoint
 * @param fetchFn - The function to fetch data
 * @param params - Optional parameters
 * @param options - Cache options
 */
export async function prefetchData<T>(
  endpoint: string,
  fetchFn: () => Promise<T>,
  params?: any,
  options: CacheOptions = {}
): Promise<void> {
  const cacheKey = generateCacheKey(endpoint, params);
  
  mark(`prefetch-start-${cacheKey}`);
  console.log(`Prefetching data for ${cacheKey}`);
  
  try {
    const data = await fetchFn();
    saveToCache(cacheKey, data, { ...DEFAULT_OPTIONS, ...options });
    mark(`prefetch-end-${cacheKey}`, `prefetch-${cacheKey}`);
    console.log(`Prefetch completed for ${cacheKey}`);
  } catch (error) {
    mark(`prefetch-error-${cacheKey}`, `prefetch-${cacheKey}`);
    console.error(`Prefetch failed for ${cacheKey}:`, error);
  }
}

/**
 * Invalidates the cache for a specific endpoint
 * 
 * @param endpoint - The API endpoint
 * @param params - Optional parameters
 * @param options - Cache options
 */
export function invalidateCache(
  endpoint: string,
  params?: any,
  options: CacheOptions = {}
): void {
  const cacheKey = generateCacheKey(endpoint, params);
  clearCache(cacheKey, options);
  console.log(`Cache invalidated for ${cacheKey}`);
}
