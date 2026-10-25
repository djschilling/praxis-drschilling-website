# Visitenkarte – freigegebene Variante J

## Druckfassung

Ausgewählt ist **J – Waldgrün und Salbei**, zweiseitig 85 × 55 mm.
Die Datei zum Hochladen bei FLYERALARM liegt unter
[`druckdateien/Visitenkarte-J-85x55-Flyeralarm-Druck.pdf`](druckdateien/Visitenkarte-J-85x55-Flyeralarm-Druck.pdf).
Seite 1 ist die Vorderseite, Seite 2 die Sprechzeiten-Rückseite.
PNG-Dateien sind nur Ansichten, keine Druckdaten.
Die [Bestellhinweise](druckdateien/Visitenkarte-J-85x55-Flyeralarm-Bestellhinweise.txt)
nennen die erforderliche Konfiguration, insbesondere **4/4-farbig statt 4/0**.

- Datenformat 87 × 57 mm, TrimBox 85 × 55 mm, 1 mm Beschnitt umlaufend.
- Texte mindestens 3 mm innerhalb des Endformats; keine Marken oder Seitendrehungen.
- CMYK, ISO Coated v2 300% (ECI), eingebetteter FOGRA39-OutputIntent.
- PDF 1.3 mit PDF/X-3:2002-Kennung, keine Transparenzen.
- Fraunces und Figtree eingebettet; Text, Landschaft und Zeilenflächen als Vektoren.
- Original-Logo auf hellem Grund, nach CMYK konvertiert, effektiv ca. 808 ppi.
- Unveränderte Größen: Tageskürzel 14 pt, Uhrzeiten 16 pt, Telefon 26,5 pt,
  Webadresse 15,5 pt.

Der Druckexport (`--icc`) nutzt dieselbe Satzquelle wie der Entwurf.
Farben und Logo werden vor dem PDF-Satz profilgestützt nach CMYK konvertiert.
PyMuPDF ergänzt OutputIntent und PDF/X-Metadaten ohne erneute Interpretation des
Textes; die Unicode-Zuordnung einschließlich Gedankenstrichen bleibt erhalten.
Ghostscript wird nur zur unabhängigen Interpretation und Farbauftragsprüfung
verwendet, nicht zum Umschreiben der finalen PDF.

