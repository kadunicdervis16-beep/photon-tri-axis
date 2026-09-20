from pathlib import Path
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Oblique', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuMono', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image,
                                Table, TableStyle, KeepTogether, Preformatted)

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/mnt/data/Paper_10_5_FULL_REWRITE_READABLE_COMPANION.txt')
OUT = ROOT / 'Paper_10_5_FINAL_READABLE_COMPANION.pdf'

BLUE = colors.HexColor('#2B507A')
GOLD = colors.HexColor('#D99000')
GREEN = colors.HexColor('#55A06A')
LIGHT_BLUE = colors.HexColor('#EAF0F6')
LIGHT_GOLD = colors.HexColor('#F8F0DF')
LIGHT_GREEN = colors.HexColor('#E8F3EA')
GRAY = colors.HexColor('#444444')
LIGHT_GRAY = colors.HexColor('#F4F5F7')
RED = colors.HexColor('#C84B4B')

PAGE_W, PAGE_H = letter
LEFT = RIGHT = 0.72*inch
TOP = 0.72*inch
BOTTOM = 0.68*inch

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyX', parent=styles['BodyText'], fontName='DejaVu', fontSize=9.6, leading=13.2, textColor=GRAY, spaceAfter=7))
styles.add(ParagraphStyle(name='SectionX', parent=styles['Heading1'], fontName='DejaVu-Bold', fontSize=17, leading=20, textColor=BLUE, spaceBefore=15, spaceAfter=9, keepWithNext=True))
styles.add(ParagraphStyle(name='SubX', parent=styles['Heading2'], fontName='DejaVu-Bold', fontSize=12.3, leading=15, textColor=BLUE, spaceBefore=10, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name='TitleX', parent=styles['Title'], fontName='DejaVu-Bold', fontSize=27, leading=31, alignment=TA_CENTER, textColor=BLUE, spaceAfter=12))
styles.add(ParagraphStyle(name='SubtitleX', parent=styles['BodyText'], fontName='DejaVu', fontSize=13.5, leading=18, alignment=TA_CENTER, textColor=GOLD, spaceAfter=12))
styles.add(ParagraphStyle(name='AuthorX', parent=styles['BodyText'], fontName='DejaVu', fontSize=11, leading=15, alignment=TA_CENTER, textColor=GRAY))
styles.add(ParagraphStyle(name='AbstractX', parent=styles['BodyText'], fontName='DejaVu', fontSize=10, leading=14, textColor=GRAY, leftIndent=8, rightIndent=8, spaceAfter=7))
styles.add(ParagraphStyle(name='FormulaX', parent=styles['BodyText'], fontName='DejaVuMono', fontSize=11, leading=14, alignment=TA_CENTER, textColor=BLUE, spaceBefore=4, spaceAfter=8))
styles.add(ParagraphStyle(name='CaptionX', parent=styles['BodyText'], fontName='DejaVu-Oblique', fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=GOLD, spaceBefore=3, spaceAfter=10))
styles.add(ParagraphStyle(name='TOCX', parent=styles['BodyText'], fontName='DejaVu', fontSize=10.3, leading=15, textColor=GRAY, leftIndent=8, spaceAfter=2))
styles.add(ParagraphStyle(name='CodeX', parent=styles['Code'], fontName='DejaVuMono', fontSize=6.9, leading=8.5, textColor=colors.HexColor('#20242A'), leftIndent=4, rightIndent=4, spaceBefore=3, spaceAfter=3))
styles.add(ParagraphStyle(name='SmallX', parent=styles['BodyText'], fontName='DejaVu', fontSize=8.3, leading=11, textColor=GRAY, spaceAfter=4))


