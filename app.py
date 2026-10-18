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
    try:
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content

        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

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
    # Split text into sentences instead of raw characters to preserve meaning
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)
        if current_length + sentence_length > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def main():
    # ---------------------------
    # UI
    # ---------------------------
    st.title("📚 AI Lecture Notes Summarizer")

    option = st.radio("Choose Input Type:", ["Text", "PDF"])

    summary_length_option = st.select_slider(
        "Choose Summary Length:",
        options=["Short", "Medium", "Long"],
        value="Medium"
    )

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

                    # Dynamically set constraints based on word count
                    if word_count < 20:
                        continue # Too small to summarize

                    # Use the slider option to adjust desired lengths
                    if summary_length_option == "Short":
                        target_max = 50
                        target_min = 10
                    elif summary_length_option == "Medium":
                        target_max = 100
                        target_min = 20
                    else: # Long
                        target_max = 200
                        target_min = 50

                    max_len = min(word_count - 5, target_max)
                    min_len = min(target_min, max_len - 5)

                    # Fallback to prevent model crash if constraints are tight
                    max_len = max(max_len, 10)
                    min_len = max(min_len, 5)

                    try:
                        result = summarizer(
                            chunk,
                            max_length=max_len,
                            min_length=min_len,
                            do_sample=False
                        )
                        summaries.append(result[0]['summary_text'])
                    except Exception as e:
                        # In case the model fails (e.g. sequence length issues)
                        summaries.append(f"[Error summarizing chunk: {str(e)}]")

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

if __name__ == "__main__":
    main()
