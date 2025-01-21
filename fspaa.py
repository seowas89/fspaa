import streamlit as st
from transformers import pipeline
import nltk

# Download NLTK data for sentence tokenization
nltk.download('punkt')

# Function to initialize the summarization pipeline
def initialize_pipeline():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return summarizer

# Function to convert AI-generated text into a human-written style
def rewrite_to_human_style(text, summarizer):
    # Summarize the text to make it more concise and human-like
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    
    # Extract the summarized text
    human_text = summary[0]['summary_text']
    
    # Split into short sentences
    sentences = nltk.sent_tokenize(human_text)
    short_sentences = [sentence.strip() for sentence in sentences if len(sentence) > 0]
    
    # Join the sentences back into a single text
    human_written_text = " ".join(short_sentences)
    
    return human_written_text

# Streamlit app to input and display the transformed text
def main():
    st.title("AI to Human Written Style Converter")

    ai_text = st.text_area("Enter AI-generated text:", height=250)

    if ai_text:
        summarizer = initialize_pipeline()

        # Process the AI-generated text
        human_text = rewrite_to_human_style(ai_text, summarizer)
        st.subheader("Converted Human-written Style:")
        st.write(human_text)

if __name__ == '__main__':
    main()