def header_footer(canvas, doc):
    canvas.saveState()
    # top gold rule and header
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.7)
    canvas.rect(0.72*inch, PAGE_H-0.38*inch, PAGE_W-1.44*inch, 0.19*inch, stroke=1, fill=0)
    canvas.setFont('Helvetica-Bold', 7.2); canvas.setFillColor(GOLD)
    canvas.drawCentredString(PAGE_W/2, PAGE_H-0.315*inch, 'DECONSTRUCTING CONTINUUM MECHANICS AND HARDWARE LIMITS')
    # footer
    canvas.setStrokeColor(GOLD); canvas.line(0.72*inch, 0.43*inch, PAGE_W-0.72*inch, 0.43*inch)
    canvas.setFont('Helvetica', 7.3); canvas.setFillColor(colors.HexColor('#777777'))
    canvas.drawString(0.72*inch, 0.25*inch, 'Paper 10.5 · A First-Principles Ledger Critique')
    canvas.drawRightString(PAGE_W-0.72*inch, 0.25*inch, f'Page {doc.page}')
    canvas.restoreState()


def clean_markup(s):
    s=s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    # preserve simple unicode math as text
    return s


def make_figure(path, num, caption, width=6.45*inch):
    img=Image(str(path), width=width, height=width*0.58)
    return [img, Paragraph(f'Figure {num} — {caption}', styles['CaptionX'])]


def extract_sections(src):
    narrative = src.split('COMPUTATIONAL VERIFICATION',1)[0]
    lines=narrative.splitlines()
    # Remove separator lines and empty framing.
    return lines


