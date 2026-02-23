import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

const repoName = process.env.GITHUB_REPOSITORY?.split('/')[1];
const isGitHubActions = process.env.GITHUB_ACTIONS === 'true';
const base = process.env.ASTRO_BASE ?? (isGitHubActions && repoName ? `/${repoName}` : '/');

export default defineConfig({
  site: 'https://praxis-dr-schilling.de',
  base,
  integrations: [tailwind()]
});
