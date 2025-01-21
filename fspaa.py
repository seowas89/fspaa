import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Hugging Face API key
huggingface_api_key = "your_huggingface_api_key"  # Replace with your Hugging Face API Key

# Function to fetch Google search results using SerpAPI
def get_serp_results(keyword):
    params = {
        "q": keyword,
        "api_key": "your_serpapi_key",  # Replace with your SerpAPI key
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

# Function to analyze text with Hugging Face API for Named Entity Recognition (NER) and Sentiment Analysis
def analyze_text_with_huggingface(text):
    headers = {
        "Authorization": f"Bearer {huggingface_api_key}"
    }
    
    # Sentiment Analysis
    sentiment_url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    sentiment_response = requests.post(sentiment_url, headers=headers, json={"inputs": text})
    sentiment = sentiment_response.json()
    
    sentiment_score = sentiment[0]['label'] if sentiment else 'neutral'

    # Named Entity Recognition (NER)
    ner_url = "https://api-inference.huggingface.co/models/dbmdz/bert-large-cased-finetuned-conll03-english"
    ner_response = requests.post(ner_url, headers=headers, json={"inputs": text})
    entities = ner_response.json()

    return sentiment_score, entities

# Function to analyze the text and suggest SEO optimization
def analyze_and_suggest_optimization(keyword, featured_snippet, competitor_content, your_content, paa_questions):
    # 1. Keyword Optimization: Ensure the keyword appears in the title, content, and meta description.
    featured_keywords = process_keywords(featured_snippet)
    competitor_keywords = process_keywords(competitor_content)
    your_keywords = process_keywords(your_content)
    
    # 2. Analyze sentiment using Hugging Face model
    sentiment_score, entities = analyze_text_with_huggingface(your_content)

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
    
    # Sentiment Analysis Suggestion
    if sentiment_score == "NEGATIVE":
        suggestions.append("Consider adjusting your content tone to be more positive.")
    elif sentiment_score == "POSITIVE":
        suggestions.append("Your content tone is positive, which is great for engagement!")
    
    # Entity Suggestion (NER) - Include important entities in the content
    important_entities = [entity['word'] for entity in entities if entity['entity_group'] in ['PER', 'LOC', 'ORG']]
    if important_entities:
        suggestions.append(f"Consider adding or emphasizing entities such as: {', '.join(important_entities)}")

    # Content Structure: Make sure your content is well-structured with subheadings (H2/H3).
    suggestions.append("Ensure your content includes structured headings (H2/H3) to improve readability.")
    
    return suggestions

# Main function to get data and analyze
def main():
    keyword = input("Enter the keyword to analyze: ")
    
    # Get Google Search Results
    results = get_serp_results(keyword)
    
    # Extract Featured Snippet Content, Competitor Content, and PAA questions
    featured_snippet = results.get('answer_box', {}).get('snippet', '')
    competitor_content = fetch_content_from_url(results['organic_results'][0]['link'])  # First organic result
    paa_questions = extract_paa(results)
    
    # Your Content (Here you can add your content manually or fetch it from your site)
    your_content = input("Enter your content: ")
    
    # Analyze and suggest optimizations
    suggestions = analyze_and_suggest_optimization(keyword, featured_snippet, competitor_content, your_content, paa_questions)
    
    print("\nSuggested SEO Optimizations for Keyword:", keyword)
    for suggestion in suggestions:
        print(f"- {suggestion}")

# Run the app
if __name__ == "__main__":
    main()
