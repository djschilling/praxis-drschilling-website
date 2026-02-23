/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        praxis: {
          deep: '#1c4f4a',
          strong: '#23635d',
          accent: '#cb8b37'
        }
      },
      boxShadow: {
        warm: '0 22px 55px rgba(28, 79, 74, 0.14)'
      }
    }
  },
  plugins: []
};
