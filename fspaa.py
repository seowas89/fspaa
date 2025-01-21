import streamlit as st
import spacy
from googletrans import Translator

# Load spaCy language model for text simplification
nlp = spacy.load("en_core_web_sm")

# Initialize googletrans translator
translator = Translator()

# Function to simplify text by removing stopwords and punctuation
def simplify_text(text):
    doc = nlp(text)
    simplified_sentences = []
    
    for sentence in doc.sents:
        simplified_sentence = " ".join([token.text for token in sentence if not token.is_stop and not token.is_punct])
        simplified_sentences.append(simplified_sentence)
    
    simplified_text = " ".join(simplified_sentences)
    return simplified_text

# Function to translate text into Spanish
def translate_to_spanish(text):
    translated = translator.translate(text, src='en', dest='es')
    return translated.text

# Function to translate Spanish text into British English (googletrans supports general translation)
def translate_to_british_english(text):
    translated = translator.translate(text, src='es', dest='en')
    return translated.text

# Streamlit App
def main():
    st.title("Text Simplification and Translation App")
    
    # Input 1: Text to simplify
    input_text_1 = st.text_area("Enter the text to simplify:")
    
    if input_text_1:
        # Simplify the text
        simplified_text = simplify_text(input_text_1)
        st.subheader("Simplified Text:")
        st.write(simplified_text)
    
    # Input 2: Text to translate into Spanish and then to British English
    input_text_2 = st.text_area("Enter the text to translate into Spanish and then to British English:")
    
    if input_text_2:
        # Translate to Spanish
        spanish_text = translate_to_spanish(input_text_2)
        st.subheader("Text Translated to Spanish:")
        st.write(spanish_text)
        
        # Translate the Spanish text back into British English
        british_english_text = translate_to_british_english(spanish_text)
        st.subheader("Text Translated Back to British English:")
        st.write(british_english_text)

if __name__ == '__main__':
    main()
