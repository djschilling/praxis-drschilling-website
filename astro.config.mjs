import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://praxis-dr-schilling.de',
  integrations: [tailwind()]
});
