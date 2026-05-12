import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_pdf_viewer import pdf_viewer
from pypdf import PdfReader
import zipfile
import os
# ==========================================
# IMPORT TOOLS
# ==========================================

from tools.merge_pdf import merge_pdfs

from tools.split_pdf import (
    split_all_pages,
    split_page_range,
    split_custom_pages
)

from tools.pdf_to_word import convert_pdf_to_word
from tools.word_to_pdf import convert_word_to_pdf
from tools.compress_pdf import compress_pdf
from tools.rotate_pdf import (
    rotate_full_pdf,
    rotate_single_page,
    rotate_page_range
)
from tools.watermark_pdf import add_watermark
# from tools.ocr_pdf import extract_text_from_pdf
from tools.extract_images import extract_images_from_pdf
from tools.protect_pdf import protect_pdf
from tools.unlock_pdf import unlock_pdf
from tools.edit_pdf import add_text_to_pdf

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="PDF Toolkit",
    page_icon="📄",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 20px;
}

.tool-card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.stButton button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 50px;
    border: none;
    font-size: 18px;
    font-weight: bold;
}

.stButton button:hover {
    background-color: #1d4ed8;
    color: white;
}

[data-testid="stFileUploader"] {
    border: 2px dashed #2563eb;
    padding: 15px;
    border-radius: 10px;
    background-color: white;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# PDF PREVIEW FUNCTION
# ==========================================

def show_pdf_preview(uploaded_file):

    if uploaded_file is not None:

        # pdf_bytes = uploaded_file.read()
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()
        uploaded_file.seek(0)

        reader = PdfReader(uploaded_file)
        reader = PdfReader(uploaded_file)

        # ==========================================
        # HANDLE ENCRYPTED PDF
        # ==========================================

        if reader.is_encrypted:

            st.warning("🔒 This PDF is password protected.")

            password = st.text_input(
                "Enter PDF Password",
                type="password",
                key=f"password_{uploaded_file.name}"
            )

            if password:

                try:

                    reader.decrypt(password)

                except:

                    st.error("❌ Wrong Password")

                    return

            else:
                return

        # ==========================================
        # TOTAL PAGES
        # ==========================================

        

        total_pages = len(reader.pages)
        uploaded_file.seek(0)

        pdf_bytes = uploaded_file.read()

        uploaded_file.seek(0)    
        
        st.subheader("📄 PDF Preview")

        session_key = f"page_{uploaded_file.name}"

        if session_key not in st.session_state:
            st.session_state[session_key] = 1

        col1, col2, col3 = st.columns([1, 2, 1])

        # LEFT
        with col1:

            if st.button("⬅", key=f"left_{uploaded_file.name}"):

                if st.session_state[session_key] > 1:
                    st.session_state[session_key] -= 1

        # PAGE INPUT
        with col2:

            page_input = st.number_input(
                f"Page (1 - {total_pages})",
                min_value=1,
                max_value=total_pages,
                value=st.session_state[session_key],
                step=1,
                key=f"input_{uploaded_file.name}"
            )

            st.session_state[session_key] = page_input

        # RIGHT
        with col3:

            if st.button("➡", key=f"right_{uploaded_file.name}"):

                if st.session_state[session_key] < total_pages:
                    st.session_state[session_key] += 1

        st.caption(
            f"Showing Page {st.session_state[session_key]} of {total_pages}"
        )

        pdf_viewer(
            input=pdf_bytes,
            width=500,
            height=600,
            pages_to_render=[
                st.session_state[session_key]
            ]
        )

        uploaded_file.seek(0)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="title">📄 PDF Toolkit</div>',
    unsafe_allow_html=True
)

st.write("### All-in-One PDF Tools")

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🛠 PDF Tools")

    selected = option_menu(
        menu_title=None,

        options=[

            "Merge PDF",
            "Split PDF",
            "Compress PDF",
            "PDF to Word",
            "Word to PDF",

            "Rotate PDF",
            "Watermark PDF",
            # "OCR PDF",
            "Extract Images",
            "Protect PDF",
            "Unlock PDF",
            "Edit PDF"

        ],

        icons=[

            "files",
            "scissors",
            "archive",
            "file-earmark-word",
            "file-earmark-pdf",

            "arrow-repeat",
            "droplet",
            # "file-text",
            "images",
            "lock",
            "unlock",
            "pencil"

        ],

        default_index=0
    )

# ==========================================
# MERGE PDF
# ==========================================

