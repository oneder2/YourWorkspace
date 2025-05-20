/**
 * SVG Utilities
 *
 * This module provides utilities for working with SVGs in the application.
 * It helps standardize SVG usage and ensures proper loading of SVG assets.
 * Enhanced with SVG sprite support, caching, and performance tracking.
 */
import { browser } from '$app/environment';
import { mark } from './performance';

// Cache for loaded SVG content
const svgCache = new Map<string, string>();

// Track which SVGs have been preloaded
const preloadedSvgs = new Set<string>();

/**
 * Get the URL for an SVG icon from the static assets folder
 *
 * @param name - The name of the SVG file without extension
 * @returns The full URL to the SVG file
 */
export function getSvgUrl(name: string): string {
  return `/images/icons/${name}.svg`;
}

/**
 * Common SVG icons used throughout the application
 */
export const SvgIcons = {
  // Navigation icons
  TODO: '/images/icons/todo.svg',
  DOING: '/images/icons/doing.svg',
  DONE: '/images/icons/done.svg',
  PLAN: '/images/icons/plan.svg',
  ANCHOR: '/images/icons/anchor.svg',

  // UI icons
  ADD: '/images/icons/add.svg',
  EDIT: '/images/icons/edit.svg',
  DELETE: '/images/icons/delete.svg',
  CLOSE: '/images/icons/close.svg',
  MENU: '/images/icons/menu.svg',
  SEARCH: '/images/icons/search.svg',

  // Status icons
  SUCCESS: '/images/icons/success.svg',
  ERROR: '/images/icons/error.svg',
  WARNING: '/images/icons/warning.svg',
  INFO: '/images/icons/info.svg',
};

/**
 * Map of route-specific SVG icons
 * Used to preload icons for specific routes
 */
export const RouteSvgMap: Record<string, string[]> = {
  '/doing': [
    SvgIcons.TODO,
    SvgIcons.ADD,
    SvgIcons.EDIT,
    SvgIcons.DELETE
  ],
  '/done': [
    SvgIcons.DONE,
    SvgIcons.ADD,
    SvgIcons.EDIT,
    SvgIcons.DELETE
  ],
  '/plan': [
    SvgIcons.PLAN,
    SvgIcons.ADD,
    SvgIcons.EDIT
  ],
  '/anchor': [
    SvgIcons.ANCHOR,
    SvgIcons.EDIT
  ]
};

/**
 * Fetch and cache SVG content
 *
 * @param url - URL of the SVG to fetch
 * @returns Promise that resolves with the SVG content
 */
export async function fetchSvgContent(url: string): Promise<string> {
  // Return from cache if available
  if (svgCache.has(url)) {
    return svgCache.get(url)!;
  }

  try {
    mark(`svg-fetch-start-${url}`);
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Failed to fetch SVG: ${url} (${response.status})`);
    }

    const svgText = await response.text();
    mark(`svg-fetch-end-${url}`, `svg-fetch-${url}`);

    // Cache the SVG content
    svgCache.set(url, svgText);

    return svgText;
  } catch (error) {
    console.error(`Error fetching SVG: ${url}`, error);
    // Return a placeholder SVG on error
    return `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><rect width="24" height="24" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" /></svg>`;
  }
}

/**
 * Preload SVG icons to ensure they're available when needed
 * Enhanced with caching and performance tracking
 *
 * @param icons - Array of icon URLs to preload
 * @returns Promise that resolves when all icons are loaded
 */
export async function preloadSvgIcons(icons: string[] = Object.values(SvgIcons)): Promise<void> {
  if (!browser) return;

  mark('svg-preload-start');

  // Filter out already preloaded icons
  const iconsToLoad = icons.filter(url => !preloadedSvgs.has(url));

  if (iconsToLoad.length === 0) {
    mark('svg-preload-end', 'svg-preload');
    return;
  }

  try {
    // Fetch all SVGs in parallel
    await Promise.all(
      iconsToLoad.map(async url => {
        try {
          await fetchSvgContent(url);
          preloadedSvgs.add(url);
        } catch (error) {
          console.error(`Failed to preload SVG: ${url}`, error);
        }
      })
    );
  } catch (error) {
    console.error('Error during SVG preloading:', error);
  }

  mark('svg-preload-end', 'svg-preload');
}

