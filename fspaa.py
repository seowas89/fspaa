import requests
from bs4 import BeautifulSoup
import pytrends
from pytrends.request import TrendReq
import streamlit as st

# Function to fetch the number of Google results by scraping the Google Search page
def get_google_results(keyword):
    search_url = f"https://www.google.com/search?q={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Scrape the number of results from the search results page
        result_stats = soup.find("div", {"id": "result-stats"})
        if result_stats:
            result_text = result_stats.get_text()
            result_count = result_text.split(" ")[1].replace(",", "")
            return int(result_count)
        else:
            st.error("Unable to fetch search results.")
            return 0
    except Exception as e:
        st.error(f"Error fetching Google results: {e}")
        return 0

# Function to fetch relative search interest using pytrends (Google Trends)
def get_search_interest(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')
    
    try:
        interest_over_time = pytrends.interest_over_time()
        if not interest_over_time.empty:
            return interest_over_time[keyword].mean()  # Average interest over the past year
        else:
            st.error("No data available for this keyword.")
            return 0
    except Exception as e:
        st.error(f"Error fetching search interest: {e}")
        return 0

# Function to calculate KGR (Keyword Golden Ratio)
def calculate_kgr(google_results, search_interest):
    if search_interest == 0:
        st.error("Search interest cannot be zero!")
        return None
    kgr = google_results / search_interest
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

    if keyword:
        # Fetch the number of Google results with the keyword
        st.write(f"Fetching Google results for the keyword: {keyword}...")
        google_results = get_google_results(keyword)

        # Fetch the relative search interest (search volume estimate)
        st.write(f"Fetching search interest for the keyword: {keyword}...")
        search_interest = get_search_interest(keyword)

        if google_results > 0 and search_interest > 0:
            st.write(f"Number of Google results for '{keyword}': {google_results}")
            st.write(f"Relative search interest for '{keyword}': {search_interest:.2f}")

            # Calculate KGR
            kgr = calculate_kgr(google_results, search_interest)

            if kgr is not None:
                st.write(f"Calculated KGR for '{keyword}': {kgr:.4f}")

                # Interpret the KGR
                interpretation = interpret_kgr(kgr)
                st.write(f"Interpretation: {interpretation}")
        else:
            st.write("Could not fetch the required data. Please check your keyword.")

if __name__ == '__main__':
    main()
