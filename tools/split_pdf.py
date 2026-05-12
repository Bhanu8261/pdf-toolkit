from pypdf import PdfReader, PdfWriter
import os

# ==========================================
# Split All Pages
# ==========================================

def split_all_pages(uploaded_file):

    reader = PdfReader(uploaded_file)

    output_files = []

    for i, page in enumerate(reader.pages):

        writer = PdfWriter()

        writer.add_page(page)

        output_path = f"temp/page_{i+1}.pdf"

        with open(output_path, "wb") as f:
            writer.write(f)

        output_files.append(output_path)

    return output_files

# ==========================================
# Split Page Range
# Example: 1-5
# ==========================================

def split_page_range(uploaded_file, start_page, end_page):

    reader = PdfReader(uploaded_file)

    writer = PdfWriter()

    for page_num in range(start_page - 1, end_page):

        writer.add_page(reader.pages[page_num])

    output_path = f"temp/pages_{start_page}_to_{end_page}.pdf"

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path

# ==========================================
# Split Custom Pages
# Example: 1,3,5
# ==========================================

def split_custom_pages(uploaded_file, page_numbers):

    reader = PdfReader(uploaded_file)

    writer = PdfWriter()

    for page_num in page_numbers:

        writer.add_page(reader.pages[page_num - 1])

    output_path = "temp/custom_pages.pdf"

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path