if selected == "Merge PDF":

    st.header("🔗 Merge PDFs")

    col1, col2 = st.columns([1,1])

    # with col1:

    #     uploaded_files = st.file_uploader(
    #         "Upload PDFs",
    #         type=["pdf"],
    #         accept_multiple_files=True
    #     )

    #     if uploaded_files:

    #         if st.button("Merge PDFs"):
    with col1:

        uploaded_files = st.file_uploader(
            "Upload PDFs",
            type=["pdf"],
            accept_multiple_files=True
        )

        if uploaded_files:

            # ==========================================
            # CHECK ENCRYPTED PDFs
            # ==========================================

            for pdf in uploaded_files:

                try:

                    pdf.seek(0)

                    reader = PdfReader(pdf)

                    if reader.is_encrypted:

                        st.warning(
                            f"🔒 {pdf.name} is password protected"
                        )

                        st.text_input(
                            f"Password for {pdf.name}",
                            type="password",
                            key=f"merge_password_{pdf.name}"
                        )

                except:
                    pass

            # ==========================================
            # MERGE BUTTON
            # ==========================================

            if st.button("Merge PDFs"):

                output_path = "temp/merged.pdf"

                success = merge_pdfs(
                    uploaded_files,
                    output_path
                )

                if success:

                    st.success("PDFs merged successfully!")

                    with open(output_path, "rb") as f:

                        st.download_button(
                            "⬇ Download Merged PDF",
                            data=f,
                            file_name="merged.pdf",
                            key="download_merged_pdf"
                        )

                

    with col2:

        if uploaded_files:

            preview_pdf = st.selectbox(
                "Select PDF to Preview",
                options=range(len(uploaded_files)),
                format_func=lambda x: uploaded_files[x].name
            )

            show_pdf_preview(
                uploaded_files[preview_pdf]
            )

# ==========================================
# SPLIT PDF
# ==========================================

elif selected == "Split PDF":

    st.header("✂ Split PDF")

    col1, col2 = st.columns([1,1])

    with col1:

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        if uploaded_file:

            reader = PdfReader(uploaded_file)

            total_pages = len(reader.pages)
            

            uploaded_file.seek(0)

            split_option = st.radio(
                "Split Method",
                [
                    "Split All Pages",
                    "Split Page Range",
                    "Split Custom Pages"
                ]
            )

            # SPLIT ALL
            if split_option == "Split All Pages":

                if st.button("Split All Pages"):

                    files = split_all_pages(
                        uploaded_file
                    )

                    for file_path in files:

                        with open(file_path, "rb") as f:

                            st.download_button(
                                f"Download {file_path}",
                                data=f,
                                file_name=file_path,
                                key=f"split_{file_path}"
                            )

            # PAGE RANGE
            elif split_option == "Split Page Range":

                start_page = st.number_input(
                    "Start Page",
                    1,
                    total_pages,
                    1
                )

                end_page = st.number_input(
                    "End Page",
                    1,
                    total_pages,
                    min(2, total_pages)
                )

                if st.button("Split Page Range"):

                    output_path = split_page_range(
                        uploaded_file,
                        start_page,
                        end_page
                    )

                    with open(output_path, "rb") as f:

                        st.download_button(
                            "⬇ Download PDF",
                            data=f,
                            file_name="page_range.pdf"
                        )

            # CUSTOM PAGES
            elif split_option == "Split Custom Pages":

                custom_pages = st.text_input(
                    "Example: 1,3,5"
                )

                if st.button("Split Custom Pages"):

                    page_numbers = [
                        int(page.strip())
                        for page in custom_pages.split(",")
                    ]

                    output_path = split_custom_pages(
                        uploaded_file,
                        page_numbers
                    )

                    with open(output_path, "rb") as f:

                        st.download_button(
                            "⬇ Download PDF",
                            data=f,
                            file_name="custom_pages.pdf"
                        )

    with col2:

        if uploaded_file:
            show_pdf_preview(uploaded_file)

# ==========================================
# COMPRESS PDF
# ==========================================

elif selected == "Compress PDF":

    st.header("🗜 Compress PDF")

    col1, col2 = st.columns([1,1])

    with col1:

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        if uploaded_file:

            if st.button("Compress PDF"):

                input_path = "temp/input.pdf"

                with open(input_path, "wb") as f:
                    f.write(uploaded_file.read())

                output_path = "temp/compressed.pdf"

                compress_pdf(
                    input_path,
                    output_path
                )

                with open(output_path, "rb") as f:

                    st.download_button(
                        "⬇ Download Compressed PDF",
                        data=f,
                        file_name="compressed.pdf"
                    )

    with col2:

        if uploaded_file:
            show_pdf_preview(uploaded_file)

