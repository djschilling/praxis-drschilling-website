# Flyer zur neuen Webseite – FLYERALARM A6

Reproduzierbare Druckfassung des ausgewählten Entwurfs „Die Webadresse im
Mittelpunkt“. Keine KI-generierten Texte oder QR-Code-Platzhalter: Schrift,
QR-Code, Piktogramme und Landschaftsflächen werden neu als Vektoren aufgebaut.
Das vorhandene Praxislogo wird unverändert als hochaufgelöstes Bild verwendet.

Die vorbereitete Druck-PDF, beide Vorschau-PNGs und die Bestellhinweise liegen
unter [`druckdateien/`](druckdateien/). Nur die Datei mit der Endung `-Druck.pdf`
ist für den Upload bei FLYERALARM vorgesehen.

## Druckprodukt und Dateien

- Standard-Flyer, DIN A6 hoch, ungefalzt, beidseitig 4/4-farbig.
- Endformat 105 × 148 mm; Datenformat 107 × 150 mm.
- 1 mm Beschnitt umlaufend; mindestens 4 mm Sicherheitsabstand zum Endformat.
- Eine PDF mit zwei Einzelseiten: Vorderseite, dann Rückseite; keine Druckbögen,
  Schnittmarken, Beschriftungen oder Drehungen im Druck-PDF.
- CMYK, ISO Coated v2 300% (ECI), eingebetteter OutputIntent FOGRA39.
- PDF/X-3:2002 (PDF 1.3), ohne Transparenzen; Fraunces und Figtree eingebettet.
- QR-Code als Vektor, 100 % Schwarz, mit vier Modulen Ruhezone. Ziel:
  `https://mvz-gomaringen.de` (kein Kurzlink oder kostenpflichtiger QR-Dienst).
- Logo: Original-PNG, in CMYK konvertiert, effektiv ca. 808 ppi.
- Papierempfehlung: 250 g/m² Bilderdruck matt, keine zusätzliche Veredelung.
  Die Empfehlung ist keine bereits bestellte oder verbindlich gewählte Ausführung.

Die PDF ist für diesen Standard-Flyer vorbereitet, nicht für beliebige Naturpapiere,
Sonderfarben, abgerundete Ecken oder andere Produkte. Vor einer Bestellung muss
das Datenblatt des tatsächlich konfigurierten Produkts weiterhin 107 × 150 mm
und 1 mm Beschnitt ausweisen. Druckereivorschau/Datencheck kontrollieren und
Inhalte freigeben. Eine Freigabe oder Bestellung bei FLYERALARM erfolgte nicht.
Bildschirmdarstellung ersetzt keinen farbverbindlichen Proof.

## Quellen der Vorgaben

- [Offizielles Datenblatt Flyer DIN A6](https://www.flyeralarm.com/sheets/de/flyer_a6_mass.pdf)
- [FLYERALARM: Druckfähiges PDF erstellen](https://www.flyeralarm.com/blog/de/tutorial-druckfaehiges-pdf-mit-indesign-erstellen/)
- [ECI-Profilpaket Offset 2009](https://eci.org/lib/exe/eci_offset_2009.zip)

Die FLYERALARM-Anleitung dokumentiert PDF/X-3:2002 und empfiehlt seit dem Update
2025 PDF/X-4. Hier wird der weiterhin dokumentierte PDF/X-3-Export verwendet;
die Gestaltung benötigt keine Transparenzen oder andere PDF/X-4-Funktionen.

## Reproduktion

Systemvoraussetzung: Ghostscript (`gs`). Python-Abhängigkeiten in einer separaten
Umgebung installieren; der Astro-Abhängigkeitsbaum wird nicht verändert:

```sh
uv venv /tmp/flyer-venv
uv pip install --python /tmp/flyer-venv/bin/python \
  'fonttools[woff]' Pillow reportlab PyMuPDF qrcode zxing-cpp
curl -L https://eci.org/lib/exe/eci_offset_2009.zip -o /tmp/eci-offset.zip
unzip -p /tmp/eci-offset.zip ECI_Offset_2009/ISOcoated_v2_300_eci.icc \
  > /tmp/ISOcoated_v2_300_eci.icc
/tmp/flyer-venv/bin/python design/flyer-webseite/generate.py \
  --icc /tmp/ISOcoated_v2_300_eci.icc
```

Ausgaben unter `.amp/in/artifacts/` (mit `--out` änderbar): Druck-PDF,
Ghostscript-Exportprotokoll sowie beschnittene PNG-Ansichten beider Seiten.

Der Export prüft Seitenformat, TrimBox, Drehung, Textränder, eingebettete
Schriften und ICC-Profil, PDF/X-Kennung, RGB-Farbräume, Transparenzmasken,
Annotationen und den QR-Code aus der finalen PDF bei 300 dpi. Diese Prüfungen
sind kein vollständiger zertifizierter PDF/X-Preflight und kein Druckerei-Datencheck.

Die statischen Fontinstanzen werden direkt aus den Website-WOFF2-Dateien mit
deren Standardachsen erzeugt: Fraunces 550/600, Figtree 400/600. Änderungen an
Texten oder Gestaltung gehören in `generate.py`; nach Änderungen neu exportieren,
Prüfungen ausführen und beide gerenderten Ansichten visuell kontrollieren.
