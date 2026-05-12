from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter
import io

def create_watermark(watermark_text):

    packet = io.BytesIO()

    can = canvas.Canvas(packet, pagesize=letter)

    # Transparency
    can.setFillColor(
        Color(
            0.6,
            0.6,
            0.6,
            alpha=0.2
        )
    )

    can.setFont("Helvetica-Bold", 40)

    width, height = letter

    # Rotate entire canvas
    can.saveState()

    can.translate(width / 2, height / 2)

    can.rotate(45)

    # Multiple watermark texts
    positions = [

        (-300, -300),
        (-100, -100),
        (100, 100),
        (250, 250),
        (-250, 250)

    ]

    for x, y in positions:

        can.drawString(
            x,
            y,
            watermark_text
        )

    can.restoreState()

    can.save()

    packet.seek(0)

    return PdfReader(packet)

# ==========================================
# ADD WATERMARK
# ==========================================

def add_watermark(uploaded_file, watermark_text):

    uploaded_file.seek(0)

    reader = PdfReader(uploaded_file)

    writer = PdfWriter()

    watermark_pdf = create_watermark(
        watermark_text
    )

    watermark_page = watermark_pdf.pages[0]

    for page in reader.pages:

        page.merge_page(watermark_page)

        writer.add_page(page)

    output_path = "temp/watermarked.pdf"

    with open(output_path, "wb") as f:

        writer.write(f)

    return output_path