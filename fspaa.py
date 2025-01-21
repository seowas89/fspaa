import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from serpapi import GoogleSearch
from wordcloud import WordCloud

# Function to fetch data from serpapi for Google Play
def fetch_playstore_data(query):
    params = {
        "q": query,
        "engine": "google",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "api_key": "74a076b94b88e3541df371407c65d4b4628da2d2db43576e0667d50a35d5e395",
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()

    # Extracting the relevant data from the search results
    apps_data = []
    for result in results.get('organic_results', []):
        if 'title' in result and 'link' in result:
            app_name = result['title']
            app_url = result['link']
            description = result.get('snippet', '')
            apps_data.append({
                "App Name": app_name,
                "App URL": app_url,
                "Description": description,
            })

    return pd.DataFrame(apps_data)

# Function to visualize wordcloud based on descriptions
def visualize_wordcloud(dataframe):
    all_text = " ".join(dataframe['Description'].fillna(''))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
    
    # Display the word cloud image
    st.image(wordcloud.to_array(), use_column_width=True)

# Streamlit UI layout
st.title("Google Play Store Keyword Research Tool")

# Input search term (keyword)
query = st.text_input("Enter Keyword to Research", "")

if query:
    st.write(f"Searching for apps related to **{query}**...")

    # Fetch data from the API
    data = fetch_playstore_data(query)
    if not data.empty:
        st.write(f"Found **{len(data)}** apps matching the keyword.")

        # Show data as a table
        st.dataframe(data)

        # Visualizations
        st.subheader("Visualizations")
        
        # Wordcloud visualization
        st.subheader("Word Cloud of App Descriptions")
        visualize_wordcloud(data)

        # Category frequency bar chart (fake category for now, since actual category extraction needs more parsing)
        st.subheader("App Price Distribution")
        st.write("The Play Store API doesn't provide direct price data, so this is a placeholder visualization.")
        st.bar_chart([1, 2, 3, 4])  # Replace with actual logic later for pricing data
    else:
        st.write("No data found for this keyword.")
