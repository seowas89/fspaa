import streamlit as st

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

    # Get user input for the number of Google results with the keyword in the title
    google_results = st.number_input(
        f"Enter the number of Google results for '{keyword}' with the keyword in the title:",
        min_value=0,
        step=1
    )

    # Get user input for the monthly search volume of the keyword
    search_volume = st.number_input(
        f"Enter the monthly search volume for '{keyword}':",
        min_value=0,
        step=1
    )

    # Ensure that we have both inputs before proceeding
    if keyword and google_results > 0 and search_volume > 0:
        # Calculate KGR
        kgr = calculate_kgr(google_results, search_volume)

        if kgr is not None:
            st.write(f"Calculated KGR for '{keyword}': {kgr:.4f}")

            # Interpret the KGR
            interpretation = interpret_kgr(kgr)
            st.write(f"Interpretation: {interpretation}")

if __name__ == '__main__':
    main()
