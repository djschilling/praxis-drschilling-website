# Hausarztpraxis Dr. Bernd Schilling - Webseite

Neue Webseite mit Astro + Tailwind fuer die Hausarztpraxis in Gomaringen.

## Start

Voraussetzung: Node.js ab 22.23.4; GitHub Actions verwendet Node.js 24.
Die Website nutzt Astro 7 und Tailwind CSS 3 über die PostCSS-Konfiguration
in `astro.config.mjs` (ohne die ältere `@astrojs/tailwind`-Integration).

```bash
npm ci
npm run dev
```

## Build

```bash
npm run build
npm run preview
```

`npm test` baut die Website und prüft die zeitgesteuerten Hinweise einschließlich
überlappender Zeiträume, Tab-Rückkehr und Zeitumstellung. Der Deployment-Workflow
führt dieselben Prüfungen vor dem Upload aus.

## Sprechzeiten und Hinweise pflegen

`src/data/oeffnungszeiten.json` enthält die regulären Sprechzeiten als Zeitpaare
im Format `HH:MM`. Website, Suchmaschinen-Metadaten und Visitenkartengenerator
verwenden dieselben Daten. Druckdateien werden nicht automatisch aktualisiert;
bei Änderungen neu erzeugen und erneut freigeben.

Hinweise stehen in `src/data/hinweise.ts`. `sichtbarAb` ist inklusive,
`sichtbarBis` exklusive. Zeitstempel brauchen den passenden deutschen UTC-Offset
(`+01:00` im Winter, `+02:00` im Sommer). `geschlossenAm` enthält die tatsächlichen
Schließtage als `YYYY-MM-DD` für die Suchmaschinen-Metadaten; diese sind unabhängig
vom Anzeigezeitraum der Ankündigung.

Der Browser plant Prüfungen an den Zeitgrenzen und im Abstand von höchstens einer
Minute. In inaktiven Tabs können Browser Timer verzögern; bei Rückkehr zum Tab
wird deshalb sofort neu geprüft. Maßgeblich ist die Geräteuhr. Ohne JavaScript bleiben
alle hinterlegten, ausdrücklich datierten Hinweise mit einer Erklärung zur
fehlenden automatischen Filterung lesbar. Abgelaufene Hinweise regelmäßig entfernen.

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

## Hero-Bild

Das Hero bietet AVIF vor WebP an; JPEG bleibt der letzte Fallback. Auflösung,
Bildausschnitt und Animation bleiben für alle Formate gleich. Die große
`sizes`-Angabe auf schmalen Displays berücksichtigt, dass `object-cover` das
Querformatbild auf die Höhe des Heros skaliert und seitlich beschneidet.

AVIF-Dateien aus dem Original-JPEG erzeugen (Sharp wird mit Astro installiert):

```sh
node --input-type=module <<'JS'
import sharp from 'sharp';
for (const [width, height] of [[1600, 838], [2400, 1257]]) {
  await sharp('public/images/hero/gomaringen-tal.jpg')
    .resize({ width, height, fit: 'fill' })
    .avif({ quality: 50, effort: 6, chromaSubsampling: '4:4:4' })
    .toFile(`public/images/hero/gomaringen-tal-${width}.avif`);
}
JS
```

## Nicht veröffentlichte Bilddateien

Die drei JPEG-Portraitvorlagen liegen unter `design/originals/team/`, die frühere
Social-Vorschau unter `design/originals/social/`. Sie bleiben im Repository,
werden aber nicht in die Website kopiert. Die verwendeten WebP-Portraits, die
aktuelle Social-Vorschau sowie Hero- und Team-JPEGs als Fallbacks bleiben in `public/`.

## Deployment (GitHub Pages)

GitHub Action ist eingerichtet unter:

- `.github/workflows/deploy.yml`

So aktivierst du es im Repository:

1. Code nach GitHub pushen (`main` Branch).
2. In GitHub: `Settings -> Pages -> Source` auf **GitHub Actions** stellen.
3. Bei jedem Push auf `main` wird automatisch gebaut und deployed.

Hinweis zur URL:

