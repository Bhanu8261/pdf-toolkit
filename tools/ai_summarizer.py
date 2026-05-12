from transformers import pipeline
import fitz

# ==========================================
# LOAD MODEL
# ==========================================

summarizer = pipeline(
    task="summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

# ==========================================
# EXTRACT PDF TEXT
# ==========================================

def extract_pdf_text(uploaded_file):

    uploaded_file.seek(0)

    pdf_bytes = uploaded_file.read()

    doc = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in doc:

        text += page.get_text()

    doc.close()

    return text

# ==========================================
# SUMMARIZE PDF
# ==========================================

def summarize_pdf(uploaded_file):

    text = extract_pdf_text(uploaded_file)

    # LIMIT TEXT SIZE
    text = text[:4000]

    summary = summarizer(

        text,

        max_length=200,
        min_length=50,

        do_sample=False

    )

    return summary[0]["summary_text"]