import fitz

def compress_pdf(input_path, output_path):
    
    doc = fitz.open(input_path)

    doc.save(
        output_path,
        garbage=4,
        deflate=True
    )

    doc.close()