# OK- so we have a problem with the website being blocked

# === Import Statements =======
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time

# === Define Global Variables =======
GCB_ISSUE_ARCHIVE = "https://onlinelibrary.wiley.com/loi/13652486"
BASE_URL = "https://onlinelibrary.wiley.com/"
YEARS = list(range(2013, 2024))

# Comprehensive headers to mimic real browser behavior
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://onlinelibrary.wiley.com/',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1'  # Do Not Track
}
CRAWL_DELAY = 1  # Respect the crawl-delay directive

# === Helper Functions =======
def extract_links(html_content):
    """Extract article links from the issue archive."""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        articles = set()

        for a_tag in soup.find_all('a', class_='issue-item__title visitable', href=True):
            href = a_tag["href"]
            if not any(disallowed in href for disallowed in ["/action", "/doi/metrics/", "/search"]):
                article_url = urljoin(BASE_URL, href)
                articles.add(article_url)

        return articles

    except Exception as e:
        print(f"Error parsing HTML content: {e}")
        return set()

def crawl(session, url, visited):
    """Recursively crawl and visit links."""
    if url in visited:
        return
    visited.add(url)
    print(f"Visiting: {url}")

    try:
        response = session.get(url)
        response.raise_for_status()
        html_content = response.text

        time.sleep(CRAWL_DELAY)  # Respect crawl-delay
        links = extract_links(html_content)

        for link in links:
            crawl(session, link, visited)

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

def links(session, start_url):
    """Start crawling from the given URL."""
    visited = set()
    crawl(session, start_url, visited)
    return visited

def parse_content(session, links, year):
    """Parse content from article links."""
    abstracts = []

    for link in links:
        try:
            time.sleep(CRAWL_DELAY)  # Respect crawl-delay
            response = session.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.find('h1', class_='citation__title').get_text(strip=True)
            publication_date = soup.find('span', class_='epub-date').get_text(strip=True)

            div_content = soup.find("div", class_="abstract-group  metis-abstract")
            ab = div_content.find("p") if div_content else None
            abstract = ab.get_text(strip=True) if ab else "No abstract available"

            abstracts.append({
                'Title': title,
                'Publication_Date': publication_date,
                'Publication Year': year,
                'Abstract': abstract
            })

        except (requests.RequestException, AttributeError) as e:
            print(f"Error processing {link}: {e}")

    return abstracts

# === Main =======
def main():
    all_content = []

    # Use a single session for all requests
    session = requests.Session()
    session.headers.update(HEADERS)

    for year in YEARS:
        start_url = f"{GCB_ISSUE_ARCHIVE}/{year}"
        visited_links = links(session, start_url)
        yearly_content = parse_content(session, visited_links, year)
        all_content.extend(yearly_content)

    return all_content

# === Entry Point =======
if __name__ == "__main__":
    all_content = main()  # Capture the returned content

    # Save the data to a JSON file
    with open('1_gcb_abstracts.json', 'w') as json_file:
        json.dump(all_content, json_file, indent=4)
