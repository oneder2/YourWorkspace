// vite.config.js
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig(({ mode }) => {
  // Determine if we're in production mode
  const isProduction = mode === 'production';

  // Set the backend API URL based on environment
  // In production, the backend service will be available at 'http://backend:5000'
  // In development, it will be 'http://localhost:5000'
  const backendUrl = isProduction
    ? 'http://backend:5000'
    : 'http://localhost:5000';

  return {
    plugins: [
      sveltekit() // Integrates SvelteKit with Vite
    ],

    // Server configuration (for the Vite development server)
    server: {
      port: 5173, // Default SvelteKit/Vite port, change if needed
      strictPort: true, // Exit if port is already in use
      proxy: { // Setup proxy for API requests during development to avoid CORS issues
        // All requests to '/api/v1' in dev will be forwarded to the backend API URL
        '/api/v1': {
          target: backendUrl, // Your backend API URL
          changeOrigin: true, // Needed for virtual hosted sites
          secure: false,
          rewrite: (path) => path // Keep the path as is since backend has the same prefix
        }
      }
    },

    // Build configuration
    build: {
      // Options for the production build
      sourcemap: false, // Don't generate source maps for production to reduce size
      reportCompressedSize: false, // Disable reporting compressed chunk sizes to speed up build
      chunkSizeWarningLimit: 1000, // Increase the size limit for warnings
    },

    // Preview server configuration (for `vite preview` command)
    preview: {
      port: 4173, // Port for the preview server
      strictPort: true,
    },

    // Environment variable handling
    // Vite automatically loads .env files.
    envPrefix: 'VITE_', // Default prefix for environment variables exposed to client-side
  };
});