Geprüft wurden Seitenformat und Boxen, Randabstände, Einbettungen, Textgleichheit
vor/nach Export, genaue Tageszuordnung, Nummer und Domain, Mindestschriftgrößen,
RGB-Freiheit, Transparenzmasken und Annotationen. Beide finalen Ansichten wurden
visuell kontrolliert. Ghostscript 10.00.0 hat beide Seiten fehlerfrei interpretiert;
der bei 300 dpi gemessene maximale Farbauftrag betrug 259,2 % / 237,3 %.
Dies ist **kein zertifizierter PDF/X-Preflight oder Druckerei-Datencheck**.
FLYERALARM empfiehlt inzwischen PDF/X-4; verwendet wird wie beim Flyer der
weiterhin dokumentierte PDF/X-3-Export für die vollständig opake Gestaltung.
[Quelle: Druck-PDF-Anleitung](https://www.flyeralarm.com/blog/de/tutorial-druckfaehiges-pdf-mit-indesign-erstellen/).
Vor der Bestellung Druckereivorschau und Datencheck kontrollieren; Farben am
Bildschirm sind nicht verbindlich. Es wurde nichts bestellt oder hochgeladen.

### Druckfassung neu erzeugen

Getestet mit Python 3.11, ReportLab 5.1.0, PyMuPDF 2.0, fontTools 4.67.0,
Pillow 13.0.0. Abhängigkeiten in einer separaten Umgebung, nicht im Astro-Projekt:

```sh
uv venv /tmp/visitenkarten-venv
uv pip install --python /tmp/visitenkarten-venv/bin/python \
  'fonttools[woff]==4.67.0' 'Pillow==13.0.0' 'reportlab==5.1.0' 'PyMuPDF==2.0'
curl -fL https://eci.org/lib/exe/eci_offset_2009.zip -o /tmp/visitenkarte-eci.zip
unzip -p /tmp/visitenkarte-eci.zip ECI_Offset_2009/ISOcoated_v2_300_eci.icc \
  > /tmp/ISOcoated_v2_300_eci.icc
/tmp/visitenkarten-venv/bin/python design/visitenkarte/generate.py \
  --icc /tmp/ISOcoated_v2_300_eci.icc --out design/visitenkarte/druckdateien
```

Der Generator bricht bei abweichenden Zeitangaben gegenüber der freigegebenen
Druckfassung ab. Wenn sich Sprechzeiten ändern, Inhalte erneut abstimmen und die
genaue Inhaltsprüfung im Export aktualisieren. Das Maßblatt liegt unter
[`druckvorgaben/`](druckvorgaben/).

## Entwurfsrunde: I und J in Grün

Auf Grundlage der ausgewählten Tagesübersicht H. Beide Varianten haben eine
waldgrüne Vorderseite mit heller Schrift, dem unveränderten Original-Logo auf
einem hellen Feld und Landschaftsflächen in Salbei und Gold am unteren Rand.
Telefonnummer: 26,5 pt; Webadresse: 15,5 pt; Praxisname: 13,2 pt;
MVZ Gomaringen: 15,5 pt. Die hellen Texte auf dunklem Grund sind damit gegenüber
H um rund 10 % vergrößert (vgl. [DBSV-Empfehlung](https://leserlich.info/zeichen/schriftgroesse)).

- **I – Waldgrün und Hell:** helle Rückseite mit zarten salbeifarbenen Wechselzeilen.
- **J – Waldgrün und Salbei:** salbeifarbene Rückseite mit helleren Wechselzeilen,
  angelehnt an die frühere Farbvariante B.

Beide Rückseiten erhalten die Tageskürzel in 14 pt und die Uhrzeiten in 16 pt.
Format, Original-Logo, Sprechzeiten, Telefon und Webadresse bleiben unverändert.
Ohne `--icc` erzeugt der Generator weiterhin die RGB-Entwürfe I und J;
mit `--variants G H` lässt sich die vorherige Auswahlrunde reproduzieren.
Diese Entwurfs-PDFs haben keinen Beschnitt und sind nicht für den Druckupload.

## Vorherige Auswahlrunde: G und H mit Webadresse

Beide Varianten sind zweiseitig im Format 85 × 55 mm. Die neue gemeinsame
Vorderseite enthält das Original-Logo, den Praxisnamen in 12 pt, MVZ Gomaringen
in 14 pt, die Telefonnummer in 24 pt und **mvz-gomaringen.de in 14 pt**.
Die Domain wird aus `src/data/praxis.ts` übernommen. Die Landschaft bleibt auf
der Vorderseite; die Rückseite ist ausschließlich den Sprechzeiten gewidmet.

- **G – Zusammengefasste Zeiten:** Mo–Fr in 16 pt, Vormittagszeit in 22 pt,
  zusätzliche Nachmittagszeiten in 18 pt. Weitere Beschriftungen mindestens 14 pt.
- **H – Tagesübersicht:** Tageskürzel in 14 pt, Uhrzeiten in 16 pt; dezente
  Wechselzeilen. Kürzel statt ausgeschriebener Tage ermöglichen die größeren Zahlen.

Grundlage der Größenwahl: [UKAAF, Clear Print / Large Print](https://www.ukaaf.org/wp-content/uploads/2024/12/G003-UKAAF-Creating-clear-print-and-large-print-documents-v4.pdf)
(12 pt Minimum, 14 pt empfohlen für Clear Print; 16/18 pt für Large Print)
und [DBSV, Schriftgröße](https://leserlich.info/zeichen/schriftgroesse).
Das ist eine Gestaltungsentscheidung, keine Bestätigung vollständiger
Barrierefreiheit. Wichtig bleiben reale Buchstabenhöhe, Kontrast, Leseabstand
und ein Ausdruck in Originalgröße. Für G/H muss 4/4-Druck gewählt werden.

Frühere Varianten sind mit `--variants A B C D E F` weiterhin reproduzierbar.

## Frühere Entwürfe

Format: 85 × 55 mm, quer. A und B sind zweiseitig, C ist einseitig.

- **A – Hell und ruhig:** helle Vorder- und Rückseite, große Telefonnummer,
  dezentes Landschaftsmotiv als Verbindung zum ausgewählten Flyer. Empfehlung.
- **B – Waldgrün und Salbei:** dunkle Vorderseite, Original-Logo auf hellem Feld,
  salbeifarbene Rückseite mit Sprechzeiten.
- **C – Alles auf einer Seite:** Marke oben, Telefonnummer im Salbeiband,
  kompakte Sprechzeitentabelle darunter. Kleinere Schrift als A/B.
- **D – Größere klassische Tabelle:** Tageskürzel, vollständige Uhrzeiten in
  Figtree 600 mit 12 pt statt bisher 8,2 pt.
- **E – Größtmögliche Zeiten:** gemeinsame Vormittage Mo–Fr in 22 pt,
  zusätzliche Nachmittage Mo + Mi und Fr in 18 pt. Keine fünf Tageszeilen.
- **F – Große Tagesliste:** ausgeschriebene Tage in 10,5 pt und verkürzte
  Uhrzeiten (8–12 statt 8:00–12:00) in 14 pt, dezente Wechselzeilen.

D/E/F sind zweiseitig mit der hellen Vorderseite von A. Ihre Rückseiten lassen
das Landschaftsmotiv und kleine Spaltenüberschriften zugunsten größerer Zahlen
weg. Für den Druck ist ebenfalls 4/4 erforderlich. E bietet die größten Zahlen,
F behält die direkte Zuordnung je Wochentag bei. Die Bildschirmvergrößerung
ersetzt keine Beurteilung eines Ausdrucks bei 100 % im echten Kartenformat.

Original-Logo: `public/images/brand/landschaft-c.png`, unverändert eingebunden.
Schriften: Fraunces 550 sowie Figtree 400/600 aus den Website-WOFF2-Dateien.
Farben und Landschaftsformen orientieren sich an `design/flyer-webseite/`.
Die visuelle Exploration erfolgte mit Painter; die gezeigten finalen Vorschauen
sind reproduzierbarer PDF-Satz mit echten Schriften und dem Originalbild.

Die Sprechzeiten werden beim Erzeugen direkt aus `src/pages/index.astro`
übernommen: Montag bis Freitag 8:00–12:00, Montag/Mittwoch zusätzlich
16:00–18:00, Freitag zusätzlich 15:00–16:00 Uhr.
Telefon: 07072 / 7031. Keine Adresse, QR-Codes oder Werbetexte.
G/H enthalten zusätzlich die Webadresse; A–F entstanden noch ohne Webadresse.

## Reproduktion

```sh
uv venv /tmp/visitenkarten-venv
uv pip install --python /tmp/visitenkarten-venv/bin/python \
  'fonttools[woff]' Pillow reportlab PyMuPDF
/tmp/visitenkarten-venv/bin/python design/visitenkarte/generate.py
```

Ausgaben: `.amp/in/artifacts/visitenkarte/`, mit `--out` änderbar.
Pro Variante entstehen eine Entwurfs-PDF, Einzelansichten bei 300 dpi und eine
beschriftete Vergleichsansicht. Die Beschriftungen stehen außerhalb der Karte.
Der Generator prüft die Seitenzahl, Textbreiten sowie das Vorhandensein der
Telefonnummer und aller Tages-/Zeitangaben im erzeugten PDF.

**Entwürfe ohne `--icc` sind keine Druckdaten:** RGB, ohne Beschnitt.
Nach Auswahl müssen Beschnitt, Sicherheitsabstände, Farbprofil und Export an
das Datenblatt des tatsächlich bestellten Visitenkartenprodukts angepasst werden.
Bildschirmfarben sind nicht farbverbindlich. Es wurde nichts bestellt.

## Vorgeschlagenes Druckprodukt

Am 25.10.2026 geprüfter [FLYERALARM-AT-Link](https://www.flyeralarm.com/at/p/visitenkarten-klassiker-4321237.html#/p/FV-4321679&/l/7050):
Querformat 8,5 × 5,5 cm, 300 g Bilderdruck matt PEFC, keine Veredelung,
4/0-farbig (einseitig CMYK), ein Motiv. Diese Einstellung passt zur einseitigen
Variante C. Für die zweiseitigen Varianten A und B muss 4/4 gewählt werden.

Empfehlung: dieses Standardprodukt auf mattem Bilderdruckpapier, ohne zusätzliche
Veredelung. 300 g/m² ist für die Praxis ausreichend; glänzende Beschichtung,
Goldfolie und Spezialmaterialien sind für den Entwurf nicht nötig.
Der Goldton ist eine gedruckte Farbe und kein Metallic-Effekt.

Das vom Konfigurator verlinkte [Original-Datenblatt](https://www.flyeralarm.com/sheets/de/vk_mass_q.pdf)
ist lokal unter [`druckvorgaben/FLYERALARM-Visitenkarte-85x55-Datenblatt.pdf`](druckvorgaben/FLYERALARM-Visitenkarte-85x55-Datenblatt.pdf)
gespeichert. Vorgaben daraus:

- Endformat 85 × 55 mm, Datenformat 87 × 57 mm.
- Umlaufend 1 mm Beschnitt; Hintergründe bis zum Datenformatrand führen.
- Sicherheitsabstand 3 mm innerhalb des Endformats.
- Keine Seitendrehungen im Druck-PDF; Hoch- und Querformat nicht mischen.

Das Maßblatt nennt keine zusätzlichen Vorgaben zu Auflösung, Farbprofil,
Schrifteinbettung oder PDF/X-Version. Diese müssen vor einem Druckexport separat
mit den aktuellen allgemeinen Druckdatenvorgaben abgeglichen werden.
Die Entwurfs-PDFs sind dadurch noch nicht zu Druckdateien geworden; für die
ausgewählte Variante J ist die separate Druckfassung oben maßgeblich.
Der Zusatz „Alle Zeiten in Uhr“ wurde auf Wunsch aus A und B entfernt.
