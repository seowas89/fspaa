import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK data for sentence tokenization
nltk.download('punkt')

# Function to initialize the T5 model and tokenizer
def initialize_model():
    model_name = "t5-small"  # You can try 't5-base' or 't5-large' for better results
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    return model, tokenizer

# Function to convert AI-generated text into a human-written style
def rewrite_to_human_style(text, model, tokenizer):
    # Summarize the text to make it more concise and human-like
    input_text = "summarize: " + text
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    
    # Generate the summary
    summary_ids = model.generate(inputs['input_ids'], max_length=150, num_beams=4, early_stopping=True)
    
    # Decode the generated summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    # Split into short sentences
    sentences = sent_tokenize(summary)
    short_sentences = [sentence.strip() for sentence in sentences if len(sentence) > 0]
    
    # Join the sentences back into a single text
    human_written_text = " ".join(short_sentences)
    
    return human_written_text

# Streamlit app to input and display the transformed text
def main():
    # Set up Streamlit UI
    st.title("AI to Human Written Style Converter")

    # Input text (AI-generated text)
    ai_text = st.text_area("Enter AI-generated text:", height=250)
    
    if ai_text:
        # Initialize the model and tokenizer
        model, tokenizer = initialize_model()
        
        # Process the AI-generated text
        human_text = rewrite_to_human_style(ai_text, model, tokenizer)
        
        # Display the human-written text
        st.subheader("Converted Human-written Style:")
        st.write(human_text)

if __name__ == '__main__':
    main()
