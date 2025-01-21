import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from serpapi import GoogleSearch
from wordcloud import WordCloud

# Function to fetch data from serpapi
def fetch_playstore_data(query):
    params = {
        "q": query,
        "tbm": "isch",  # Using images because Play Store is included in Google Search API
        "engine": "google",
        "api_key": "74a076b94b88e3541df371407c65d4b4628da2d2db43576e0667d50a35d5e395"
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()

    # Extracting the relevant data from the results
    apps_data = []
    for result in results['shopping_results']:
        apps_data.append({
            "App Name": result.get("title"),
            "App URL": result.get("link"),
            "Description": result.get("snippet"),
            "Price": result.get("price"),
            "Category": result.get("category"),
        })

    return pd.DataFrame(apps_data)


# Function to visualize keyword frequency in a word cloud
def visualize_wordcloud(dataframe):
    all_text = " ".join(dataframe['Description'].fillna(''))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

    st.image(wordcloud.to_array(), use_column_width=True)


# Streamlit UI layout
st.title("Google Play Store Keyword Research Tool")

# Input search term (keyword)
query = st.text_input("Enter Keyword to Research", "")

if query:
    st.write(f"Searching for apps related to **{query}**...")

    # Fetch data from the API
    data = fetch_playstore_data(query)
    st.write(f"Found **{len(data)}** apps matching the keyword.")

    # Show data as a table
    st.dataframe(data)

    # Visualizations
    st.subheader("Visualizations")
    
    # Wordcloud visualization
    st.subheader("Word Cloud of App Descriptions")
    visualize_wordcloud(data)

    # Category frequency bar chart
    category_counts = data['Category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']
    st.subheader("Category Frequency Bar Chart")
    fig = px.bar(category_counts, x='Category', y='Count', title="Category Distribution")
    st.plotly_chart(fig)
    
    # App Price distribution
    data['Price'] = data['Price'].apply(lambda x: float(x[1:]) if x != "Free" else 0.0)  # Extracting price values
    st.subheader("App Price Distribution")
    fig = px.histogram(data, x="Price", nbins=20, title="Price Distribution")
    st.plotly_chart(fig)
