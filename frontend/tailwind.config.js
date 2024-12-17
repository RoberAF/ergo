// tailwind.config.js (o tailwind.config.mjs, si prefieres)
import tailwindScrollBar from 'tailwind-scrollbar';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [
    tailwindScrollBar
  ],
};
