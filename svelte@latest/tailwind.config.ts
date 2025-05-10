/** @type {import('tailwindcss').Config} */
export default {
  // The 'content' array tells Tailwind which files to scan for class names.
  // This is crucial for Tailwind to generate the necessary CSS.
  // Ensure this pattern correctly covers all your .svelte files and any other
  // files where you might use Tailwind classes (e.g., .html, .ts).
  content: [
    './src/**/*.{html,js,svelte,ts}', 
  ],

  // The 'theme' section is where you can customize Tailwind's default design system.
  // For example, you can extend colors, fonts, spacing, etc.
  theme: {
    extend: {
      // Example: Adding a custom font family
      // fontFamily: {
      //   sans: ['Inter', 'sans-serif'], // Ensure 'Inter' is imported in your global CSS or app.html
      // },
      // Example: Adding custom colors
      // colors: {
      //   'brand-blue': '#007bff',
      //   'brand-purple': '#6f42c1',
      // },
    },
  },

  // The 'plugins' array is where you can add official or third-party Tailwind CSS plugins.
  // For example, @tailwindcss/forms, @tailwindcss/typography, etc.
  plugins: [
    // require('@tailwindcss/forms'), // Uncomment if you need form styling plugin (use import for ESM)
  ],
};
