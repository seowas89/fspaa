import requests
import streamlit as st
from bs4 import BeautifulSoup


# Function to fetch SEO data for the given keyword using SerpApi
def get_seo_data(keyword, api_key):
    url = f"https://serpapi.com/search?q={keyword}&api_key={api_key}&hl=en"

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Extracting data from the response
        data = response.json()
        
        # Extracting the relevant fields: Featured Snippet, Competitor Content, and Your Content
        featured_snippet = ""
        competitor_content = ""
        your_content = ""

        if "organic_results" in data:
            for result in data["organic_results"]:
                if "snippet" in result:
                    featured_snippet = result["snippet"]
                    break
        
        # Extract the first result as the competitor content
        if "organic_results" in data:
            competitor_content = data["organic_results"][0].get('title', '')
        
        # Placeholder for your own content (can be modified by the user input)
        your_content = "Placeholder content for your website."

        return {
            "featured_snippet": featured_snippet,
            "competitor_content": competitor_content,
            "your_content": your_content
        }

    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {e}")
        return None


# Function to fetch People Also Ask from Google SERP using SerpApi
def get_people_also_ask(keyword, api_key):
    url = f"https://serpapi.com/search?q={keyword}&api_key={api_key}&hl=en"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if status code is not 2xx
        
        data = response.json()
        people_also_ask = []

        if "related_questions" in data:
            for question in data["related_questions"]:
                people_also_ask.append(question["question"])

        return people_also_ask
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching People Also Ask data: {e}")
        return []


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

    # Provide content structure suggestions
    content = f"To win the Featured Snippet, use a structured approach. Here's an optimized version of your content:\n\n"

    # Example optimized content suggestion
    optimized_content = f"**Optimized Answer**: {current_snippet}.\n\n"
    optimized_content += f"Make sure to place this key information in your introduction to grab attention right away."

    suggestions.append(content + optimized_content)

    # Suggest content placement
    suggestions.append("Place the answer to the most frequently asked question in your introduction.")
    
    return suggestions, optimized_content


# Main function to run the app
def main():
    # Define your SerpApi key (replace with your own key)
    api_key = '74a076b94b88e3541df371407c65d4b4628da2d2db43576e0667d50a35d5e395'

    st.title('SEO Optimization for Featured Snippets')

    # Get keyword input from the user
    keyword = st.text_input("Enter the Keyword for SEO Optimization:")

    # Inputs for user to enter content
    current_fs = st.text_area("Paste the current Featured Snippet content:")
    competitor_content = st.text_area("Enter the Competitor's content:")
    your_content = st.text_area("Enter your content:")

    # Button to analyze the SERP data and provide suggestions
    if st.button('Check SERP and Optimize'):
        if keyword:
            st.write(f"Fetching SEO data for: {keyword}...")

            # Fetch SEO data using SerpApi
            seo_data = get_seo_data(keyword, api_key)

            if seo_data:
                # Get the Featured Snippet and Competitor Content from SerpApi
                featured_snippet = seo_data.get('featured_snippet', '')
                competitor_content_serp = seo_data.get('competitor_content', '')
                your_content_serp = your_content  # Use the user's input

                st.subheader("Current Featured Snippet Content:")
                st.write(current_fs)

                st.subheader("Competitor Content:")
                st.write(competitor_content)

                st.subheader("Your Content:")
                st.write(your_content)

                # Fetch People Also Ask questions
                people_ask_data = get_people_also_ask(keyword, api_key)

                st.subheader("People Also Ask Questions:")
                for question in people_ask_data:
                    st.write(question)

                # Suggest SEO optimization
                st.subheader("SEO Optimization Suggestions:")
                suggestions, optimized_content = suggest_seo_optimization(
                    current_fs, competitor_content, your_content, people_ask_data
                )

                for suggestion in suggestions:
                    st.write(f"- {suggestion}")

                st.subheader("Optimized Content Suggestion:")
                st.write(optimized_content)

                st.subheader("Content Placement Suggestions:")
                st.write("To improve your chances of winning the featured snippet, place the optimized answer at the beginning of your content.")
                st.write("Ensure that you structure your content with clear headings, subheadings, and concise bullet points.")

if __name__ == '__main__':
    main()
