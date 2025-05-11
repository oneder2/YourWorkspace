// postcss.config.js

// Import the necessary plugins
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';

// Export the configuration object
export default {
  plugins: [
    // Initialize Tailwind CSS
    tailwindcss(),
    // Add vendor prefixes for browser compatibility
    autoprefixer(),
    // You can add other PostCSS plugins here if needed
  ],
};
