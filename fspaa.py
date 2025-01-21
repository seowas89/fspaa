import requests
import streamlit as st
from bs4 import BeautifulSoup
import json


# Function to fetch SEO data for the given keyword using SEPAPI
def get_seo_data(keyword, api_key):
    url = f"https://api.sepapi.com/v1/seo/featured_snippet?keyword={keyword}&api_key={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Error fetching SEO data")
        return None


# Function to fetch People Also Ask from Google SERP
def get_people_also_ask(keyword):
    search_url = f"https://www.google.com/search?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting People Also Ask data
    people_also_ask = []
    for question in soup.find_all('div', {'class': 'related-question-pair'}):
        question_text = question.get_text()
        people_also_ask.append(question_text.strip())

    return people_also_ask


# Function to suggest SEO optimization strategies
def suggest_seo_optimization(current_snippet, competitor_content, your_content, people_ask_data):
    suggestions = []

    # Compare lengths and structure of the content
    if len(current_snippet) > len(your_content):
        suggestions.append("Make your content more concise and structured like the featured snippet.")
    
    if current_snippet != your_content:
        suggestions.append(f"Include key phrases from the featured snippet like: '{current_snippet[:50]}'")

    # Check for gaps and additional content from competitors
    if competitor_content and len(competitor_content) > len(your_content):
        suggestions.append("Add more relevant content like your competitors to enhance your chances.")

    # Incorporate People Also Ask questions
    for question in people_ask_data:
        suggestions.append(f"Consider including an answer to this question: '{question}'")

    # Final SEO content optimization
    suggestions.append("Focus on clear, concise content with rich formatting and frequently asked questions.")

    return suggestions


# Main function to run the app
def main():
    # Define your API key
    api_key = '74a076b94b88e3541df371407c65d4b4628da2d2db43576e0667d50a35d5e395'

    st.title('SEO Optimization for Featured Snippets')

    # Get keyword input from the user
    keyword = st.text_input("Enter the Keyword for SEO Optimization:")

    if keyword:
        st.write(f"Fetching SEO data for: {keyword}...")

        # Fetch SEO data
        seo_data = get_seo_data(keyword, api_key)

        if seo_data:
            featured_snippet = seo_data.get('featured_snippet', '')
            competitor_content = seo_data.get('competitor_content', '')
            your_content = seo_data.get('your_content', '')

            st.subheader("Featured Snippet Content:")
            st.write(featured_snippet)

            st.subheader("Competitor Content:")
            st.write(competitor_content)

            st.subheader("Your Content:")
            st.write(your_content)

            # Fetch People Also Ask questions
            people_ask_data = get_people_also_ask(keyword)

            st.subheader("People Also Ask Questions:")
            for question in people_ask_data:
                st.write(question)

            # Suggest SEO optimization
            st.subheader("SEO Optimization Suggestions:")
            suggestions = suggest_seo_optimization(featured_snippet, competitor_content, your_content, people_ask_data)

            for suggestion in suggestions:
                st.write(f"- {suggestion}")


if __name__ == '__main__':
    main()
