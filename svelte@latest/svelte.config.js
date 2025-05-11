import adapter from '@sveltejs/adapter-auto'; // Or your specific adapter (e.g., adapter-node, adapter-static)
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'; // Commonly used with Vite-based SvelteKit
// import sveltePreprocess from 'svelte-preprocess'; // Alternative, more explicit preprocessor

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://kit.svelte.dev/docs/integrations#preprocessors
  // for more information about preprocessors.
  
  // Option 1: Using vitePreprocess (often the default and simpler)
  // vitePreprocess will automatically pick up your PostCSS configuration (postcss.config.js)
  // and apply Tailwind CSS transformations.
  preprocess: vitePreprocess(),

  // Option 2: Using svelte-preprocess (more explicit control)
  // If you use svelte-preprocess, you need to ensure its postcss option is enabled.
  // preprocess: sveltePreprocess({
  //   postcss: true, // This tells svelte-preprocess to use PostCSS
  //   // You can also configure other preprocessors here if needed:
  //   // scss: {
  //   //   prependData: '@use "src/variables.scss" as *;',
  //   // },
  //   // typescript: {
  //   //  tsconfigFile: './tsconfig.json',
  //   // },
  // }),

  kit: {
    adapter: adapter(),
    // You can add aliases here if needed, e.g., for $lib
    // alias: {
    //   $lib: 'src/lib',
    // }
    // Other SvelteKit specific configurations
  }
};

export default config;
