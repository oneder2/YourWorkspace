// svelte.config.js
import adapter from '@sveltejs/adapter-auto'; // Or your preferred adapter (e.g., adapter-node, adapter-static)
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://kit.svelte.dev/docs/integrations#preprocessors
  // for more information about preprocessors
  preprocess: vitePreprocess(), // Enables Vite-based preprocessing (e.g., for TypeScript, PostCSS)

  kit: {
    // adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
    // If your environment is not supported or you settled on a specific environment, switch out the adapter.
    // See https://kit.svelte.dev/docs/adapters for more information about adapters.
    adapter: adapter(), // Default adapter, automatically chooses the best adapter for your deployment target.
                        // You might change this to adapter-node, adapter-static, etc., based on hosting.

    // Alias configuration: Define shortcuts for import paths.
    // This helps in keeping imports clean, especially in larger projects.
    // Example: import Component from '$components/Component.svelte' instead of '../../components/Component.svelte'
    alias: {
      // '$components': 'src/lib/components', // Already common practice to put in lib
      // '$utils': 'src/lib/utils',
      // '$stores': 'src/lib/store',
      // '$services': 'src/lib/services',
      // '$assets': 'src/lib/assets',
      // Note: SvelteKit automatically provides $lib for src/lib
    },

    // Other Kit configurations can go here:
    // csrf: { checkOrigin: false }, // Example: CSRF protection settings
    // files: { assets: 'static' }, // Default is 'static'
    // outDir: '.svelte-kit',      // Default output directory
    // appDir: '_app',             // Directory for SvelteKit's internal files in the browser
  },

  // Compiler options for Svelte, if needed
  // compilerOptions: {
  //  customElement: false, // Set to true if building Svelte components as custom elements
  //  runes: true, // Enable runes mode if you are using Svelte 5 features
  // },
};

export default config;
