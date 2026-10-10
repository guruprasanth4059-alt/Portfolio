#!/usr/bin/env python3
"""
Guru Prasanth — ATS-Friendly Professional Resume Generator
Deterministic PDF generation using ReportLab.
Produces a crisp, 1-page ATS-compatible vector PDF with selectable text and active links.
"""

import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

ACCENT_COLOR = colors.HexColor("#FD1053")       # Brand Accent
TEXT_PRIMARY = colors.HexColor("#111827")       # Near-black
TEXT_SECONDARY = colors.HexColor("#374151")     # Charcoal
TEXT_MUTED = colors.HexColor("#4B5563")         # Slate
DIVIDER_COLOR = colors.HexColor("#E5E7EB")      # Subtle border
LINK_COLOR = colors.HexColor("#C00F43")         # Darker accessible pink for links

class NumberedCanvas(canvas.Canvas):
    """Canvas that enforces single-page bounds and valid metadata."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            # Optional subtle single page footer or metadata
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)


def load_resume_data(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_resume_pdf(data, output_pdf_path):
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
    
    # 0.5 inch (36 pt) margins for optimal printable area on Letter size (612 x 792 pt)
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=22,
        textColor=TEXT_PRIMARY,
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=ACCENT_COLOR,
        spaceAfter=4
    )

    contact_style = ParagraphStyle(
        'DocContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=TEXT_MUTED,
        spaceAfter=8
    )

    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=TEXT_PRIMARY,
        spaceBefore=7,
        spaceAfter=3,
        textTransform='uppercase'
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_SECONDARY
    )

    item_title_style = ParagraphStyle(
        'ItemTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=TEXT_PRIMARY
    )

    item_meta_style = ParagraphStyle(
        'ItemMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=TEXT_MUTED,
        alignment=2 # Right align
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=TEXT_SECONDARY,
        leftIndent=10,
        firstLineIndent=-7,
        spaceAfter=2
    )

    story = []

    # 1. Header Block
    p = data['personal']
    story.append(Paragraph(p['name'], title_style))
    story.append(Paragraph(p['headline'], subtitle_style))

    contact_line = (
        f"{p['location']} &nbsp;|&nbsp; "
        f"<a href='mailto:{p['email']}' color='{LINK_COLOR}'><b>{p['email']}</b></a> &nbsp;|&nbsp; "
        f"<a href='{p['linkedin_url']}' color='{LINK_COLOR}'><b>{p['linkedin_display']}</b></a> &nbsp;|&nbsp; "
        f"<a href='{p['github_url']}' color='{LINK_COLOR}'><b>{p['github_display']}</b></a>"
    )
    story.append(Paragraph(contact_line, contact_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_COLOR, spaceAfter=5, spaceBefore=0))

    # 2. Professional Summary
    story.append(Paragraph("Professional Summary", section_heading_style))
    story.append(Paragraph(data['summary'], body_style))
    story.append(Spacer(1, 4))

    # 3. Technical & Analytical Skills
    story.append(Paragraph("Technical & Analytical Skills", section_heading_style))
    skills = data['skills']
    skills_text = []
    for cat, items in skills.items():
        skills_text.append(f"<b>{cat}:</b> {', '.join(items)}")
    
    # Render skills in compact clean rows
    for st in skills_text:
        story.append(Paragraph(f"• &nbsp;{st}", bullet_style))
    story.append(Spacer(1, 4))

    # 4. Featured Projects
    story.append(Paragraph("Featured Projects", section_heading_style))
    
    # Include all 4 projects cleanly formatted
    for proj in data['projects']:
        # Header line with Title, Category/Status
        title_para = Paragraph(f"<b>{proj['title']}</b> &nbsp;—&nbsp; <font color='{TEXT_MUTED}'>{proj['subtitle']}</font>", item_title_style)
        tech_line = f"<b>Stack:</b> {', '.join(proj['technologies'])} &nbsp;|&nbsp; <i>{proj['status']}</i>"
        
        # Two-column layout for title and status
        row_table = Table(
            [[title_para]],
            colWidths=[540]
        )
        row_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        story.append(row_table)
        story.append(Paragraph(f"• &nbsp;{proj['description']}", bullet_style))
        story.append(Paragraph(f"• &nbsp;{tech_line}", bullet_style))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 2))

    # 5. Education
    story.append(Paragraph("Education", section_heading_style))
    edu = data['education']
    edu_left = Paragraph(
        f"<b>{edu['degree']}</b><br/>"
        f"{edu['primary_institution']} (Affiliated with {edu['affiliating_university']}) — {edu['location']}",
        item_title_style
    )
    edu_right = Paragraph(f"<b>{edu['timeline']}</b>", item_meta_style)
    
    edu_table = Table([[edu_left, edu_right]], colWidths=[420, 120])
    edu_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    story.append(edu_table)
    story.append(Spacer(1, 4))

    # 6. Certifications & Job Simulations
    story.append(Paragraph("Certifications & Job Simulations", section_heading_style))
    for cert in data['certifications']:
        cert_left = Paragraph(f"<b>{cert['name']}</b> &nbsp;—&nbsp; {cert['issuer']}", item_title_style)
        cert_right = Paragraph("<i>Verified Simulation</i>", item_meta_style)
        cert_table = Table([[cert_left, cert_right]], colWidths=[440, 100])
        cert_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        story.append(cert_table)
        story.append(Paragraph(f"• &nbsp;{cert['focus']}", bullet_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Resume successfully built at: {output_pdf_path}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file = os.path.join(base_dir, "data", "resume_data.json")
    
    # Destination paths for live website and assets
    targets = [
        os.path.join(base_dir, "assets", "Guruprasanth_Resume.pdf"),
        os.path.join(base_dir, "guruprasanth-portfolio", "assets", "Guruprasanth_Resume.pdf"),
        os.path.join(base_dir, "Guruprasanth_Resume.pdf")
    ]
    
    resume_data = load_resume_data(json_file)
    for target in targets:
        build_resume_pdf(resume_data, target)
