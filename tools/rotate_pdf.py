from pypdf import PdfReader, PdfWriter

# ==========================================
# FULL PDF
# ==========================================

def rotate_full_pdf(uploaded_file, angle):

    uploaded_file.seek(0)

    reader = PdfReader(uploaded_file)

    writer = PdfWriter()

    for page in reader.pages:

        page.rotate(angle)

        writer.add_page(page)

    output_path = "temp/rotated_full.pdf"

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path

# ==========================================
# SINGLE PAGE
# ==========================================

def rotate_single_page(uploaded_file, page_number, angle):

    uploaded_file.seek(0)

    reader = PdfReader(uploaded_file)

    writer = PdfWriter()

    for i, page in enumerate(reader.pages):

        if i == page_number - 1:
            page.rotate(angle)

        writer.add_page(page)

    output_path = "temp/rotated_single.pdf"

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path

# ==========================================
# PAGE RANGE
# ==========================================

def rotate_page_range(
    uploaded_file,
    start_page,
    end_page,
    angle
):

    uploaded_file.seek(0)

    reader = PdfReader(uploaded_file)

    writer = PdfWriter()

    for i, page in enumerate(reader.pages):

        if start_page - 1 <= i <= end_page - 1:
            page.rotate(angle)

        writer.add_page(page)

    output_path = "temp/rotated_range.pdf"

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path