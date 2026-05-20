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


def scrape_html_page(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    for tag in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header"
    ]):
        tag.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return text[:8000]


def scrape_page_text(url):

    source_type = detect_source_type(url)

    print(f"Detected source type: {source_type}")

    if source_type == "pdf":
        return ""

    return scrape_html_page(url)
