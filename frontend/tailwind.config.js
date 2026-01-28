/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        'deep-sea': {
          900: '#0f1419',  // Deepest navy
          800: '#1a2f4f',  // Dark navy
          700: '#2a3f5f',  // Medium navy
          600: '#3a4f6f',  // Blue-gray
          500: '#4a627f',  // Medium blue-gray
          400: '#7a8fa8',  // Light blue-gray
          300: '#a8b8c8',  // Lighter gray
          200: '#d4d4d8',  // Light gray
          100: '#f0f0f2',  // Very light gray
        },
        primary: '#0f1419',
        secondary: '#4a627f',
        accent: '#7a8fa8',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

