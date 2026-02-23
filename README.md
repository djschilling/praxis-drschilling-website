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

## Wichtige Anpassung

Die Terminvergabe ist als `iframe` eingebunden.
Trage die echte S3-Embed-URL in folgender Datei ein:

- `src/pages/index.astro`
- Variable: `s3BookingUrl`