# ==========================================
# PDF TO WORD
# ==========================================

elif selected == "PDF to Word":

    st.header("📄 ➜ 📝 PDF to Word")

    col1, col2 = st.columns([1,1])

    with col1:

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        if uploaded_file:

            if st.button("Convert to Word"):

                output_docx = "temp/converted.docx"

                convert_pdf_to_word(
                    uploaded_file,
                    output_docx
                )

                with open(output_docx, "rb") as f:

                    st.download_button(
                        "⬇ Download Word",
                        data=f,
                        file_name="converted.docx"
                    )

    with col2:

        if uploaded_file:
            show_pdf_preview(uploaded_file)

# ==========================================
# WORD TO PDF
# ==========================================

elif selected == "Word to PDF":

    st.header("📝 ➜ 📄 Word to PDF")

    uploaded_file = st.file_uploader(
        "Upload DOCX",
        type=["docx"]
    )

    if uploaded_file:

        if st.button("Convert to PDF"):

            input_docx = "temp/input.docx"

            with open(input_docx, "wb") as f:
                f.write(uploaded_file.read())

            output_pdf = "temp/output.pdf"

            convert_word_to_pdf(
                input_docx,
                output_pdf
            )

            with open(output_pdf, "rb") as f:

                st.download_button(
                    "⬇ Download PDF",
                    data=f,
                    file_name="converted.pdf"
                )

# ==========================================
# ROTATE PDF
# ==========================================

elif selected == "Rotate PDF":

    st.header("🔄 Rotate PDF")

    col1, col2 = st.columns([1,1])

    with col1:

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        if uploaded_file:

            reader = PdfReader(uploaded_file)

            total_pages = len(reader.pages)

            uploaded_file.seek(0)

            rotate_option = st.radio(
                "Rotate Option",
                [
                    "Full PDF",
                    "Single Page",
                    "Page Range"
                ]
            )

            angle = st.selectbox(
                "Rotation Angle",
                [90, 180, 270]
            )

            # FULL PDF
            if rotate_option == "Full PDF":

                if st.button("Rotate Full PDF"):

                    output_path = rotate_full_pdf(
                        uploaded_file,
                        angle
                    )

                    with open(output_path, "rb") as f:

                        st.download_button(
                            "Download PDF",
                            data=f,
                            file_name="rotated.pdf"
                        )

            # SINGLE PAGE
            elif rotate_option == "Single Page":

                page_number = st.number_input(
                    "Page Number",
                    1,
                    total_pages,
                    1
                )

                if st.button("Rotate Page"):

                    output_path = rotate_single_page(
                        uploaded_file,
                        page_number,
                        angle
                    )

                    with open(output_path, "rb") as f:

                        st.download_button(
                            "Download PDF",
                            data=f,
                            file_name="rotated.pdf"
                        )

            # PAGE RANGE
            elif rotate_option == "Page Range":

                start_page = st.number_input(
                    "Start Page",
                    1,
                    total_pages,
                    1
                )

                end_page = st.number_input(
                    "End Page",
                    1,
                    total_pages,
                    2
                )

                if st.button("Rotate Page Range"):

                    output_path = rotate_page_range(
                        uploaded_file,
                        start_page,
                        end_page,
                        angle
                    )

                    with open(output_path, "rb") as f:

                        st.download_button(
                            "Download PDF",
                            data=f,
                            file_name="rotated.pdf"
                        )

    with col2:

        if uploaded_file:
            show_pdf_preview(uploaded_file)
            # ==========================================
# WATERMARK PDF
# ==========================================

elif selected == "Watermark PDF":

    st.header("💧 Watermark PDF")

    col1, col2 = st.columns([1,1])

    with col1:

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        watermark_text = st.text_input(
            "Watermark Text"
        )

        if uploaded_file:

            if st.button("Add Watermark"):

                output_path = add_watermark(
                    uploaded_file,
                    watermark_text
                )

                with open(output_path, "rb") as f:

                    st.download_button(
                        "⬇ Download PDF",
                        data=f,
                        file_name="watermarked.pdf"
                    )

    with col2:

        if uploaded_file:
            show_pdf_preview(uploaded_file)

# ==========================================
# OCR PDF
# ==========================================

# elif selected == "OCR PDF":

#     st.header("📝 OCR PDF")

#     col1, col2 = st.columns([1,1])

#     with col1:

#         uploaded_file = st.file_uploader(
#             "Upload PDF",
#             type=["pdf"]
#         )

#         if uploaded_file:

