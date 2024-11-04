import os
import re
import spacy
from docx import Document
from PyPDF2 import PdfReader
import pdfminer
import logging


# Load spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Define HIPAA identifiers
HIPAA_IDENTIFIERS = [
    r'\b\d{3}-\d{2}-\d{4}\b',  # Social Security Numbers (SSN)
    r'\b\d{5}\b',  # Zip Codes
    r'\b\d{10}\b',  # Phone Numbers
    r'\b\d{3}-\d{3}-\d{4}\b',  # Phone Numbers (formatted)
    r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit Card Numbers
    r'\b\d{2}-\d{7}\b',  # National Provider Identifier (NPI)
    r'\b\d{8,9}\b',  # Patient ID
    r'\b([A-Z][a-z]+),?\s([A-Z][a-z]+)\b',  # Patient Names (simple pattern)
    # Other identifiers like email, dates, IP address etc. can be added here.
]

# De-identification function for text files
def deidentify_text_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    text = deidentify_text(text)
    with open(file_path, 'w') as file:
        file.write(text)

# De-identification function for PDF files
def deidentify_pdf_file(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    deidentified_text = deidentify_text(text)
    with open(file_path.replace(".pdf", "_deidentified.txt"), 'w') as f:
        f.write(deidentified_text)

# De-identification function for Word files (.docx)
def deidentify_word_file(file_path):
    document = Document(file_path)
    for para in document.paragraphs:
        para.text = deidentify_text(para.text)
    document.save(file_path.replace(".docx", "_deidentified.docx"))

# De-identification logic
def deidentify_text(text):
    # Apply spaCy NER
    doc = nlp(text)
    for ent in doc.ents:
        text = text.replace(ent.text, "[REDACTED]")

    # Apply regex-based de-identification for HIPAA identifiers
    for pattern in HIPAA_IDENTIFIERS:
        text = re.sub(pattern, "[REDACTED]", text)

    return text

# Main function to route based on file extension
def deidentify_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        deidentify_text_file(file_path)
    elif ext == ".pdf":
        deidentify_pdf_file(file_path)
    elif ext == ".docx":
        deidentify_word_file(file_path)
    else:
        logging.error(f"Unsupported file type: {ext}")

# Example usage
if __name__ == "__main__":
    # Replace with the path of your file to deidentify
    file_path = r"C:\Users\Jayanth C\Downloads\Optimization_Techniques_SALES_DATA.docx"
    deidentify_file(file_path)
