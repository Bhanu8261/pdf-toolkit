from pdf2docx import Converter

def convert_pdf_to_word(uploaded_file, output_docx):

    temp_pdf = "temp/input.pdf"

    with open(temp_pdf, "wb") as f:
        f.write(uploaded_file.seek(0))

    cv = Converter(temp_pdf)

    cv.convert(output_docx)

    cv.close()