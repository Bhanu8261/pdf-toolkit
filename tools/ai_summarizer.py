import fitz
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

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

    parser = PlaintextParser.from_string(
        text,
        Tokenizer("english")
    )

    summarizer = LsaSummarizer()

    summary = summarizer(
        parser.document,
        5
    )

    final_summary = ""

    for sentence in summary:

        final_summary += str(sentence) + " "

    return final_summary