"""Rebuild the approved website-announcement flyer for standard FLYERALARM A6.

Run with the repository fonts, ECI ISOcoated_v2_300_eci.icc, and Ghostscript.
See README.md for dependencies, sources, and print settings.
"""

import argparse
import io
from pathlib import Path
import re
import subprocess
import tempfile

from fontTools.ttLib import TTFont as OpenTypeFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageCms
import pymupdf as fitz
import qrcode
from reportlab.lib.colors import CMYKColor
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import zxingcpp


ROOT = Path(__file__).resolve().parents[2]
URL = 'https://mvz-gomaringen.de'
WIDTH, HEIGHT, BLEED = 105, 148, 1
PREFIX = 'Flyer-Webseite-A6-Flyeralarm'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--icc', required=True, type=Path)
    parser.add_argument('--out', type=Path, default=ROOT / '.amp/in/artifacts')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    profile = args.icc.resolve()
    srgb = ImageCms.createProfile('sRGB')
    cmyk = ImageCms.getOpenProfile(str(profile))
    convert = ImageCms.buildTransformFromOpenProfiles(srgb, cmyk, 'RGB', 'CMYK', renderingIntent=1, flags=0x2000)

    def color(hex_color):
        pixel = Image.new('RGB', (1, 1), hex_color)
        values = ImageCms.applyTransform(pixel, convert).getpixel((0, 0))
        return CMYKColor(*(value / 255 for value in values))

    green, body, gold = map(color, ['#164039', '#243e38', '#c4a35a'])
    cream, sage, sage_light = map(color, ['#f7faf8', '#bfd2c9', '#dbe6df'])
    white, black = CMYKColor(0, 0, 0, 0), CMYKColor(0, 0, 0, 1)

    with tempfile.TemporaryDirectory(prefix='flyer-print-') as tmp:
        tmp = Path(tmp)
        for family, weight in [('Fraunces', 550), ('Fraunces', 600), ('Figtree', 400), ('Figtree', 600)]:
            font = OpenTypeFont(ROOT / f'public/fonts/{family.lower()}-latin-variable.woff2')
            axes = {axis.axisTag: axis.defaultValue for axis in font['fvar'].axes}
            axes['wght'] = weight
            font = instantiateVariableFont(font, axes, inplace=True)
            font.flavor = None
            for record in font['name'].names:
                if record.nameID == 6:
                    record.string = f'{family}-{weight}'.encode(record.getEncoding())
            file = tmp / f'{family}{weight}.ttf'
            font.save(file)
            pdfmetrics.registerFont(TTFont(f'{family}{weight}', str(file)))

        logo = Image.open(ROOT / 'public/images/brand/landschaft-c.png').convert('RGBA')
        flattened = Image.new('RGB', logo.size, '#f7faf8')
        flattened.paste(logo, mask=logo.getchannel('A'))
        logo_cmyk = ImageCms.applyTransform(flattened, convert)
        logo_data = io.BytesIO()
        logo_cmyk.save(logo_data, format='TIFF', compression='tiff_lzw')
        logo_reader = ImageReader(logo_data)

        intermediate = tmp / 'artwork.pdf'
        c = canvas.Canvas(str(intermediate), pagesize=(107*mm, 150*mm), pageCompression=1, pdfVersion=(1, 3), enforceColorSpace='CMYK')
        c.setTitle('Neue Webseite – MVZ Gomaringen – Flyer A6')
        c.setAuthor('MVZ Gomaringen · Praxis Dr. Bernd Schilling')
        c.setSubject('Beidseitiger Flyer, DIN A6 hoch, 1 mm Beschnitt')

        def rect(x, y, w, h, fill):
            c.setFillColor(fill)
            c.rect(x*mm, (HEIGHT-y-h)*mm, w*mm, h*mm, fill=1, stroke=0)

        def circle(x, y, r, fill=None):
            if fill is not None:
                c.setFillColor(fill)
            c.circle(x*mm, (HEIGHT-y)*mm, r*mm, fill=fill is not None, stroke=fill is None)

        def curve(commands, fill=None, stroke=None, width=.3):
            p = c.beginPath()
            for command in commands:
                op, *v = command
                points = [value*mm if i % 2 == 0 else (HEIGHT-value)*mm for i, value in enumerate(v)]
                if op == 'M': p.moveTo(*points)
                elif op == 'L': p.lineTo(*points)
                elif op == 'C': p.curveTo(*points)
                elif op == 'Z': p.close()
            if fill is not None: c.setFillColor(fill)
            if stroke is not None: c.setStrokeColor(stroke)
            c.setLineWidth(width*mm)
            c.drawPath(p, fill=fill is not None, stroke=stroke is not None)

        def line(x1, y1, x2, y2, stroke=gold, width=.35):
            curve([('M', x1, y1), ('L', x2, y2)], stroke=stroke, width=width)

        def text(value, x, y, size=10, font='Figtree400', fill=body, tracking=0):
            t = c.beginText(x*mm, (HEIGHT-y)*mm)
            t.setFont(font, size)
            t.setFillColor(fill)
            t.setCharSpace(tracking)
            t.textOut(value)
            c.drawText(t)

        def brand():
            # Original bitmap at >800 ppi; no AI-redrawn logo.
            c.drawImage(logo_reader, 8*mm, (HEIGHT-7-12)*mm, 16.6*mm, 12*mm)
            text('MVZ Gomaringen', 27.3, 12.2, 11.5, 'Fraunces550', green, -.12)
            text('Praxis Dr. Schilling · Hausarzt', 27.3, 16.3, 7.2)
            line(8, 22.2, 16.2, 22.2)

        def landscape(front):
            if front:
                circle(86.8, 125.8, 9.5, gold)
                curve([('M', -1, 138), ('C', 18, 137, 29, 120, 47, 120.6), ('C', 65, 120, 78, 130, 106, 130), ('L', 106, 149), ('L', -1, 149), ('Z',)], green)
                curve([('M', -1, 135.3), ('C', 23, 127.8, 45, 133.3, 62, 136), ('C', 79, 138, 91, 137, 106, 136), ('L', 106, 149), ('L', -1, 149), ('Z',)], sage)
                curve([('M', 21, 149), ('C', 45, 132.6, 69, 129.8, 106, 130.5), ('L', 106, 132.5), ('C', 74, 133.4, 55, 140.1, 39, 149), ('Z',)], cream)
                curve([('M', 27, 149), ('C', 48, 134.5, 75, 130.8, 106, 131.2), ('L', 106, 132), ('C', 78, 133.7, 56, 141.5, 42, 149), ('Z',)], gold)
                curve([('M', 40, 149), ('C', 63, 136, 84, 133.5, 106, 133.2), ('L', 106, 149), ('Z',)], green)
            else:
                curve([('M', -1, 135), ('C', 19, 127.8, 34, 133.8, 50, 134.3), ('C', 74, 134.8, 81, 124.5, 106, 128.6), ('L', 106, 149), ('L', -1, 149), ('Z',)], sage_light)
                curve([('M', -1, 142), ('C', 24, 133, 50, 139, 69, 134), ('C', 84, 130.3, 94, 130.4, 106, 132), ('L', 106, 149), ('L', -1, 149), ('Z',)], sage)
                curve([('M', 28, 149), ('C', 48, 136.2, 72, 132, 91, 131.1), ('C', 68, 137.3, 52, 143, 44, 149), ('Z',)], cream)
                curve([('M', 33, 149), ('C', 52, 136.7, 75, 132.4, 90, 131.5), ('C', 68, 137.6, 56, 143.9, 47, 149), ('Z',)], gold)
                curve([('M', 47, 149), ('C', 68, 136.1, 87, 133.3, 106, 135.5), ('L', 106, 149), ('Z',)], sage_light)

        def icon(kind, x, y):
            circle(x, y, 7.1, sage_light)
            c.setStrokeColor(green)
            c.setLineWidth(.32*mm)
            c.setLineCap(1)
            c.setLineJoin(1)
            if kind == 'notice':
                curve([('M', x-2.2, y-3.2), ('L', x+2.2, y-3.2), ('L', x+2.2, y+3.2), ('L', x-2.2, y+3.2), ('Z',)], stroke=green)
                for dy in [-1.8, -.3, 1.2]: line(x-1.2, y+dy, x+1.2, y+dy, green, .25)
            elif kind == 'clock':
                circle(x, y, 3.1)
                curve([('M', x, y-2), ('L', x, y), ('L', x+1.65, y+.9)], stroke=green)
            else:
                circle(x, y-1.9, 1.05)
                circle(x-3, y-.8, .8)
                circle(x+3, y-.8, .8)
                curve([('M', x-1.8, y+2.7), ('L', x-1.8, y+1.7), ('C', x-1.8, y+.2, x+1.8, y+.2, x+1.8, y+1.7), ('L', x+1.8, y+2.7)], stroke=green)
                for sign in [-1, 1]:
                    curve([('M', x+sign*3.9, y+1.9), ('L', x+sign*3.9, y+1.1), ('C', x+sign*3.9, y+.4, x+sign*2.7, y+.1, x+sign*2.5, y+.8)], stroke=green)

        for side in ['front', 'back']:
            c.setTrimBox((1*mm, 1*mm, 106*mm, 149*mm))
            c.setBleedBox((0, 0, 107*mm, 150*mm))
            c.saveState()
            c.translate(mm, mm)
            rect(-1, -1, 107, 150, cream)
            brand()
            if side == 'front':
                text('NEU IM WEB', 8, 31.4, 8.5, 'Figtree600', gold, 1.4)
                text('Unsere neue', 8, 44, 33, 'Fraunces600', green, -.40)
                text('Webseite ist da.', 8, 56.8, 33, 'Fraunces600', green, -.40)
                text('mvz-gomaringen.de', 8, 70.5, 26.5, 'Figtree600', green, -.35)
                c.setFillColor(white)
                c.roundRect(8*mm, (HEIGHT-78-40)*mm, 40*mm, 40*mm, 2*mm, fill=1, stroke=0)
                qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=4)
                qr.add_data(URL)
                qr.make(fit=True)
                matrix = qr.get_matrix()
                unit = 38 / len(matrix)
                p = c.beginPath()
                for row, cells in enumerate(matrix):
                    for col, on in enumerate(cells):
                        if on: p.rect((9+col*unit)*mm, (HEIGHT-79-(row+1)*unit)*mm, unit*mm, unit*mm)
                c.setFillColor(black)
                c.drawPath(p, stroke=0, fill=1)
                curve([('M', 66, 94), ('C', 65, 89.5, 60, 87.5, 52, 89.4)], stroke=gold, width=.4)
                curve([('M', 53.2, 87.8), ('L', 52, 89.4), ('L', 54.6, 89.8)], stroke=gold, width=.4)
                text('Scannen und', 60, 99, 10.3)
                text('entdecken.', 60, 103.7, 10.3)
                landscape(True)
            else:
                text('Gut zu wissen.', 8, 35.8, 30.5, 'Fraunces600', green, -.37)
                text('Leicht zu finden.', 8, 48, 30.5, 'Fraunces600', green, -.37)
                for y, kind, title, subtitle in [
                    (60.5, 'notice', 'Aktuelle Hinweise', 'Wichtige Informationen auf einen Blick.'),
                    (77, 'clock', 'Sprechzeiten & Kontakt', 'Öffnungszeiten und Kontaktdaten.'),
                    (93.5, 'team', 'Leistungen & Team', 'Ein Überblick für Sie.'),
                ]:
                    icon(kind, 15, y)
                    text(title, 27, y-1, 11.5, 'Figtree600', green)
                    text(subtitle, 27, y+4, 8.5)
                text('Alles übersichtlich auf unserer neuen Webseite.', 8, 107.5, 8.7)
                line(8, 112.6, 16.2, 112.6)
                text('mvz-gomaringen.de', 8, 122, 26.5, 'Figtree600', green, -.35)
                landscape(False)
            c.restoreState()
            c.showPage()
        c.save()

        prefix = tmp / 'pdfx.ps'
        prefix.write_text(f'''%!
[/GTS_PDFXVersion (PDF/X-3:2002) /Title (Neue Webseite - MVZ Gomaringen - Flyer A6) /Trapped /False /DOCINFO pdfmark
[/_objdef {{icc}} /type /stream /OBJ pdfmark
[{{icc}} << /N 4 >> /PUT pdfmark
[{{icc}} ({profile}) (r) file /PUT pdfmark
[/_objdef {{oi}} /type /dict /OBJ pdfmark
[{{oi}} << /Type /OutputIntent /S /GTS_PDFX /OutputCondition (ISO Coated v2 300% ECI)
/OutputConditionIdentifier (FOGRA39) /RegistryName (http://www.color.org)
/Info (ISO Coated v2 300% ECI) /DestOutputProfile {{icc}} >> /PUT pdfmark
[{{Catalog}} << /OutputIntents [{{oi}}] >> /PUT pdfmark
''')
        output = args.out / f'{PREFIX}-Druck.pdf'
        command = [
            'gs', '-dBATCH', '-dNOPAUSE', '-dSAFER', f'--permit-file-read={profile}',
            '-sDEVICE=pdfwrite', '-dPDFX', '-dCompatibilityLevel=1.3',
            '-sColorConversionStrategy=CMYK', '-dProcessColorModel=/DeviceCMYK',
            f'-sOutputICCProfile={profile}', '-dEmbedAllFonts=true', '-dSubsetFonts=true',
            '-dDownsampleColorImages=false', '-dDownsampleGrayImages=false',
            '-dAutoRotatePages=/None', f'-sOutputFile={output}', str(prefix), str(intermediate),
        ]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        (args.out / f'{PREFIX}-Exportprotokoll.txt').write_text(result.stdout + result.stderr)

    doc = fitz.open(output)
    assert len(doc) == 2
    assert doc.metadata['format'] == 'PDF 1.3', doc.metadata
    info = int(doc.xref_get_key(-1, 'Info')[1].split()[0])
    assert doc.xref_get_key(info, 'GTS_PDFXVersion')[1] == 'PDF/X-3:2002'
    assert doc.xref_get_key(info, 'Trapped')[1] == '/False'
    assert doc.xref_get_key(doc.pdf_catalog(), 'OutputIntents')[0] == 'array'
    embedded_profiles = [doc.xref_stream(xref) for xref in range(1, doc.xref_length()) if doc.xref_is_stream(xref) and '/N 4' in doc.xref_object(xref)]
    assert profile.read_bytes() in embedded_profiles, 'ECI output profile must be embedded unchanged'
    assert not doc.is_encrypted
    for xref in range(1, doc.xref_length()):
        obj = doc.xref_object(xref)
        assert '/DeviceRGB' not in obj and '/SMask' not in obj
    qr_results = []
    for i, page in enumerate(doc):
        assert page.rotation == 0
        assert abs(page.rect.width/mm-107) < .01 and abs(page.rect.height/mm-150) < .01
        assert abs(page.trimbox.width/mm-105) < .01 and abs(page.trimbox.height/mm-148) < .01
        assert not list(page.annots() or []) and not page.get_links()
        assert not re.search(rb'\s(?:rg|RG)\s', page.read_contents())
        for block in page.get_text('dict')['blocks']:
            for line_ in block.get('lines', []):
                for span in line_['spans']:
                    safe = fitz.Rect(5*mm, 5*mm, 102*mm, 145*mm)
                    assert safe.contains(fitz.Rect(span['bbox'])), (i, span['text'], span['bbox'])
        fonts = page.get_fonts(full=True)
        assert fonts and all(doc.extract_font(font[0])[3] for font in fonts)
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
        img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        qr_results += [barcode.text for barcode in zxingcpp.read_barcodes(img)]
        cropped = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=page.trimbox)
        preview = args.out / f'{PREFIX}-{"Vorderseite" if i == 0 else "Rueckseite"}.png'
        cropped.save(str(preview))
    assert qr_results == [URL], qr_results
    print('OK: 2 Seiten, 107 × 150 mm, TrimBox 105 × 148 mm, 1 mm Beschnitt, 0° Drehung.')
    print('OK: Alle Schriften eingebettet, Texte ≥4 mm innerhalb des Endformats.')
    print('OK: PDF/X-3-Kennung, ECI-OutputIntent, kein RGB, keine Transparenzmasken oder Annotationen.')
    print(f'OK: QR aus der finalen Druck-PDF bei 300 dpi dekodiert: {qr_results[0]}')
    print(output)


if __name__ == '__main__':
    main()
