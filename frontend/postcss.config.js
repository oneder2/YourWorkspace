// postcss.config.js (if your project uses ES Modules, check package.json for "type": "module")
// Or postcss.config.cjs (if your project uses CommonJS, or if .js files are treated as CommonJS by default)

// It's crucial that the plugins are correctly listed here.
// tailwindcss: The Tailwind CSS plugin itself.
// autoprefixer: Adds vendor prefixes to CSS rules for older browsers.

export default { // Use 'export default' for ESM (.js with "type": "module" or .mjs)
  // module.exports = { // Use 'module.exports' for CommonJS (.cjs or .js without "type": "module")
    plugins: {
      tailwindcss: {}, // Configuration for Tailwind CSS (usually empty, reads from tailwind.config.js)
      autoprefixer: {}, // Configuration for Autoprefixer (usually empty for default behavior)
    },
  };
  
  /*
  If you are using a .cjs file (postcss.config.cjs), the syntax would be:
  module.exports = {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  };
  
  If you are using a .js file in an ES Module project (package.json has "type": "module"),
  the ES Module syntax with `export default` is preferred:
  export default {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  };
  
  Make sure the syntax (ESM vs CommonJS) matches your project's module system.
  SvelteKit projects created with `npm create svelte@latest` typically use ES Modules.
  */
  