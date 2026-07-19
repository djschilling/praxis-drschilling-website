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

## Terminvergabe

Termine werden derzeit nur telefonisch vergeben (`07072 / 7031`).
Eine Online-Buchung ist für später vorgesehen.