#             if st.button("Extract Text"):

#                 text = extract_text_from_pdf(
#                     uploaded_file
#                 )

#                 st.text_area(
#                     "Extracted Text",
#                     text,
#                     height=400
#                 )

#     with col2:

#         if uploaded_file:
#             show_pdf_preview(uploaded_file)

# elif selected == "OCR PDF":

#     st.header("📝 OCR PDF")

#     st.info("🚧 OCR feature is coming soon.")

#     st.warning(
#         """
#        COMING SOON⛷️⛷️
#         """
#     )

#     uploaded_file = st.file_uploader(
#         "Upload PDF",
#         type=["pdf"],
#         disabled=True
#     )

#     st.button(
#         "Extract Text",
#         disabled=True
#     )# ==========================================
# EXTRACT IMAGES
# ==========================================

elif selected == "Extract Images":

    st.header("🖼 Extract Images")

    col1, col2 = st.columns([1,1])

    with col1:

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        if uploaded_file:

            if st.button("Extract Images"):

                images = extract_images_from_pdf(
                    uploaded_file
                )

                # ==========================
                # CREATE ZIP FILE
                # ==========================

                zip_path = "temp/extracted_images.zip"

                with zipfile.ZipFile(
                    zip_path,
                    "w"
                ) as zipf:

                    for image_path in images:

                        zipf.write(
                            image_path,
                            arcname=os.path.basename(image_path)
                        )

                # ==========================
                # DOWNLOAD ALL BUTTON
                # ==========================

                with open(zip_path, "rb") as zip_file:

                    st.download_button(
                        "⬇ Download All Images (ZIP)",
                        data=zip_file,
                        file_name="extracted_images.zip",
                        mime="application/zip"
                    )

                st.divider()

                # ==========================
                # SHOW INDIVIDUAL IMAGES
                # ==========================

                for image_path in images:

                    st.image(
                        image_path,
                        width=300
                    )

                    with open(image_path, "rb") as f:

                        st.download_button(
                            f"Download {os.path.basename(image_path)}",
                            data=f,
                            file_name=os.path.basename(image_path),
                            key=f"image_{image_path}"
                        )

    with col2:

        if uploaded_file:
            show_pdf_preview(uploaded_file)
# ==========================================
# PROTECT PDF
# ==========================================

elif selected == "Protect PDF":

    st.header("🔒 Protect PDF")

    col1, col2 = st.columns([1,1])

    with col1:

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if uploaded_file:

            if st.button("Protect PDF"):

                output_path = protect_pdf(
                    uploaded_file,
                    password
                )

                with open(output_path, "rb") as f:

                    st.download_button(
                        "⬇ Download Protected PDF",
                        data=f,
                        file_name="protected.pdf"
                    )

    with col2:

        if uploaded_file:
            show_pdf_preview(uploaded_file)

# ==========================================
# UNLOCK PDF
# ==========================================

elif selected == "Unlock PDF":

    st.header("🔓 Unlock PDF")

    uploaded_file = st.file_uploader(
        "Upload Protected PDF",
        type=["pdf"]
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if uploaded_file:

        if st.button("Unlock PDF"):

            output_path = unlock_pdf(
                uploaded_file,
                password
            )

            with open(output_path, "rb") as f:

                st.download_button(
                    "⬇ Download Unlocked PDF",
                    data=f,
                    file_name="unlocked.pdf"
                )

# ==========================================
# EDIT PDF
# ==========================================

elif selected == "Edit PDF":

    st.header("✏ Edit PDF")

    col1, col2 = st.columns([1,1])

    with col1:

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        if uploaded_file:

            reader = PdfReader(uploaded_file)

            total_pages = len(reader.pages)

            uploaded_file.seek(0)

            text = st.text_input(
                "Text"
            )

            page_number = st.number_input(
                "Page",
                1,
                total_pages,
                1
            )

            x = st.number_input(
                "X Position",
                0,
                1000,
                100
            )

            y = st.number_input(
                "Y Position",
                0,
                1000,
                100
            )

            if st.button("Add Text"):

                output_path = add_text_to_pdf(
                    uploaded_file,
                    text,
                    page_number,
                    x,
                    y
                )

                with open(output_path, "rb") as f:

                    st.download_button(
                        "Download PDF",
                        data=f,
                        file_name="edited.pdf"
                    )

    with col2:

        if uploaded_file:
            show_pdf_preview(uploaded_file)# ==========================================
# FOOTER
# ==========================================

st.markdown("---")
st.caption("🚀 Built with Streamlit | PDF Toolkit")