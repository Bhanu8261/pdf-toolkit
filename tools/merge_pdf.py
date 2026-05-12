from pypdf import PdfReader, PdfWriter
import streamlit as st

def merge_pdfs(pdf_files, output_path):

    writer = PdfWriter()

    for pdf in pdf_files:

        pdf.seek(0)

        reader = PdfReader(pdf)

        # ==========================================
        # HANDLE ENCRYPTED PDF
        # ==========================================

        if reader.is_encrypted:

            password_key = f"merge_password_{pdf.name}"

            password = st.session_state.get(
                password_key,
                ""
            )

            if password:

                try:

                    reader.decrypt(password)

                except:

                    st.error(
                        f"Wrong password for {pdf.name}"
                    )

                    return False

            else:

                st.error(
                    f"No password given for {pdf.name}"
                )

                return False

        # ==========================================
        # ADD PAGES
        # ==========================================

        for page in reader.pages:

            writer.add_page(page)

    # ==========================================
    # SAVE OUTPUT
    # ==========================================

    with open(output_path, "wb") as f:

        writer.write(f)

    return True