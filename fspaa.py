import requests
import streamlit as st

# Function to fetch the number of Google results with keyword in the title using SerpApi
def get_google_results(keyword, api_key):
    url = f"https://serpapi.com/search?q={keyword}&api_key={api_key}&hl=en"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Check for the number of results (can be adjusted based on the API's response structure)
        total_results = data.get("search_information", {}).get("total_results", 0)

        return int(total_results)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Google results: {e}")
        return 0

# Function to simulate getting search volume for the keyword (in a real scenario, use an API like Google Keyword Planner or Ahrefs)
def get_search_volume(keyword):
    # In this example, we'll assume a dummy search volume of 1000 for any keyword
    # Replace this with a real search volume API call in a real-world app.
    return 1000

# Function to calculate KGR (Keyword Golden Ratio)
def calculate_kgr(google_results, search_volume):
    if search_volume == 0:
        st.error("Search volume cannot be zero!")
        return None
    kgr = google_results / search_volume
    return kgr

# Function to interpret the KGR value
def interpret_kgr(kgr):
    if kgr < 0.25:
        return "Great opportunity to rank! (KGR < 0.25)"
    elif 0.25 <= kgr < 1.0:
        return "Moderate competition, still worth targeting."
    else:
        return "Too competitive, not recommended."

# Main function to run the Streamlit app
def main():
    st.title('Keyword Golden Ratio (KGR) Calculator')

    # Get user input for the keyword
    keyword = st.text_input("Enter the keyword to analyze:")

    # Define your SerpApi key (replace with your actual API key)
    api_key = 'YOUR_SERPAPI_KEY'

    if keyword:
        # Fetch the number of Google results with the keyword in the title
        st.write(f"Fetching Google results for the keyword: {keyword}...")
        google_results = get_google_results(keyword, api_key)

        # Fetch the monthly search volume for the keyword
        search_volume = get_search_volume(keyword)

        # Display the results
        st.write(f"Number of Google results for '{keyword}' with the keyword in the title: {google_results}")
        st.write(f"Assumed monthly search volume for '{keyword}': {search_volume}")

        # Calculate KGR
        kgr = calculate_kgr(google_results, search_volume)

        if kgr is not None:
            st.write(f"Calculated KGR for '{keyword}': {kgr:.4f}")

            # Interpret the KGR
            interpretation = interpret_kgr(kgr)
            st.write(f"Interpretation: {interpretation}")

if __name__ == '__main__':
    main()
