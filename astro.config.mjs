import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import autoprefixer from 'autoprefixer';
import tailwindcss from 'tailwindcss';

export default defineConfig({
  site: 'https://mvz-gomaringen.de',
  base: '/',
  integrations: [sitemap()],
  vite: {
    css: {
      postcss: {
        plugins: [tailwindcss(), autoprefixer()]
      }
    }
  }
});