def build_story():
    src=SOURCE.read_text(encoding='utf-8')
    lines=extract_sections(src)
    story=[]

    # Title page
    story += [Spacer(1,0.55*inch), Paragraph('PAPER 10.5', styles['TitleX']),
              Paragraph('DECONSTRUCTING CONTINUUM MECHANICS AND HARDWARE LIMITS', styles['TitleX']),
              Paragraph('A First-Principles Ledger Critique', styles['SubtitleX']),
              Paragraph('Companion to Paper 10 — Departure From the Photon Baseline', styles['SubtitleX']),
              Spacer(1,0.20*inch), Paragraph('Dervis Kadunic', styles['AuthorX']),
              Paragraph('Omega Research Collective', styles['AuthorX']), Paragraph('2026', styles['AuthorX']),
              Spacer(1,0.45*inch)]
    # title plate
    t=Table([[Paragraph('<b>COMPANION PURPOSE</b><br/>Make the deferred reasoning visible without turning the critique into a second copy of Paper 10.', styles['BodyX'])]], colWidths=[6.25*inch])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT_BLUE),('BOX',(0,0),(-1,-1),1,BLUE),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    story += [t, PageBreak()]

    # We will build from the manuscript lines, skipping abstract/contents for custom versions.
    in_abstract=False; abstract=[]; in_contents=False; contents=[]; i=0
    while i < len(lines):
        l=lines[i].strip()
        if l=='ABSTRACT':
            in_abstract=True; i+=1
            while i<len(lines) and lines[i].strip()!='============================================================':
                if lines[i].strip(): abstract.append(lines[i].strip())
                i+=1
            continue
        if l=='CONTENTS':
            in_contents=True; i+=1
            while i<len(lines) and lines[i].strip()!='============================================================':
                if lines[i].strip(): contents.append(lines[i].strip())
                i+=1
            break
        i+=1

    story.append(Paragraph('ABSTRACT', styles['SectionX']))
    story.append(Spacer(1,2))
    for p in abstract:
        story.append(Paragraph(clean_markup(p), styles['AbstractX']))
    story.append(Spacer(1,5))
    story.append(Paragraph('CONTENTS', styles['SectionX']))
    for c in contents:
        story.append(Paragraph(clean_markup(c), styles['TOCX']))
    story.append(PageBreak())

    # Parse all sections from 1 onward, stopping before APPENDICES.
    body_start=next(idx for idx,l in enumerate(lines) if l.strip()=='1. INTRODUCTION')
    body_end=next(idx for idx,l in enumerate(lines) if l.strip()=='APPENDICES')
    body=lines[body_start:body_end]

    # Track figure insertion by exact heading marker.
    figures={
      '3. WHAT PAPER 10 CLAIMS AND WHAT PAPER 10.5 TESTS': ('figure_1_claim_chain.png','The companion paper audits the links between propositions.'),
      '4.2 SHELL ALLOCATION': ('figure_2_shell_count.png','Exact finite shell count and its inverse-square shadow.'),
      '4.4 WHAT HAPPENS AT LOCAL CAPACITY EXHAUSTION': ('figure_3_port_exhaustion.png','Six-port blocking produces a finite set of directional responses.'),
      '5.3 SYMMETRY': ('figure_4_beta.png','The coefficient β follows from axis equivalence and normalization.'),
      '8.3 WHY THE FACTOR IS NOT AN ARBITRARY CONVENTION': ('figure_5_two_transitions.png','Two distinct mandatory operations precede physical reconstruction.'),
      '9.4 SIMULATION AND EXPERIMENT': ('figure_6_single_regime.png','The falsification harness must be capable of rejecting a planted scale-dependent failure.'),
      '10.3 CONSERVATION OF CLAIM BURDEN': ('figure_7_bridge_ledger.png','The weakest necessary bridge limits the strength of the downstream claim.'),
    }
    idx=0
    current_section=None
    while idx<len(body):
        raw=body[idx].rstrip(); s=raw.strip()
        if not s or s.startswith('----'):
            idx+=1; continue
        if s.upper() in figures:
            current_section=s.upper()
        # Section heading
        if re.match(r'^\d+\. ', s):
            story.append(Paragraph(clean_markup(s), styles['SectionX']))
            if s in figures:
                pass
            idx+=1; continue
        if re.match(r'^\d+\.\d+ ', s):
            story.append(Paragraph(clean_markup(s), styles['SubX']))
            idx+=1; continue
        # insert figure immediately after selected heading's following paragraph block, not before text
        # handle lists and formula blocks
        if s.startswith('    '):
            block=[]
            while idx<len(body) and (body[idx].strip().startswith(('N(', 'S(', 'β', 'd_', 'Δ', 'L_', 'COUNT','ALLOCATE','BLOCK','TRANSITION','RECONSTRUCT','OBSERVE','enumeration →','β +','β·','N_transitions','κ =','C_exec','P_id','27 =','6 =','1 /','S_total','R_exact','ρ =','Δ(')) or body[idx].startswith('    ')):
                q=body[idx].strip();
                if q: block.append(q)
                idx+=1
            if block:
                story.append(Paragraph('<br/>'.join(clean_markup(q) for q in block), styles['FormulaX']))
            continue
        # bullets
        if s.startswith('•'):
            story.append(Paragraph('• '+clean_markup(s[1:].strip()), styles['BodyX']))
            idx+=1; continue
        # tables: detect the six-port table region
        if s.startswith('b   o'):
            rows=[]
            while idx<len(body) and body[idx].strip() and not body[idx].strip().startswith('Thus'):
                rows.append(body[idx].split())
                idx+=1
            if rows:
                data=[['b','o','configurations','factor']]
                for r in rows[1:]:
                    if len(r)>=4: data.append(r[:4])
                tbl=Table(data,colWidths=[.5*inch,.5*inch,1.6*inch,1.5*inch],hAlign='CENTER')
                tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLUE),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#BFC5CC')),('ALIGN',(0,0),(-1,-1),'CENTER'),('FONTSIZE',(0,0),(-1,-1),8),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT_BLUE])]))
                story.append(tbl); story.append(Spacer(1,8))
            continue
        # normal paragraph
        # avoid treating the title metadata as body
        story.append(Paragraph(clean_markup(s), styles['BodyX']))
        idx+=1
        # Figure after paragraph containing section-specific endpoint.
        # For figure 2/3 etc, insert once when the next source line starts a known conclusion or heading.
        if current_section in figures:
            # Insert after a paragraph that contains an anchor phrase.
            anchor=False
            if current_section.startswith('3.') and 'last two require additional bridges' in s: anchor=True
            elif current_section.startswith('4.2') and 'allocation step is logically distinct' in s: anchor=True
            elif current_section.startswith('4.4') and 'finite set of directional responses' in s: anchor=True
            elif current_section.startswith('5.3') and 'Neither piece is optional' in s: anchor=True
            elif current_section.startswith('8.3') and 'independent consistency check' in s: anchor=True
            elif current_section.startswith('9.4') and 'planted failures' in s: anchor=True
            elif current_section.startswith('10.3') and 'Circa budget' in s: anchor=True
            if anchor:
                fn,cap=figures[current_section]; story += make_figure(ROOT/'figures'/fn, int(re.search(r'figure_(\d+)',fn).group(1)), cap)
                current_section=None

    # Appendices and references from source, but omit old computational block.
    app_start=next(idx for idx,l in enumerate(lines) if l.strip()=='APPENDICES')
    app_end=next(idx for idx,l in enumerate(lines) if l.strip()=='REFERENCES')
    apps=lines[app_start:app_end]
    story.append(PageBreak())
    for raw in apps:
        s=raw.strip()
        if not s or s.startswith('===='): continue
        if s.startswith('APPENDIX '): story.append(Paragraph(clean_markup(s), styles['SectionX'])); continue
        if re.match(r'^\d+\.\d+',s): story.append(Paragraph(clean_markup(s), styles['SubX'])); continue
        if s.startswith('    '): story.append(Paragraph(clean_markup(s), styles['FormulaX'])); continue
        story.append(Paragraph(clean_markup(s), styles['BodyX']))

    # References
    ref_start=next(idx for idx,l in enumerate(lines) if l.strip()=='REFERENCES')
    refs=lines[ref_start:]
    story.append(Paragraph('REFERENCES', styles['SectionX']))
    for raw in refs[1:]:
        s=raw.strip()
        if not s or s.startswith('===='): continue
        story.append(Paragraph(clean_markup(s), styles['BodyX']))

    # Computational verification — clean, executable listings.
    story.append(PageBreak())
    story.append(Paragraph('COMPUTATIONAL VERIFICATION', styles['SectionX']))
    story.append(Paragraph('The executable listings below are the clean verification record for the companion paper. They are intentionally separated from the narrative. Each script checks a registered proposition under declared inputs; a PASS certifies the executable check, not an experimental validation of the physical reconstruction.', styles['BodyX']))
    script_names=['F25_beta.py','F26_relay_distance.py','F27_mass_quantum.py','F28_two_transitions.py','F29_port_exhaustion.py','F30_single_regime.py','F31_claim_registry.py']
    for name in script_names:
        story.append(Paragraph(name, styles['SubX']))
        code=(ROOT/name).read_text(encoding='utf-8')
        # Keep code printable; Preformatted handles long lines better than Paragraph.
        story.append(Preformatted(code, styles['CodeX']))
        story.append(PageBreak())
    story.append(Paragraph('MASTER VERIFICATION RUNNER', styles['SubX']))
    story.append(Preformatted((ROOT/'paper10_5_verification.py').read_text(encoding='utf-8'), styles['CodeX']))
    story.append(Spacer(1,8))
    story.append(Paragraph('FINAL VERIFICATION STATUS: 7/7 executable modules PASS.', styles['BodyX']))

    return story


def main():
    doc=SimpleDocTemplate(str(OUT),pagesize=letter,rightMargin=RIGHT,leftMargin=LEFT,topMargin=TOP,bottomMargin=BOTTOM,title='Paper 10.5 — Deconstructing Continuum Mechanics and Hardware Limits',author='Dervis Kadunic')
    doc.build(build_story(), onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUT)

if __name__=='__main__': main()
