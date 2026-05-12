import fitz
import os

def extract_images_from_pdf(uploaded_file):

    uploaded_file.seek(0)

    pdf_bytes = uploaded_file.read()

    pdf = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    image_paths = []

    for page_index in range(len(pdf)):

        page = pdf[page_index]

        images = page.get_images(full=True)

        for img_index, img in enumerate(images):

            xref = img[0]

            base_image = pdf.extract_image(xref)

            image_bytes = base_image["image"]

            image_ext = base_image["ext"]

            image_path = (
                f"temp/image_"
                f"{page_index+1}_"
                f"{img_index+1}."
                f"{image_ext}"
            )

            with open(image_path, "wb") as f:

                f.write(image_bytes)

            image_paths.append(image_path)

    pdf.close()

    return image_paths