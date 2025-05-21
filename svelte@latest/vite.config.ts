// vite.config.js
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [
    sveltekit() // Integrates SvelteKit with Vite
  ],

  // Server configuration (for the Vite development server)
  server: {
    port: 5173, // Default SvelteKit/Vite port, change if needed
    strictPort: true, // Exit if port is already in use
    proxy: { // Setup proxy for API requests during development to avoid CORS issues
      '/api/v1': {
        target: 'http://localhost:5000', // Your backend API URL
        changeOrigin: true, // Needed for virtual hosted sites
        secure: false,
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, _res) => {
            console.log('proxy error', err);
          });
          proxy.on('proxyReq', (proxyReq, req, _res) => {
            console.log('Sending Request to the Target:', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes, req, _res) => {
            console.log('Received Response from the Target:', proxyRes.statusCode, req.url);
          });
        },
      }
    }
  },

  // Build configuration
  build: {
    // Options for the production build
    // sourcemap: true, // Generate source maps for production (can be 'inline', 'hidden')
  },

  // Preview server configuration (for `vite preview` command)
  preview: {
    port: 4173, // Port for the preview server
    strictPort: true,
  },

  // Environment variable handling
  // Vite automatically loads .env files.
  // envPrefix: 'VITE_', // Default prefix for environment variables exposed to client-side

  // Resolve aliases (can also be defined in svelte.config.js, keeping them in one place is good)
  // resolve: {
  //   alias: {
  //     '$lib': path.resolve(__dirname, './src/lib'),
  //     '$components': path.resolve(__dirname, './src/lib/components'),
  //     // Add other aliases if you prefer to manage them here
  //   }
  // }
  // If using path.resolve, you'd need: import path from 'path';
});
