import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.platypus.flowables import PageBreak
from bs4 import BeautifulSoup

def create_pdf_report(markdown_text, pdf_path):
    """Create a PDF report from Markdown text."""
    # Convert Markdown to HTML
    html = markdown2.markdown(markdown_text)

    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Create a PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Define custom styles
    code_style = ParagraphStyle(
        name='Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=10,
        leading=12,
        backColor='#f5f5f5',
        borderPadding=(5, 5, 5, 5),
        borderColor='#dedede',
        borderWidth=1,
        borderRadius=2
    )

    for element in soup.children:
        if element.name == 'h1':
            style = styles['Heading1']
        elif element.name == 'h2':
            style = styles['Heading2']
        elif element.name == 'p':
            style = styles['BodyText']
        elif element.name == 'code':
            story.append(Paragraph(element.get_text(), code_style))
            continue
        elif element.name == 'pre':
            story.append(Paragraph(element.get_text(), code_style))
            continue
        else:
            style = styles['Normal']

        story.append(Paragraph(element.get_text(), style))

        if element.name in ['h1', 'h2', 'p']:
            story.append(Spacer(1, 0.2 * inch))

        # Add page break after each <h1> tag for better readability
        if element.name == 'h1':
            story.append(PageBreak())

    # Build the PDF
    doc.build(story)

    print(f"PDF report created at: {pdf_path}")
