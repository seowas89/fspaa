import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize Spacy for local NLP tasks
nlp = spacy.load("en_core_web_sm")

# Function to fetch Google search results using SerpAPI
def get_serp_results(keyword, api_key):
    params = {
        "q": keyword,
        "api_key": api_key,  # Use the provided SerpAPI key
        "engine": "google"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results

# Function to extract PAA questions from the Google search results
def extract_paa(results):
    paa_questions = []
    if "related_questions" in results:
        for question in results["related_questions"]:
            paa_questions.append(question["question"])
    return paa_questions

# Function to fetch content from a given URL
def fetch_content_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all('p')
    content = " ".join([p.get_text() for p in paragraphs])
    return content

# Function to extract and process keywords
def process_keywords(text):
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    
    words = word_tokenize(text.lower())
    filtered_words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words and w.isalpha()]
    return filtered_words

# Function to analyze text with Spacy (NER)
def analyze_entities_spacy(text):
    doc = nlp(text)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities

# Function to analyze text with TextRazor API for Named Entity Recognition (NER)
def analyze_entities_textrazor(text, api_key):
    url = "https://api.textrazor.com/"
    headers = {
        "x-textrazor-key": api_key
    }
    data = {
        "text": text,
        "extractors": "entities"
    }
    response = requests.post(url, headers=headers, data=data)
    entities = response.json()
    return entities.get("response", {}).get("entities", [])

# Function to analyze the text and suggest SEO optimization
def analyze_and_suggest_optimization(keyword, featured_snippet, competitor_content, your_content, paa_questions):
    # 1. Keyword Optimization: Ensure the keyword appears in the title, content, and meta description.
    featured_keywords = process_keywords(featured_snippet)
    competitor_keywords = process_keywords(competitor_content)
    your_keywords = process_keywords(your_content)
    
    # 2. Analyze Sentiment and Entities using Spacy/TextRazor
    spacy_entities = analyze_entities_spacy(your_content)
    textrazor_entities = analyze_entities_textrazor(your_content, "your_textrazor_api_key")  # Replace with your Textrazor API key
    
    suggestions = []
    
    # Keyword Density Check
    missing_keywords = [kw for kw in featured_keywords if kw not in your_keywords]
    if missing_keywords:
        suggestions.append(f"Consider adding missing keywords like: {', '.join(missing_keywords)}")

    # PAA Section Improvement
    paa_keywords = [process_keywords(q) for q in paa_questions]
    paa_keywords_flat = [item for sublist in paa_keywords for item in sublist]
    
    if paa_keywords_flat:
        suggestions.append(f"Integrate phrases from 'People Also Ask' such as: {', '.join(set(paa_keywords_flat))}")
    
    # Entity Suggestion (NER) - Include important entities in the content
    important_spacy_entities = [entity[0] for entity in spacy_entities if entity[1] in ['PERSON', 'GPE', 'ORG']]
    important_textrazor_entities = [entity['rawText'] for entity in textrazor_entities if entity['type'] in ['Person', 'Organization', 'Location']]
    
    if important_spacy_entities:
        suggestions.append(f"Consider adding or emphasizing Spacy entities such as: {', '.join(important_spacy_entities)}")
    if important_textrazor_entities:
        suggestions.append(f"Consider adding or emphasizing TextRazor entities such as: {', '.join(important_textrazor_entities)}")

    # Content Structure: Make sure your content is well-structured with subheadings (H2/H3).
    suggestions.append("Ensure your content includes structured headings (H2/H3) to improve readability.")
    
    return suggestions

# Streamlit app function
import streamlit as st

def main():
    st.title("SEO Optimization for Featured Snippets")
    
    # Input the keyword for analysis
    keyword = st.text_input("Enter Keyword", "")
    
    if keyword:
        # Provide your SerpAPI key here
        serpapi_key = "74a076b94b88e3541df371407c65d4b4628da2d2db43576e0667d50a35d5e395"
        
        # Get Google Search Results using SerpAPI
        results = get_serp_results(keyword, serpapi_key)
        
        # Extract Featured Snippet Content, Competitor Content, and PAA questions
        featured_snippet = results.get('answer_box', {}).get('snippet', '')
        competitor_content = fetch_content_from_url(results['organic_results'][0]['link'])  # First organic result
        paa_questions = extract_paa(results)
        
        # Input Your Content
        your_content = st.text_area("Enter Your Content", "")
        
        # If content is entered, analyze and suggest SEO optimizations
        if your_content:
            suggestions = analyze_and_suggest_optimization(keyword, featured_snippet, competitor_content, your_content, paa_questions)
            
            st.subheader("SEO Optimization Suggestions")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")

if __name__ == "__main__":
    main()
