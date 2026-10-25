"""Render business-card concepts using the original logo and website fonts.

Default: RGB concepts without bleed. With --icc: approved J as CMYK PDF/X-3
with 1 mm bleed. Dependencies: fonttools[woff], Pillow, reportlab, PyMuPDF;
print export additionally requires ISOcoated_v2_300_eci.icc.
"""

import argparse
import io
from pathlib import Path
import re
import tempfile

from fontTools.ttLib import TTFont as OpenTypeFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageCms, ImageDraw, ImageFont
import pymupdf
from reportlab.lib.colors import CMYKColor, HexColor
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
GREEN, CREAM, SAGE, GOLD = '#164039', '#f7faf8', '#bfd2c9', '#c4a35a'
WIDTH, HEIGHT = 85, 55
PRINT_PREFIX = 'Visitenkarte-J-85x55-Flyeralarm'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / '.amp/in/artifacts/visitenkarte')
    parser.add_argument('--variants', nargs='+', choices=list('ABCDEFGHIJ'))
    parser.add_argument('--icc', type=Path, help='Enable print export of J with this CMYK profile')
    args = parser.parse_args()
    args.variants = args.variants or (['J'] if args.icc else ['I', 'J'])
    if args.icc and args.variants != ['J']:
        parser.error('Print export is supported only for the approved variant J')
    if args.icc:
        args.icc = args.icc.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    source = (ROOT / 'src/pages/index.astro').read_text()
    block = source.split('const oeffnungszeiten = [', 1)[1].split('];', 1)[0]
    hours = re.findall(r"tag: '([^']+)', zeit: '([^']+)'", block)
    assert len(hours) == 5
    website = re.search(r"website: '([^']+)'", (ROOT / 'src/data/praxis.ts').read_text()).group(1)
    domain = website.removeprefix('https://').rstrip('/')
    rows = []
    for day, value in hours:
        sessions = value.removesuffix(' Uhr').split(' und ')
        rows.append((day, sessions[0], sessions[1] if len(sessions) == 2 else '–'))

    with tempfile.TemporaryDirectory(prefix='visitenkarte-') as tmp:
        tmp = Path(tmp)
        logo_reader = str(ROOT / 'public/images/brand/landschaft-c.png')
        if args.icc:
            transform = ImageCms.buildTransformFromOpenProfiles(
                ImageCms.createProfile('sRGB'), ImageCms.getOpenProfile(str(args.icc)),
                'RGB', 'CMYK', renderingIntent=1, flags=0x2000)
            logo = Image.open(logo_reader).convert('RGBA')
            flattened = Image.new('RGB', logo.size, CREAM)
            flattened.paste(logo, mask=logo.getchannel('A'))
            logo_data = io.BytesIO()
            ImageCms.applyTransform(flattened, transform).save(logo_data, format='TIFF', compression='tiff_lzw')
            logo_reader = ImageReader(logo_data)

        def color(value):
            if not args.icc:
                return HexColor(value)
            pixel = ImageCms.applyTransform(Image.new('RGB', (1, 1), value), transform)
            return CMYKColor(*(channel/255 for channel in pixel.getpixel((0, 0))), alpha=None)

        fonts = {}
        for family, weight in [('Fraunces', 550), ('Figtree', 400), ('Figtree', 600)]:
            font = OpenTypeFont(ROOT / f'public/fonts/{family.lower()}-latin-variable.woff2')
            axes = {axis.axisTag: axis.defaultValue for axis in font['fvar'].axes}
            axes['wght'] = weight
            font = instantiateVariableFont(font, axes, inplace=True)
            font.flavor = None
            for record in font['name'].names:
                if record.nameID == 6:
                    record.string = f'{family}-{weight}'.encode(record.getEncoding())
            path = Path(tmp) / f'{family}{weight}.ttf'
            font.save(path)
            name = f'{family}{weight}'
            pdfmetrics.registerFont(TTFont(name, str(path)))
            fonts[name] = path

        for variant in args.variants:
            for name, path in fonts.items():
                pdfmetrics.registerFont(TTFont(name, str(path)))
            file = tmp / 'artwork.pdf' if args.icc else args.out / f'Visitenkarte-{variant}-Entwurf.pdf'
            bleed = 1 if args.icc else 0
            c = canvas.Canvas(str(file), pagesize=((WIDTH+2*bleed)*mm, (HEIGHT+2*bleed)*mm),
                              pdfVersion=(1, 3), enforceColorSpace='CMYK' if args.icc else None,
                              initialFontName='Figtree400')
            c.setTitle('MVZ Gomaringen – Visitenkarte J – Druck' if args.icc else
                       f'Visitenkarte {variant} – Gestaltungsentwurf, nicht druckfertig')
            c.setAuthor('MVZ Gomaringen · Praxis Dr. Bernd Schilling')

            def begin_page():
                if args.icc:
                    c.setTrimBox((mm, mm, 86*mm, 56*mm))
                    c.setBleedBox((0, 0, 87*mm, 57*mm))
                    c.translate(mm, mm)

            begin_page()

            def rect(x, y, w, h, fill):
                if args.icc and x == 0 and w == WIDTH:
                    x, w = -1, WIDTH+2
                    if y == 0 and h == HEIGHT:
                        y, h = -1, HEIGHT+2
                c.setFillColor(color(fill))
                c.rect(x*mm, (HEIGHT-y-h)*mm, w*mm, h*mm, fill=1, stroke=0)

            def text(value, x, y, size=9, font='Figtree400', fill=GREEN):
                assert x*mm + pdfmetrics.stringWidth(value, font, size) <= (WIDTH-4)*mm, value
                c.setFillColor(color(fill))
                c.setFont(font, size)
                c.drawString(x*mm, (HEIGHT-y)*mm, value)

            def line(x1, y, x2, fill=GOLD, width=.25):
                c.setStrokeColor(color(fill))
                c.setLineWidth(width*mm)
                c.line(x1*mm, (HEIGHT-y)*mm, x2*mm, (HEIGHT-y)*mm)

            def landscape():
                for fill, points in [
                    (GREEN, [(-1, 51), (22, 39, 45, 49, 86, 48)]),
                    (SAGE, [(-1, 49), (24, 43, 43, 56, 86, 51)]),
                    (GOLD, [(31, 56), (49, 49, 65, 47, 86, 48)]),
                ]:
                    p = c.beginPath()
                    p.moveTo(points[0][0]*mm, (HEIGHT-points[0][1])*mm)
                    a, b, d, e, f, g = points[1]
                    p.curveTo(a*mm, (HEIGHT-b)*mm, d*mm, (HEIGHT-e)*mm, f*mm, (HEIGHT-g)*mm)
                    p.lineTo(86*mm, -mm)
                    p.lineTo(points[0][0]*mm, -mm)
                    p.close()
                    c.setFillColor(color(fill))
                    c.drawPath(p, fill=1, stroke=0)

            def brand(dark=False, compact=False):
                if dark:
                    rect(5, 5, 17, 14, CREAM)
                c.drawImage(str(ROOT / 'public/images/brand/landschaft-c.png'),
                            6*mm, (HEIGHT-7-10.8)*mm, 15*mm, 10.8*mm, mask='auto')
                text('MVZ Gomaringen', 25, 11.8, 12, 'Fraunces550', CREAM if dark else GREEN)
                text('Praxis Dr. Bernd Schilling', 25, 16.4, 7.4, fill=CREAM if dark else GREEN)
                if not compact:
                    line(5, 23, 14)

            def table(y, step, compact=False):
                text('Sprechzeiten' if not compact else 'Sprechzeiten · Uhr', 5, y, 12 if not compact else 8.5, 'Fraunces550')
                text('vormittags', 33, y, 6.2)
                text('nachmittags', 58, y, 6.2)
                for index, (day, morning, afternoon) in enumerate(rows):
                    baseline = y + (4 if compact else 6) + index*step
                    text(day, 5, baseline, 8.2 if not compact else 7.5)
                    text(morning, 33, baseline, 8.2 if not compact else 7.5)
                    text(afternoon, 58, baseline, 8.2 if not compact else 7.5)
                    if index < 4:
                        line(5, baseline+1.6, 80, '#c9d8d3', .13)

            if variant in ['G', 'H', 'I', 'J']:
                dark = variant in ['I', 'J']
                rect(0, 0, 85, 55, GREEN if dark else CREAM)
                if dark:
                    rect(4, 4.5, 18.6, 15, CREAM)
                c.drawImage(logo_reader,
                            5*mm, (HEIGHT-6-12)*mm, 16.6*mm, 12*mm, mask='auto')
                text('MVZ Gomaringen', 25, 11, 15.5 if dark else 14, 'Fraunces550', CREAM if dark else GREEN)
                text('Praxis Dr. Bernd Schilling', 25, 18, 13.2 if dark else 12, fill=CREAM if dark else GREEN)
                line(5, 24, 14)
                text('07072 / 7031', 5, 34, 26.5 if dark else 24, 'Figtree600', CREAM if dark else GREEN)
                text(domain, 5, 42, 15.5 if dark else 14, 'Figtree600', CREAM if dark else GREEN)
                landscape()
                c.showPage()
                begin_page()
                rect(0, 0, 85, 55, SAGE if variant == 'J' else CREAM)
                text('Sprechzeiten', 5, 9, 14, 'Fraunces550')
                line(49, 8, 80)
                if variant == 'G':
                    assert len({morning for _, morning, _ in rows}) == 1
                    text(f'{rows[0][0][:2]}–{rows[-1][0][:2]}', 5, 21, 16, 'Figtree600')
                    text(rows[0][1].replace(':00', '').replace(' ', '') + ' Uhr',
                         32, 21, 22, 'Figtree600')
                    line(5, 26, 80, '#c9d8d3', .2)
                    text('Zusätzlich nachmittags', 5, 32, 14, 'Figtree600')
                    groups = {}
                    for day, _, afternoon in rows:
                        if afternoon != '–':
                            groups.setdefault(afternoon, []).append(day[:2])
                    assert len(groups) <= 2
                    for index, (afternoon, days) in enumerate(groups.items()):
                        text(' + '.join(days), 5, 41+index*9, 14, 'Figtree600')
                        text(afternoon.replace(':00', '').replace(' ', '') + ' Uhr',
                             41, 41+index*9, 18, 'Figtree600')
                else:
                    for index, (day, morning, afternoon) in enumerate(rows):
                        baseline = 18 + index*7.6
                        if index % 2 == 0:
                            rect(0, baseline-5.5, 85, 7.6, '#e7efe9' if variant == 'J' else '#e4ede7')
                        text(day[:2], 5, baseline, 14, 'Figtree600')
                        text(morning.replace(':00', '').replace(' ', ''),
                             23, baseline, 16, 'Figtree600')
                        text(afternoon.replace(':00', '').replace(' ', ''),
                             54, baseline, 16, 'Figtree600')
                c.showPage()
            elif variant in ['A', 'B', 'D', 'E', 'F']:
                dark = variant == 'B'
                rect(0, 0, 85, 55, GREEN if dark else CREAM)
                brand(dark)
                text('Telefon', 5, 30, 8, fill=CREAM if dark else GREEN)
                text('07072 / 7031', 5, 39.5, 23, 'Figtree600', CREAM if dark else GREEN)
                landscape()
                c.showPage()
                rect(0, 0, 85, 55, SAGE if dark else CREAM)
                if variant in ['D', 'F']:
                    text('Sprechzeiten', 5, 9, 14, 'Fraunces550')
                    line(49, 8, 80)
                    for index, (day, morning, afternoon) in enumerate(rows):
                        baseline = 18 + index*7.7
                        if variant == 'F' and index % 2 == 0:
                            rect(0, baseline-5.5, 85, 7.7, '#e4ede7')
                        text(day[:2] if variant == 'D' else day, 5, baseline,
                             12 if variant == 'D' else 10.5, 'Figtree600')
                        for value, x in [(morning, 19 if variant == 'D' else 38),
                                         (afternoon, 51 if variant == 'D' else 60)]:
                            display = value if variant == 'D' else value.replace(':00', '').replace(' ', '')
                            text(display, x, baseline, 12 if variant == 'D' else 14, 'Figtree600')
                        if variant == 'D' and index < 4:
                            line(5, baseline+2.8, 80, '#c9d8d3', .15)
                elif variant == 'E':
                    # Group only truly identical sessions; fail rather than misstate changed hours.
                    assert len({morning for _, morning, _ in rows}) == 1
                    text('Sprechzeiten', 5, 9, 14, 'Fraunces550')
                    line(49, 8, 80)
                    text(f'{rows[0][0][:2]}–{rows[-1][0][:2]}', 5, 22, 14, 'Figtree600')
                    text(rows[0][1].replace(':00', '').replace(' ', '') + ' Uhr',
                         30, 22, 22, 'Figtree600')
                    line(5, 27, 80, '#c9d8d3', .2)
                    text('Zusätzlich nachmittags', 5, 33, 10, 'Figtree600')
                    groups = {}
                    for day, _, afternoon in rows:
                        if afternoon != '–':
                            groups.setdefault(afternoon, []).append(day[:2])
                    assert len(groups) <= 2
                    for index, (afternoon, days) in enumerate(groups.items()):
                        text(' + '.join(days), 5, 41+index*9, 13, 'Figtree600')
                        text(afternoon.replace(':00', '').replace(' ', '') + ' Uhr',
                             40, 41+index*9, 18, 'Figtree600')
                else:
                    table(10, 5.7)
                    if not dark:
                        landscape()
                    else:
                        line(5, 48, 14)
                c.showPage()
            else:
                rect(0, 0, 85, 55, CREAM)
                brand(compact=True)
                rect(0, 20.5, 85, 9.5, SAGE)
                text('Telefon', 5, 26.8, 8)
                text('07072 / 7031', 25, 27.2, 14, 'Figtree600')
                table(34, 2.9, compact=True)
                c.showPage()
            c.save()
            if args.icc:
                export_print(file, args.icc, args.out)
                continue
            doc = pymupdf.open(file)
            assert len(doc) == (1 if variant == 'C' else 2)
            assert '07072 / 7031' in doc[0].get_text()
            if variant in ['G', 'H', 'I', 'J']:
                assert domain in doc[0].get_text()
            for day, morning, afternoon in rows:
                content = doc[-1].get_text()
                if variant in ['A', 'B', 'C', 'D']:
                    assert (day[:2] if variant == 'D' else day) in content
                    assert morning in content and afternoon in content
                else:
                    if variant in ['F', 'H', 'I', 'J']:
                        assert (day if variant == 'F' else day[:2]) in content
                    else:
                        assert f'{rows[0][0][:2]}–{rows[-1][0][:2]}' in content
                        if afternoon != '–':
                            assert ' + '.join(groups[afternoon]) in content
                    assert morning.replace(':00', '').replace(' ', '') in content
                    assert afternoon.replace(':00', '').replace(' ', '') in content
            panels = []
            for index, page in enumerate(doc):
                pix = page.get_pixmap(dpi=300, alpha=False)
                image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
                panels.append(image)
                image.save(args.out / f'Visitenkarte-{variant}-{index+1}.png')
            w, h = panels[0].size
            board = Image.new('RGB', (2*w+120, h+145), '#e8ede9')
            draw = ImageDraw.Draw(board)
            label_font = ImageFont.truetype(str(fonts['Figtree600']), 27)
            for index, image in enumerate(panels):
                x = 40 + index*(w+40) if len(panels) == 2 else (board.width-w)//2
                draw.text((x, 26), f'{variant} · ' + ('Vorderseite' if index == 0 else 'Rückseite'), font=label_font, fill=GREEN)
                board.paste(image, (x, 80))
            board.save(args.out / f'Visitenkarte-{variant}-Vorschau.png')
            print(f'{variant}: {len(doc)} Seite(n), 85 × 55 mm; Telefonnummer und alle Sprechzeiten geprüft')


