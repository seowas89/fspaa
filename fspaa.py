import streamlit as st
import spacy
import nltk

# Download necessary NLTK data
nltk.download('punkt')

# Initialize the spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to simplify and humanize the text
def simplify_text(text):
    doc = nlp(text)
    
    sentences = list(doc.sents)
    simplified_sentences = []

    for sentence in sentences:
        simplified_sentence = " ".join([token.text for token in sentence if not token.is_stop and not token.is_punct])
        simplified_sentences.append(simplified_sentence)
    
    simplified_text = ". ".join(simplified_sentences)
    
    return simplified_text

# Streamlit app
def main():
    st.title("AI to Human-like Text Converter")

    # Get user input
    ai_text = st.text_area("Enter AI-generated text:", height=250)

    if ai_text:
        # Simplify AI-generated text
        simplified_text = simplify_text(ai_text)
        
        # Display the simplified text
        st.subheader("Converted Human-like Text:")
        st.write(simplified_text)

if __name__ == '__main__':
    main()
