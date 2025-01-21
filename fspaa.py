import requests
import streamlit as st

# Function to fetch the number of Google results with the keyword in the title using SerpApi
def get_google_results(keyword, api_key):
    url = f"https://serpapi.com/search?q={keyword}&api_key={api_key}&hl=en"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Get the number of results
        total_results = data.get("search_information", {}).get("total_results", 0)
        return int(total_results)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Google results: {e}")
        return 0

# Function to fetch the search volume for the keyword using SerpApi
def get_search_volume(keyword, api_key):
    url = f"https://serpapi.com/search?q={keyword}&api_key={api_key}&hl=en"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Get the search volume from the structured data (This will depend on how SerpApi structures the data)
        search_volume = data.get("organic_results", [{}])[0].get("search_volume", 0)  # Example for extracting volume from data
        return int(search_volume)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching search volume: {e}")
        return 0

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
    api_key = '4a076b94b88e3541df371407c65d4b4628da2d2db43576e0667d50a35d5e395'

    if keyword:
        # Fetch the number of Google results with the keyword in the title
        st.write(f"Fetching Google results for the keyword: {keyword}...")
        google_results = get_google_results(keyword, api_key)

        # Fetch the search volume for the keyword
        st.write(f"Fetching search volume for the keyword: {keyword}...")
        search_volume = get_search_volume(keyword, api_key)

        if google_results > 0 and search_volume > 0:
            st.write(f"Number of Google results for '{keyword}' with the keyword in the title: {google_results}")
            st.write(f"Search volume for '{keyword}': {search_volume}")

            # Calculate KGR
            kgr = calculate_kgr(google_results, search_volume)

            if kgr is not None:
                st.write(f"Calculated KGR for '{keyword}': {kgr:.4f}")

                # Interpret the KGR
                interpretation = interpret_kgr(kgr)
                st.write(f"Interpretation: {interpretation}")
        else:
            st.write("Could not fetch the required data. Please check your keyword or API key.")

if __name__ == '__main__':
    main()
