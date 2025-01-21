import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def initialize_model():
    try:
        model_name = "t5-small"  # You can try 't5-base' or 't5-large' for better results
        model = T5ForConditionalGeneration.from_pretrained(model_name)
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

def rewrite_to_human_style(text, model, tokenizer):
    if model is None or tokenizer is None:
        return "Model not loaded successfully."

    input_text = "summarize: " + text
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")

    summary_ids = model.generate(inputs['input_ids'], max_length=150, num_beams=4, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    sentences = sent_tokenize(summary)
    short_sentences = [sentence.strip() for sentence in sentences if len(sentence) > 0]
    
    human_written_text = " ".join(short_sentences)
    
    return human_written_text

def main():
    st.title("AI to Human Written Style Converter")

    ai_text = st.text_area("Enter AI-generated text:", height=250)

    if ai_text:
        model, tokenizer = initialize_model()

        if model and tokenizer:
            human_text = rewrite_to_human_style(ai_text, model, tokenizer)
            st.subheader("Converted Human-written Style:")
            st.write(human_text)
        else:
            st.warning("Unable to load the model.")

if __name__ == '__main__':
    main()
