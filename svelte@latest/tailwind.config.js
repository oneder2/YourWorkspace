/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      // Font family
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Open Sans', 'Helvetica Neue', 'sans-serif'],
      },

      // Color system
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
      },

      zIndex: {
        'navbar': 50,
        'modal': 1050,
        'tooltip': 1070,
        'dropdown': 1000,
        'popover': 1060,
      },
      keyframes: {
        dropdown: {
          '0%': { opacity: 0, transform: 'translateY(-10px) translateX(-50%)' },
          '100%': { opacity: 1, transform: 'translateY(0) translateX(-50%)' }
        }
      },
      animation: {
        dropdown: 'dropdown 0.3s ease-out forwards'
      },

      // Screen sizes for more consistent responsive design
      screens: {
        'xs': '475px',
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
}
