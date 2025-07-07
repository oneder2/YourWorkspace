/**
 * SVG Utilities
 * 
 * This module provides utilities for working with SVGs in the application.
 * It helps standardize SVG usage and ensures proper loading of SVG assets.
 */

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
 * Preload SVG icons to ensure they're available when needed
 * 
 * @param icons - Array of icon URLs to preload
 * @returns Promise that resolves when all icons are loaded
 */
export function preloadSvgIcons(icons: string[] = Object.values(SvgIcons)): Promise<void[]> {
  return Promise.all(
    icons.map(url => 
      fetch(url)
        .then(response => {
          if (!response.ok) {
            console.warn(`Failed to preload SVG: ${url}`);
          }
          return;
        })
        .catch(error => {
          console.error(`Error preloading SVG: ${url}`, error);
          return;
        })
    )
  );
}

/**
 * SVG Component Props
 */
export interface SvgProps {
  name: string;
  size?: string | number;
  color?: string;
  className?: string;
}

/**
 * Generate inline SVG markup for embedding directly in components
 * 
 * @param props - SVG properties
 * @returns SVG markup string
 */
export function getInlineSvg(props: SvgProps): string {
  const { name, size = 24, color = 'currentColor', className = '' } = props;
  
  // This is a simplified example - in a real implementation, you would
  // either fetch the SVG content or have a mapping of SVG content
  const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="${className}"><use href="${getSvgUrl(name)}#icon" /></svg>`;
  
  return svgContent;
}
