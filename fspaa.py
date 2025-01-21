import requests
from serpapi import GoogleSearch
import streamlit as st

# Function to fetch Google Search Results using SerpAPI
def get_serp_results(keyword, api_key):
    params = {
        "q": keyword,
        "api_key": api_key,  # Use your actual SerpAPI key
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
    return response.text

# Streamlit app function
def main():
    st.title("SEO Optimization for Featured Snippets")
    
    # Input the keyword for analysis
    keyword = st.text_input("Enter Keyword", "")
    
    if keyword:
        # Provide your SerpAPI key here
        serpapi_key = "74a076b94b88e3541df371407c65d4b4628da2d2db43576e0667d50a35d5e395"
        
        try:
            # Get Google Search Results using SerpAPI
            results = get_serp_results(keyword, serpapi_key)
            
            if not results:
                st.error("No results found. Please check your API key or try another keyword.")
                return
            
            # Extract Featured Snippet Content and PAA questions
            featured_snippet = results.get('answer_box', {}).get('snippet', 'No featured snippet found.')
            paa_questions = extract_paa(results)
            
            # Show the Featured Snippet content
            st.subheader("Featured Snippet")
            st.write(featured_snippet)
            
            # Show the PAA questions
            st.subheader("People Also Ask (PAA) Questions")
            if paa_questions:
                for idx, question in enumerate(paa_questions, 1):
                    st.write(f"{idx}. {question}")
            else:
                st.write("No PAA questions found.")
            
            # Input Your Content
            your_content = st.text_area("Enter Your Content", "")
            
            if your_content:
                st.write("Your content: ", your_content)
                
                # Placeholder for further optimization logic (Add your NLP analysis logic here)
                st.write("Optimization suggestions will be displayed here.")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
