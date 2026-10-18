# 📚 AI Lecture Notes Summarizer

A Streamlit application that uses the Hugging Face `distilbart-cnn-12-6` model to generate concise summaries of text or PDF files. Ideal for summarizing lecture notes or long documents.

## Features
- **Text Summarization**: Directly input text to get a summary.
- **PDF Extraction**: Upload a PDF file, and the app will extract the text and summarize it.
- **Customizable Length**: Choose between Short, Medium, or Long summaries.
- **Sentence Chunking**: Intelligently chunks text by sentences to preserve context.
- **Downloadable Output**: Easily download the summarized text as a `.txt` file.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd notes_summarizer
   ```

2. **Install the dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

## Usage
- Run the app and open the provided local URL in your browser.
- Select either "Text" or "PDF" as the input type.
- Adjust the summary length slider to your preference.
- Provide your text or upload a PDF.
- Click "Generate Summary" and wait for the AI to process the input.
- Review the summary and optionally download it.

## Testing
To run the utility tests:
```bash
pytest test_app.py
```
