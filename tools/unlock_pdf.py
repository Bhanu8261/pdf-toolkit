from pypdf import PdfReader, PdfWriter

def unlock_pdf(uploaded_file, password):

    reader = PdfReader(uploaded_file)

    if reader.is_encrypted:
        reader.decrypt(password)

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    output_path = "temp/unlocked.pdf"

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path