- Die Website ist in `astro.config.mjs` auf `https://mvz-gomaringen.de` mit `base: '/'` konfiguriert.
- Der Workflow setzt keinen Repo-Pfad automatisch; `ASTRO_BASE` wird nicht ausgewertet.
- Bei einem Umzug auf eine GitHub-Projektseite müssen `site` und `base` in der
  Astro-Konfiguration sowie absolute Font-, Sitemap- und strukturierte Daten-URLs geprüft werden.

## Terminvergabe

Termine werden derzeit nur telefonisch vergeben (`07072 / 7031`).
Eine Online-Buchung ist für später vorgesehen.

## Offene Prüfpunkte aus dem Projektreview

### Impressum und Anbieterangaben

Bestätigt sind der rechtliche Anbieter **MED-GO e.G.**, die Anschrift
**Lindenstraße 84/1, 72810 Gomaringen** und das **Amtsgericht Stuttgart**.
Die übrigen Angaben sind noch nicht abschließend bestätigt; diese Liste ist
keine rechtliche Freigabe. Die öffentlichen Rechtstexte bleiben bis zur Klärung
unverändert, ohne Platzhalter für fehlende Angaben.

- Genossenschaftsregisternummer: `GnR 720231` steht im Code, ist aber noch zu bestätigen.
- Vertretungsberechtigter Vorstand: vollständige Namen und Einzel-/Gesamtvertretung fehlen.
- Eine überwachte, öffentlich erreichbare E-Mail-Adresse fehlt. Die vorhandene
  KIM-Adresse ersetzt keine gewöhnliche E-Mail-Adresse nach § 5 DDG.
  Terminvereinbarungen können weiterhin ausschließlich telefonisch erfolgen.
- Für Dr. Bernd Schilling, Julie Osmaston und Dr. Cornelia Riesner: genaue
  Berufsbezeichnung und Staat der Verleihung bestätigen.
- Zuständige Kammern, KV und gegebenenfalls weitere Aufsichtsbehörden bestätigen.
- Falls vergeben: USt-IdNr. bzw. Wirtschafts-Identifikationsnummer des Anbieters
  ergänzen. Die Umsatzsteuerbefreiung ärztlicher Leistungen begründet nicht das
  Fehlen einer solchen Nummer. Keine persönlichen Steuer-IDs oder Steuernummern veröffentlichen.
- Klären, ob journalistisch-redaktionelle Inhalte geplant sind und die Angabe
  nach § 18 Abs. 2 MStV erforderlich ist; gegebenenfalls die benannte Verantwortung bestätigen.
- Die Haftungstexte zitieren frühere TMG-Regelungen fälschlich als §§ 7–10 DDG.
  Empfehlung zur rechtlichen Prüfung: generische Inhalts-/Linkhaftungstexte entfernen.

### Weitere Prüfungen

#### Datenschutz: öffentlich geprüft am 12. November 2026

Umami läuft laut Betreiber auf einem Server bei netcup. Die folgenden Befunde
trennen öffentlich sichtbare Einstellungen von allgemeinen Anbieterangaben;
sie bestätigen keine konkrete Serverkonfiguration oder rechtliche Zulässigkeit.

- Die live ausgelieferte Startseite bindet `https://umami.davidschilling.de/script.js`
  mit `data-do-not-track="true"`, `data-exclude-search="true"` und
  `data-exclude-hash="true"` ein. Das öffentlich abgerufene Skript unterstützt
  diese Optionen. Geprüft wurden HTML und Skript, keine Analytics-Anfragen versendet.
