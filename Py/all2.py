import os
import re
import spacy
from docx import Document
from PyPDF2 import PdfReader
from faker import Faker
import logging

# Load spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Initialize Faker for fake data generation
fake = Faker()

# HIPAA Identifiers regex patterns categorized by type
HIPAA_PATTERNS = {
    'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
    'Zip Code': r'\b\d{5}(?:-\d{4})?\b',
    'Phone Number': [r'\b\d{10}\b', r'\b\d{3}-\d{3}-\d{4}\b'],  # 10-digit, formatted
    'Credit Card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    'NPI': r'\b\d{2}-\d{7}\b',
    'Patient ID': r'\b\d{8,9}\b',
    'Names': r'\b([A-Z][a-z]+),?\s([A-Z][a-z]+)\b',  # First Last Name pattern
    # Add more patterns if needed, like Email or Date of Birth
}

# Functions to generate realistic fake data for each category
def generate_fake_data(category):
    if category == 'SSN':
        return fake.ssn()
    elif category == 'Zip Code':
        return fake.zipcode()
    elif category == 'Phone Number':
        return fake.phone_number()
    elif category == 'Credit Card':
        return fake.credit_card_number()
    elif category == 'NPI':
        return str(fake.unique.random_number(digits=9, fix_len=True))  # Fake NPI
    elif category == 'Patient ID':
        return str(fake.unique.random_number(digits=8, fix_len=True))  # Fake Patient ID
    elif category == 'Names':
        return fake.name()

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
    # Use spaCy NER to identify PERSON entities (names) and locations (GPE)
    doc = nlp(text)
    
    # Replace identified PERSON names and GPE locations
    for ent in doc.ents:
        if ent.label_ == 'PERSON':  # Replace names with fake names
            text = text.replace(ent.text, generate_fake_data('Names'))
        elif ent.label_ == 'GPE':  # Replace locations with fake locations
            text = text.replace(ent.text, fake.city())
        elif ent.label_ == 'DATE':  # Replace dates with fake dates
            text = text.replace(ent.text, fake.date())
        # Add other NER entity replacement as needed (like ORG, etc.)

    # Regex-based de-identification for HIPAA identifiers
    for category, patterns in HIPAA_PATTERNS.items():
        if isinstance(patterns, list):  # Multiple patterns for this category (e.g., Phone Number)
            for pattern in patterns:
                text = re.sub(pattern, generate_fake_data(category), text)
        else:
            text = re.sub(patterns, generate_fake_data(category), text)

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