def export_print(artwork, profile, out):
    """Export and validate the final print PDF, then render trimmed previews."""
    output = out / f'{PRINT_PREFIX}-Druck.pdf'
    # Artwork is already opaque CMYK with embedded fonts. Add the output condition
    # without reinterpreting glyph encodings, paths or page content streams.
    with pymupdf.open(artwork) as prepared:
        icc = prepared.get_new_xref()
        prepared.update_object(icc, '<< /N 4 >>')
        prepared.update_stream(icc, profile.read_bytes())
        intent = prepared.get_new_xref()
        prepared.update_object(intent, f'''<< /Type /OutputIntent /S /GTS_PDFX
            /OutputCondition (ISO Coated v2 300% ECI)
            /OutputConditionIdentifier (FOGRA39) /RegistryName (http://www.color.org)
            /Info (ISO Coated v2 300% ECI) /DestOutputProfile {icc} 0 R >>''')
        prepared.xref_set_key(prepared.pdf_catalog(), 'OutputIntents', f'[{intent} 0 R]')
        info = int(prepared.xref_get_key(-1, 'Info')[1].split()[0])
        prepared.xref_set_key(info, 'GTS_PDFXVersion', '(PDF/X-3:2002)')
        prepared.xref_set_key(info, 'Trapped', '/False')
        prepared.save(output, garbage=4, deflate=True)
    doc = pymupdf.open(output)
    assert len(doc) == 2 and not doc.is_encrypted
    assert doc.metadata['format'] == 'PDF 1.3'
    info = int(doc.xref_get_key(-1, 'Info')[1].split()[0])
    assert doc.xref_get_key(info, 'GTS_PDFXVersion')[1] == 'PDF/X-3:2002'
    assert doc.xref_get_key(doc.pdf_catalog(), 'OutputIntents')[0] == 'array'
    profiles = [doc.xref_stream(x) for x in range(1, doc.xref_length())
                if doc.xref_is_stream(x) and '/N 4' in doc.xref_object(x)]
    assert profile.read_bytes() in profiles
    for x in range(1, doc.xref_length()):
        obj = doc.xref_object(x)
        assert '/DeviceRGB' not in obj and '/SMask' not in obj
        assert not re.search(r'/(?:ca|CA)\s+(?!1(?:\s|/|$))\d', obj)
    source = pymupdf.open(artwork)
    for index, page in enumerate(doc):
        assert page.rotation == 0
        assert abs(page.rect.width/mm-87) < .01 and abs(page.rect.height/mm-57) < .01
        assert all(abs(a-b) < .02 for a, b in zip(page.trimbox, (mm, mm, 86*mm, 56*mm)))
        assert all(abs(a-b) < .02 for a, b in zip(page.bleedbox, page.rect))
        assert not list(page.annots() or []) and not page.get_links()
        assert not re.search(rb'\s(?:rg|RG)\s', page.read_contents())
        assert page.get_text().splitlines() == source[index].get_text().splitlines()
        fonts = page.get_fonts(full=True)
        assert fonts and all(doc.extract_font(font[0])[3] for font in fonts)
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    assert pymupdf.Rect(4*mm, 4*mm, 83*mm, 53*mm).contains(pymupdf.Rect(span['bbox']))
                    if index == 1:
                        assert span['size'] >= 13.99
                        if any(c.isdigit() for c in span['text']):
                            assert span['size'] >= 15.99
        page.get_pixmap(dpi=300, clip=page.trimbox).save(
            out / f'{PRINT_PREFIX}-{"Vorderseite" if index == 0 else "Rueckseite"}.png')
    assert '07072 / 7031' in doc[0].get_text() and 'mvz-gomaringen.de' in doc[0].get_text()
    assert doc[1].get_text().splitlines() == [
        'Sprechzeiten', 'Mo', '8–12', '16–18', 'Di', '8–12', '–',
        'Mi', '8–12', '16–18', 'Do', '8–12', '–', 'Fr', '8–12', '15–16']
    print('OK: 2 Seiten, 87 × 57 mm, Endformat 85 × 55 mm, 1 mm Beschnitt, 0° Drehung.')
    print('OK: Schriften und ECI-Profil eingebettet; kein RGB, keine Transparenzmasken oder Annotationen.')
    print('OK: Texte ≥3 mm innerhalb des Endformats; Tageskürzel 14 pt und Zeiten 16 pt erhalten.')
    print('OK: Telefonnummer, Webadresse und genaue Tageszuordnung in der finalen PDF geprüft.')
    print(output)


if __name__ == '__main__':
    main()