- Laut [Umami-Konfiguration](https://docs.umami.is/docs/tracker-configuration)
  unterdrücken diese Optionen Suchparameter und Fragmente der erfassten Seiten-URL
  sowie Tracking bei einem vom Browser bereitgestellten aktivierten DNT-Signal.
  DNT wird nicht von allen Browsern unterstützt und verhindert weder das Laden
  des Skripts noch sämtliche Infrastruktur-Logs.
- Laut [Umami-Metrikdefinitionen](https://docs.umami.is/docs/metric-definitions)
  wird die IP-Adresse zur Standortermittlung und Bildung einer Sitzungskennung
  verarbeitet, aber nicht als Feld im Standard-Analytics-Datensatz gespeichert.
  Infrastruktur-Logs können dennoch IP-Adressen enthalten. Cookie-freie Kennungen
  garantieren keine absolute Anonymität. Die derzeitigen pauschalen Aussagen
  „Die IP-Adresse wird nicht gespeichert“ und „ermöglicht keine Identifizierung“
  sind dadurch nicht für diese Installation belegt.
- Laut [Umami-FAQ](https://docs.umami.is/docs/faq) verwendet der Web-Tracker keine
  Cookies; selbst gehostete Installationen behalten Daten unbefristet, sofern sie
  nicht gelöscht werden. Eine tatsächliche Löschroutine ist hier **unbekannt**.
  Die Aussage im Datenschutztext zur Löschung ist daher noch nicht verifiziert.
- Die Live-Website antwortete mit GitHub-/Fastly-Headern; der Umami-Skriptserver
  mit einem nginx-Header. Das zeigt keine vollständige Infrastruktur oder Logkonfiguration.
  [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
  dokumentiert ausdrücklich die Speicherung von Besucher-IP-Adressen zu Sicherheitszwecken.
- Die [GitHub-Datenschutzerklärung](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement)
  beschreibt internationale Verarbeitung einschließlich USA sowie SCC und DPF.
  Sie nennt keine feste Pages-spezifische Logfrist. Welche Vertragsbedingungen
  MED-GO konkret abdecken, bleibt **unbekannt**; die öffentliche Erklärung ersetzt
  keine Prüfung der eigenen Vertragsbeziehung.
- netcup bietet einen [AVV im CCP unter Stammdaten → Auftragsverarbeitung](https://www.netcup.com/de/helpcenter/dokumentation/general/avv)
  an. Das belegt nicht, dass für diesen Server ein Vertrag abgeschlossen wurde.
  netcup hat [mehrere Serverstandorte](https://helpcenter.netcup.com/en/faq), auch
  außerhalb der EU; der Anbietername allein belegt keinen deutschen Standort.

#### Betriebliche Angaben: unbekannt

- Konkreter netcup-Serverstandort und gegebenenfalls separate Datenbank-/Backupstandorte.
- Rechtlicher Umami-Betreiber, Vertragsinhaber und Zugriffsberechtigte für Dashboard,
  Datenbank, Server und Backups; Verhältnis zur MED-GO e.G.
- Abgeschlossener netcup-AVV und gegebenenfalls Vereinbarung zwischen MED-GO und Betreiber.
- Installierte Umami-Version, serverseitige Anpassungen und zusätzliche Datenerfassung.
- Aufbewahrungsfristen und Löschverfahren für Analytics, Backups und Server-/Proxy-Logs;
  insbesondere Speicherung von IP-Adressen und vollständigen URLs in diesen Logs.
- Vollständige Liste zusätzlicher Proxys, CDNs und Monitoringdienste.
- GitHub-Vertragsinhaber und für MED-GO geltende Datenschutz-/Hostingvereinbarungen.
- Überwachte Datenschutz-E-Mail und gegebenenfalls öffentlicher Kontakt eines
  bestellten Datenschutzbeauftragten.

Rechtsgrundlage, Einwilligungsbedarf und öffentliche Datenschutzformulierungen
bleiben rechtlich zu prüfen. Die Website wurde bei dieser Recherche nicht geändert;
unbekannte Betriebsdetails werden nicht als Tatsachen veröffentlicht.

### Abgeschlossen oder nicht erforderlich

- **Druck:** Flyer und Visitenkarte sind laut Betreiber bereits gedruckt;
  eine Druckfreigabe ist kein offener Punkt mehr.
- **Unterpfad-Portabilität:** nicht erforderlich. Die Website bleibt für die
  eigene Domain mit `base: '/'` ausgelegt.

Astro-/Abhängigkeitsupdate, Hinweiszeitsteuerung, gemeinsame Sprechzeiten,
Flyer-Textextraktion, festes Datenschutz-Revisionsdatum, Hero-Komprimierung und
das Verschieben ungenutzter Bildvorlagen sind lokal umgesetzt. Eine Veröffentlichung
dieser Änderungen ist damit nicht dokumentiert oder freigegeben.
