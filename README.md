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

## Logo und Favicon

Die Navigation auf Startseite, Impressum und Datenschutz verwendet das Landschaftslogo
mit Sonne (`public/images/brand/landschaft-c.png`, transparente PNG, 528 × 382 px).
Die zweizeilige HTML-Wortmarke steht in `src/components/Brand.astro`:
„MVZ Gomaringen“ in Fraunces 550, „Praxis Dr. Schilling · Hausarzt“ in Figtree 400.
Im Hero wird kein zusätzliches Logo angezeigt.

Die Favicons sind nur verkleinerte Fassungen dieser Original-Bildmarke, keine
separate SVG-Zeichnung. PNGs (16/32/48 px), ICO und Apple-Touch-Icon (180 px)
werden in `src/layouts/MainLayout.astro` eingebunden. Reproduktion mit ImageMagick:

```bash
for size in 16 32 48 180; do
  magick public/images/brand/landschaft-c.png -filter Lanczos -resize "${size}x${size}" -background none -gravity center -extent "${size}x${size}" -depth 8 "PNG32:public/favicon-${size}.png"
done
magick public/favicon-16.png public/favicon-32.png public/favicon-48.png public/favicon.ico
```

Bei Änderungen der Icons auch die Version in ihren URLs aktualisieren, damit
Browser keine veralteten Favicons aus dem Cache verwenden.

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
