import requests
from bs4 import BeautifulSoup
from googlesearch import search
import openai  # Requires OpenAI API Key

# OpenAI API Key (Replace with your own key)
openai.api_key = "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"

def get_featured_snippet(keyword):
    # Use Google search results to find the featured snippet
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?q={keyword}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the featured snippet content
    snippet = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")
    return snippet.text if snippet else "No featured snippet found."

def get_competitor_content(keyword):
    # Use the googlesearch library to fetch URLs for competitors
    competitor_urls = list(search(keyword, num_results=5))
    competitor_content = []

    headers = {"User-Agent": "Mozilla/5.0"}
    for url in competitor_urls:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = ' '.join([p.text for p in soup.find_all('p')[:5]])  # Extract first 5 paragraphs
            competitor_content.append({"url": url, "content": text})
        except Exception as e:
            print(f"Error fetching competitor content from {url}: {e}")

    return competitor_content

def get_people_also_ask(keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?q={keyword}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    paa_questions = []
    for question in soup.find_all("div", class_="related-question-pair"):  # Look for PAA div
        paa_questions.append(question.text)

    return paa_questions

def generate_suggestions(snippet, competitor_content, paa_questions, user_content):
    # Combine all the data for context
    prompt = f"Keyword: {keyword}\n" \
             f"Featured Snippet: {snippet}\n" \
             f"Competitor Content: {competitor_content}\n" \
             f"People Also Ask: {paa_questions}\n" \
             f"Your Content: {user_content}\n" \
             "\nSuggest SEO-optimized content to win the featured snippet and answer the PAA questions."

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error generating suggestions: {e}"

if __name__ == "__main__":
    keyword = input("Enter the keyword: ")
    user_content = input("Enter your content: ")

    print("Fetching featured snippet...")
    featured_snippet = get_featured_snippet(keyword)

    print("Fetching competitor content...")
    competitors = get_competitor_content(keyword)

    print("Fetching People Also Ask questions...")
    paa_questions = get_people_also_ask(keyword)

    print("Generating suggestions...")
    suggestions = generate_suggestions(featured_snippet, competitors, paa_questions, user_content)

    print("\nSuggestions:\n", suggestions)
