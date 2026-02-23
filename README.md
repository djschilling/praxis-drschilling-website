# Hausarztpraxis Dr. Bernd Schilling - Webseite

Neue Webseite mit Astro + Tailwind fuer die Hausarztpraxis in Gomaringen.

## Start

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
npm run preview
```

## Deployment (GitHub Pages)

GitHub Action ist eingerichtet unter:

- `.github/workflows/deploy.yml`

So aktivierst du es im Repository:

1. Code nach GitHub pushen (`main` Branch).
2. In GitHub: `Settings -> Pages -> Source` auf **GitHub Actions** stellen.
3. Bei jedem Push auf `main` wird automatisch gebaut und deployed.

Hinweis zur URL:

- Fuer Projektseiten nutzt Astro automatisch den Repo-Pfad als `base`.
- Falls du spaeter eine eigene Domain verwendest, kannst du im Workflow `ASTRO_BASE=/` setzen.

## Wichtige Anpassung

Die Terminvergabe ist als `iframe` eingebunden.
Trage die echte S3-Embed-URL in folgender Datei ein:

- `src/pages/index.astro`
- Variable: `s3BookingUrl`
