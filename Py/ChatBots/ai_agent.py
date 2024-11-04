import spacy
import nltk
from transformers import pipeline
import speech_recognition as sr

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize transformers pipeline for text generation
text_generator = pipeline("text-generation", model="gpt-2")

# Initialize speech recognizer
recognizer = sr.Recognizer()

def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None

def process_text(text):
    doc = nlp(text)
    for token in doc:
        print(f"{token.text}: {token.pos_}")

def generate_response(prompt):
    response = text_generator(prompt, max_length=50)
    print(response[0]['generated_text'])

def main():
    while True:
        command = recognize_speech()
        if command:
            process_text(command)
            generate_response(command)
        if command and "exit" in command.lower():
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