/**
 * Preload SVG icons for a specific route
 *
 * @param route - The route to preload icons for
 * @returns Promise that resolves when all route-specific icons are loaded
 */
export async function preloadRouteSvgIcons(route: string): Promise<void> {
  if (!browser) return;

  const routeIcons = RouteSvgMap[route] || [];

  if (routeIcons.length === 0) return;

  mark(`route-svg-preload-start-${route}`);
  await preloadSvgIcons(routeIcons);
  mark(`route-svg-preload-end-${route}`, `route-svg-preload-${route}`);
}

/**
 * SVG Component Props
 */
export interface SvgProps {
  name: string;
  size?: string | number;
  color?: string;
  className?: string;
  title?: string;
  ariaLabel?: string;
  ariaHidden?: boolean;
  role?: string;
  focusable?: boolean;
}

/**
 * Generate inline SVG markup for embedding directly in components
 * Uses cached SVG content when available
 *
 * @param props - SVG properties
 * @returns SVG markup string or a placeholder while loading
 */
export async function getInlineSvg(props: SvgProps): Promise<string> {
  if (!browser) {
    return createPlaceholderSvg(props);
  }

  const {
    name,
    size = 24,
    color = 'currentColor',
    className = '',
    title,
    ariaLabel,
    ariaHidden = !ariaLabel,
    role = 'img',
    focusable = false
  } = props;

  // Determine the SVG URL
  const url = name.includes('/') ? name : getSvgUrl(name);

  try {
    // Fetch SVG content (will use cache if available)
    const svgContent = await fetchSvgContent(url);

    // Process the SVG content to apply custom properties
    return processSvgContent(svgContent, {
      size,
      color,
      className,
      title,
      ariaLabel,
      ariaHidden,
      role,
      focusable
    });
  } catch (error) {
    console.error(`Error generating inline SVG for ${name}:`, error);
    return createPlaceholderSvg(props);
  }
}

/**
 * Process SVG content to apply custom properties
 *
 * @param svgContent - The raw SVG content
 * @param options - Options for customizing the SVG
 * @returns Processed SVG content
 */
function processSvgContent(
  svgContent: string,
  options: {
    size: string | number;
    color: string;
    className: string;
    title?: string;
    ariaLabel?: string;
    ariaHidden: boolean;
    role: string;
    focusable: boolean;
  }
): string {
  const {
    size,
    color,
    className,
    title,
    ariaLabel,
    ariaHidden,
    role,
    focusable
  } = options;

  // Convert size to string with 'px' if it's a number
  const sizeValue = typeof size === 'number' ? `${size}px` : size;

  // Extract the SVG element
  const svgMatch = svgContent.match(/<svg[^>]*>([\s\S]*?)<\/svg>/i);

  if (!svgMatch) {
    return createPlaceholderSvg(options);
  }

  // Extract the inner content of the SVG
  const innerContent = svgMatch[1];

  // Create a new SVG element with our custom properties
  let newSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${sizeValue}" height="${sizeValue}" viewBox="0 0 24 24" fill="none" stroke="${color}" class="${className}" role="${role}" aria-hidden="${ariaHidden}" focusable="${focusable}"`;

  // Add aria-label if provided
  if (ariaLabel) {
    newSvg += ` aria-label="${ariaLabel}"`;
  }

  // Close the opening tag
  newSvg += '>';

  // Add title if provided
  if (title) {
    newSvg += `<title>${title}</title>`;
  }

  // Add the inner content
  newSvg += innerContent;

  // Close the SVG tag
  newSvg += '</svg>';

  return newSvg;
}

/**
 * Create a placeholder SVG while the actual SVG is loading
 *
 * @param props - SVG properties
 * @returns Placeholder SVG markup
 */
function createPlaceholderSvg(props: SvgProps | any): string {
  const {
    size = 24,
    color = 'currentColor',
    className = '',
    ariaHidden = true
  } = props;

  // Convert size to string with 'px' if it's a number
  const sizeValue = typeof size === 'number' ? `${size}px` : size;

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${sizeValue}" height="${sizeValue}" viewBox="0 0 24 24" fill="none" stroke="${color}" class="${className}" aria-hidden="${ariaHidden}"><rect width="24" height="24" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" /></svg>`;
}
