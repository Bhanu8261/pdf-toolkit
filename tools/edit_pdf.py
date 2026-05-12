import fitz

def add_text_to_pdf(
    uploaded_file,
    text,
    page_number,
    x,
    y
):

    uploaded_file.seek(0)

    doc = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    page = doc[page_number - 1]

    page.insert_text(
        (x, y),
        text,
        fontsize=20,
        color=(0,0,0)
    )

    output_path = "temp/edited.pdf"

    doc.save(output_path)

    doc.close()

    return output_path