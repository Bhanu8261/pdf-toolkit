import fitz
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\Bhanu\tesseract.exe"
)

def extract_text_from_pdf(uploaded_file):

    # ==========================================
    # RESET POINTER
    # ==========================================

    uploaded_file.seek(0)

    pdf_bytes = uploaded_file.read()

    # ==========================================
    # OPEN PDF
    # ==========================================

    doc = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    extracted_text = ""

    # ==========================================
    # OCR EACH PAGE
    # ==========================================

    for page in doc:

        pix = page.get_pixmap()

        img_bytes = pix.tobytes("png")

        image = Image.open(
            io.BytesIO(img_bytes)
        )

        text = pytesseract.image_to_string(
            image
        )

        extracted_text += text + "\n\n"

    doc.close()

    return extracted_text