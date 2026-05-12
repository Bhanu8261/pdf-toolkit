from pypdf import PdfReader, PdfWriter

def protect_pdf(uploaded_file, password):

    reader = PdfReader(uploaded_file)

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    output_path = "temp/protected.pdf"

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path