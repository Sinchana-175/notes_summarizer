import streamlit as st
from transformers import pipeline
from pypdf import PdfReader
import warnings
import re

warnings.filterwarnings("ignore")

# ---------------------------
# Load Model (fast)
# ---------------------------
@st.cache_resource
def load_model():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

summarizer = load_model()

# ---------------------------
# PDF Extraction
# ---------------------------
def extract_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return text

# ---------------------------
# Clean Text
# ---------------------------
def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace("- ", "")
    text = " ".join(text.split())
    return text

# ---------------------------
# Chunking (bigger = faster)
# ---------------------------
def split_text(text, chunk_size=1500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ---------------------------
# UI
# ---------------------------
st.title("📚 AI Lecture Notes Summarizer")

option = st.radio("Choose Input Type:", ["Text", "PDF"])

text = ""

if option == "Text":
    text = st.text_area("Enter Lecture Text:")

elif option == "PDF":
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    if uploaded_file is not None:
        text = extract_pdf(uploaded_file)
        text = clean_text(text)

# ---------------------------
# Summarization
# ---------------------------
if st.button("Generate Summary"):

    if not text:
        st.warning("Please provide input!")
    else:
        chunks = split_text(text)
        summaries = []

        with st.spinner("Processing..."):
            for chunk in chunks:
                if len(chunk.strip()) < 50:
                    continue

                word_count = len(chunk.split())

                max_len = 50
                min_len = 20

                result = summarizer(
                    chunk,
                    max_length=max_len,
                    min_length=min_len,
                    do_sample=False
                )

                summaries.append(result[0]['summary_text'])

        # ---------------------------
        # FINAL PARAGRAPH GROUPING
        # ---------------------------
        combined_text = " ".join(summaries)

        sentences = re.split(r'(?<=[.!?]) +', combined_text)

        paragraphs = []
        temp = []

        for sentence in sentences:
            temp.append(sentence)

            if len(temp) == 3:   # group size
                paragraphs.append(" ".join(temp))
                temp = []

        if temp:
            paragraphs.append(" ".join(temp))

        # ---------------------------
        # OUTPUT
        # ---------------------------
        st.subheader("📌 Summary")

        for para in paragraphs:
            st.write(para)

        # ---------------------------
        # DOWNLOAD
        # ---------------------------
        st.download_button(
            label="Download Summary",
            data="\n\n".join(paragraphs),
            file_name="summary.txt"
        )