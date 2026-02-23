# AGENTS.md

## Projektkontext
- Projekt: Webseite fuer die Hausarztpraxis Dr. Bernd Schilling in Gomaringen.
- Stack: Astro + Tailwind CSS.
- Ziel: Vertrauenswuerdiger, familienaer Eindruck und gute Auffindbarkeit fuer neue Patientinnen und Patienten.

## Inhaltsregeln
- Praxisdaten konsistent halten:
  - Name: Dr. Bernd Schilling
  - Ort: Gomaringen
  - Adresse: Lindenstrasse 84
  - Telefon: 07072 / 7031
- Sprache: Deutsch (de-DE), klar und freundlich, ohne Marketingfloskeln.
- Historie und familiaerer Charakter der Praxis beibehalten (3. Generation, ueber 100 Jahre).

## Technische Regeln
- Bestehende Struktur beibehalten:
  - `src/layouts/MainLayout.astro`
  - `src/pages/index.astro`
  - `src/styles/global.css`
- Styling nur mit Tailwind und vorhandenen CSS-Variablen erweitern.
- Keine unnoetigen neuen Abhaengigkeiten einfuehren.
- Terminvergabe ueber bestehendes S3-`iframe` integrieren; URL ueber `s3BookingUrl` pflegen.

## Deployment
- Deployment erfolgt ueber GitHub Actions nach GitHub Pages.
- Workflow-Datei: `.github/workflows/deploy.yml`
- Bei Aenderungen an Routen/Assets auf korrekten `base` in `astro.config.mjs` achten.

## Qualitaet
- Nach Aenderungen mindestens `npm run build` erfolgreich ausfuehren.
- Aenderungen klein und nachvollziehbar halten.
- Keine sensiblen Daten oder Zugangsdaten im Repository speichern.
