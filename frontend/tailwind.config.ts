/** @type {import('tailwindcss').Config} */
export default {
  // The 'content' array tells Tailwind which files to scan for class names.
  content: [
    './src/**/*.{html,js,svelte,ts}',
  ],

  // Enable dark mode using class strategy
  darkMode: 'class',

  // Define our design system
  theme: {
    extend: {
      // Font family
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Open Sans', 'Helvetica Neue', 'sans-serif'],
      },

      // Color system - based on existing CSS variables
      colors: {
        // Primary colors
        'primary': {
          DEFAULT: '#007bff',
          '50': '#e6f2ff',
          '100': '#cce5ff',
          '200': '#99caff',
          '300': '#66afff',
          '400': '#3394ff',
          '500': '#007bff',
          '600': '#0062cc',
          '700': '#004999',
          '800': '#003166',
          '900': '#001833',
        },
        'secondary': {
          DEFAULT: '#6c757d',
          '50': '#f2f3f4',
          '100': '#e6e7e9',
          '200': '#cccfd3',
          '300': '#b3b7bd',
          '400': '#999fa7',
          '500': '#6c757d',
          '600': '#565e64',
          '700': '#41464b',
          '800': '#2b2f32',
          '900': '#161719',
        },

        // Status colors
        'success': {
          DEFAULT: '#28a745',
          '50': '#e9f7ed',
          '100': '#d4efdb',
          '200': '#a9dfb7',
          '300': '#7dcf93',
          '400': '#52bf6f',
          '500': '#28a745',
          '600': '#208637',
          '700': '#186429',
          '800': '#10431c',
          '900': '#08210e',
        },
        'danger': {
          DEFAULT: '#dc3545',
          '50': '#fbecee',
          '100': '#f8d9dd',
          '200': '#f1b3bb',
          '300': '#ea8d99',
          '400': '#e36777',
          '500': '#dc3545',
          '600': '#b02a37',
          '700': '#842029',
          '800': '#58151c',
          '900': '#2c0b0e',
        },
        'warning': {
          DEFAULT: '#ffc107',
          '50': '#fff9e6',
          '100': '#fff3cc',
          '200': '#ffe799',
          '300': '#ffdb66',
          '400': '#ffcf33',
          '500': '#ffc107',
          '600': '#cc9a06',
          '700': '#997304',
          '800': '#664d03',
          '900': '#332601',
        },
        'info': {
          DEFAULT: '#17a2b8',
          '50': '#e8f6f8',
          '100': '#d1edf1',
          '200': '#a3dbe3',
          '300': '#75c9d5',
          '400': '#47b7c7',
          '500': '#17a2b8',
          '600': '#138293',
          '700': '#0e616e',
          '800': '#09414a',
          '900': '#052025',
        },

        // UI colors
        'light': {
          DEFAULT: '#f8f9fa',
          'hover': '#e9ecef',
        },
        'dark': {
          DEFAULT: '#212529',
          'hover': '#343a40',
        },
        'focus': {
          DEFAULT: '#ffc107', // Same as warning
          'bg': '#fffbeb',
        },

        // Gray shades for more flexibility
        'gray': {
          '50': '#f9fafb',
          '100': '#f3f4f6',
          '200': '#e5e7eb',
          '300': '#d1d5db',
          '400': '#9ca3af',
          '500': '#6b7280',
          '600': '#4b5563',
          '700': '#374151',
          '800': '#1f2937',
          '900': '#111827',
          '950': '#030712',
        },
      },

      // Border radius
      borderRadius: {
        'sm': '0.25rem',
        'md': '0.375rem',
        'lg': '0.5rem',
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
      },

      // Box shadows
      boxShadow: {
        'sm': '0 1px 3px rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px rgba(0, 0, 0, 0.07)',
        'lg': '0 8px 16px rgba(0, 0, 0, 0.07)',
        'xl': '0 12px 24px rgba(0, 0, 0, 0.09)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)',
      },

      // Z-index
      zIndex: {
        'navbar': 1000,
        'modal': 1050,
        'tooltip': 1070,
        'dropdown': 1000,
        'popover': 1060,
      },

      // Screen sizes for more consistent responsive design
      screens: {
        'xs': '475px',
        // sm: '640px', // Tailwind default
        // md: '768px', // Tailwind default
        // lg: '1024px', // Tailwind default
        // xl: '1280px', // Tailwind default
        // '2xl': '1536px', // Tailwind default
      },

      // Spacing for more flexibility
      spacing: {
        '72': '18rem',
        '80': '20rem',
        '96': '24rem',
        '128': '32rem',
      },
    },
  },

  // Plugins
  plugins: [
    require('@tailwindcss/typography'),
    // Uncomment if you need form styling
    // require('@tailwindcss/forms'),
  ],
};
