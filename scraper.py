import requests
from bs4 import BeautifulSoup

def detect_source_type(url):

    if url.endswith(".pdf"):
        return "pdf"

    elif "irs.gov" in url:
        return "federal"

    elif (
        "tampaelectric.com" in url
        or "duke-energy.com" in url
        or "fpl.com" in url
    ):
        return "utility"

    elif (
        "tampa.gov" in url
        or "hillsboroughcounty.org" in url
        or "floridahousing.org" in url
    ):
        return "government"

    elif "floridapace.gov" in url:
        return "pace"

    else:
        return "generic"


import trafilatura

def scrape_html_page(url):
    """
    Uses Trafilatura for intelligent main content extraction
    """
    # Fetch and extract main content
    downloaded = trafilatura.fetch_url(url)
    
    if downloaded is None:
        # Fallback to requests if trafilatura fetch fails
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        downloaded = response.text
    
    # Extract main content with structure preserved
    text = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=True,      # Keep tables (often have eligibility info)
        include_links=False,      # Don't need URLs in text
        no_fallback=False,        # Use fallback extraction if needed
        favor_recall=True         # Prioritize getting all content
    )
    
    if text is None:
        return ""
    
    # Increase limit to 16,000 characters (fits in Llama 3.1's context)
    return text[:16000]


def scrape_page_text(url):

    source_type = detect_source_type(url)

    print(f"Detected source type: {source_type}")

    if source_type == "pdf":
        return ""

    return scrape_html_page(url)
