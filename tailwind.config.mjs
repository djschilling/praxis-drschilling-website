/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        praxis: {
          deep: '#164039',
          mid: '#1f5a50',
          accent: '#2f6f7a',
          soft: '#d7e8eb',
          mist: '#eef3f1',
          highlight: '#c4a35a',
          ink: '#152826'
        }
      },
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'serif'],
        sans: ['Figtree', 'Segoe UI', 'sans-serif']
      },
      boxShadow: {
        soft: '0 20px 50px rgba(15, 46, 42, 0.12)',
        lift: '0 12px 30px rgba(47, 111, 122, 0.16)'
      }
    }
  },
  plugins: []
};
