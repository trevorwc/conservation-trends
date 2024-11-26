# import asyncio
# import aiohttp
# from bs4 import BeautifulSoup
# import json

# BASE_URL = 'https://www.ecolex.org/result/?xlanguage=English&type=legislation&xdate_max=2024&xdate_min=2013'

# # Initialize counters
# total_articles = 0
# articles_with_abstracts = 0
# articles_without_abstracts = 0
# articles_data = []

# async def fetch_detail_page(session, article_url):
#     """Fetches the abstract from the detail page of an article asynchronously."""
#     try:
#         async with session.get(article_url, timeout=10) as response:
#             html_content = await response.text()
#             soup = BeautifulSoup(html_content, 'html.parser')

#             # Extract abstract from <section id="text">
#             text_section = soup.find('section', id='text')
#             if text_section:
#                 abstract_dt = text_section.find('dt', string='Abstract')
#                 if abstract_dt:
#                     abstract_dd = abstract_dt.find_next_sibling('dd')
#                     if abstract_dd:
#                         abstract_p = abstract_dd.find('p', class_='abstract')
#                         abstract = abstract_p.text.strip() if abstract_p else None
#                         return abstract
#         return None
#     except Exception:
#         return None

# async def fetch_page(session, page_number):
#     page_url = f"{BASE_URL}&page={page_number}"
#     try:
#         print(f"Fetching page {page_number}...")
#         async with session.get(page_url, timeout=10) as response:
#             if response.status != 200:
#                 print(f"Page {page_number} returned status {response.status}")
#                 return []
#             html_content = await response.text()
#             soup = BeautifulSoup(html_content, 'html.parser')
#             articles = soup.find_all('li', class_='search-result')

#             page_data = []
#             for article in articles:
#                 title_element = article.find('h3', class_='search-result-title')
#                 link = title_element.find('a', href=True) if title_element else None
#                 article_url = f"https://www.ecolex.org{link['href']}" if link else None

#                 date_elements = article.find_all('span', class_='sr-date sr-help')
#                 original_date = date_elements[0].text.strip() if date_elements else None
#                 consolidation_date = date_elements[1].text.strip('()') if len(date_elements) > 1 else None
#                 publication_date = consolidation_date if consolidation_date else original_date

#                 if article_url:
#                     page_data.append({"url": article_url, "date": publication_date})
#             print(f"Page {page_number}: {len(page_data)} articles found")
#             return page_data
#     except Exception as e:
#         print(f"Error fetching page {page_number}: {e}")
#         return []


# async def process_pages(total_pages):
#     """Processes all pages to extract article links, abstracts, and dates."""
#     global total_articles, articles_with_abstracts, articles_without_abstracts, articles_data

#     async with aiohttp.ClientSession() as session:
#         # Fetch all pages concurrently
#         page_tasks = [fetch_page(session, page) for page in range(1, total_pages + 1)]
#         all_page_data = await asyncio.gather(*page_tasks)

#         # Flatten the list of articles across all pages
#         articles = [item for sublist in all_page_data for item in sublist]
#         total_articles = len(articles)

#         # Fetch all abstracts concurrently
#         detail_tasks = [
#             fetch_detail_page(session, article["url"])
#             for article in articles
#         ]
#         detail_results = await asyncio.gather(*detail_tasks)

#         # Collect results
#         for article, abstract in zip(articles, detail_results):
#             if abstract:
#                 articles_with_abstracts += 1
#                 articles_data.append({
#                     "url": article["url"],
#                     "date": article["date"],
#                     "abstract": abstract
#                 })
#             else:
#                 articles_without_abstracts += 1

# # Main entry point
# async def main():
#     global total_articles, articles_with_abstracts, articles_without_abstracts, articles_data

#     total_pages = 1026 # Update as needed
#     await process_pages(total_pages)

#     # Save the filtered data to JSON
#     data = {
#         "total_articles": total_articles,
#         "articles_with_abstracts": articles_with_abstracts,
#         "articles_without_abstracts": articles_without_abstracts,
#         "articles": articles_data
#     }

#     with open('ecolex_filtered_articles_with_dates.json', 'w') as f:
#         json.dump(data, f, indent=4)

#     # Output final statistics
#     print(f"Data saved to ecolex_filtered_articles_with_dates.json")
#     print(f"Total articles retrieved: {total_articles}")
#     print(f"Articles with abstracts: {articles_with_abstracts}")
#     print(f"Articles excluded (no abstracts): {articles_without_abstracts}")

# # Run the script
# if __name__ == "__main__":
#     asyncio.run(main())
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://www.ecolex.org/result/?xlanguage=English&type=legislation&xdate_max=2024&xdate_min=2013'

# Initialize counters
total_articles = 0
articles_with_abstracts = 0
articles_without_abstracts = 0
articles_data = []
failed_requests = []


async def fetch_page(session, page_number):
    """Fetches articles, links, and publication dates for a specific page asynchronously."""
    page_url = f"{BASE_URL}&page={page_number}"
    try:
        async with session.get(page_url, timeout=30) as response:
            if response.status != 200:
                failed_requests.append(page_url)
                return []
            html_content = await response.text()
            soup = BeautifulSoup(html_content, 'html.parser')

            articles = soup.find_all('li', class_='search-result')
            page_data = []

            for article in articles:
                title_element = article.find('h3', class_='search-result-title')
                link = title_element.find('a', href=True) if title_element else None
                article_url = f"https://www.ecolex.org{link['href']}" if link else None

                # Extract publication date
                date_elements = article.find_all('span', class_='sr-date sr-help')
                original_date = date_elements[0].text.strip() if date_elements else None
                consolidation_date = date_elements[1].text.strip('()') if len(date_elements) > 1 else None
                publication_date = consolidation_date if consolidation_date else original_date

                if article_url:
                    page_data.append({
                        "url": article_url,
                        "date": publication_date
                    })
            return page_data
    except Exception as e:
        failed_requests.append(page_url)
        return []


async def fetch_detail_page(session, article_url):
    """Fetches the abstract from the detail page of an article asynchronously."""
    try:
        async with session.get(article_url, timeout=30) as response:
            if response.status != 200:
                failed_requests.append(article_url)
                return None
            html_content = await response.text()
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract abstract from <section id="text">
            text_section = soup.find('section', id='text')
            if text_section:
                abstract_dt = text_section.find('dt', string='Abstract')
                if abstract_dt:
                    abstract_dd = abstract_dt.find_next_sibling('dd')
                    if abstract_dd:
                        abstract_p = abstract_dd.find('p', class_='abstract')
                        abstract = abstract_p.text.strip() if abstract_p else None
                        return abstract
        return None
    except Exception:
        failed_requests.append(article_url)
        return None


async def fetch_with_retry(fetch_func, max_retries, *args, **kwargs):
    """Retries fetching data up to a maximum number of retries."""
    for attempt in range(max_retries):
        result = await fetch_func(*args, **kwargs)
        if result is not None:
            return result
        await asyncio.sleep(2)  # Delay before retrying
    return None


async def process_pages(total_pages):
    """Processes all pages to extract article links, abstracts, and dates."""
    global total_articles, articles_with_abstracts, articles_without_abstracts, articles_data

    async with aiohttp.ClientSession() as session:
        # Limit concurrency to avoid server overload
        semaphore = asyncio.Semaphore(10)

        async def limited_fetch(page):
            async with semaphore:
                return await fetch_with_retry(fetch_page, 3, session, page)

        # Fetch all pages with limited concurrency
        page_tasks = [limited_fetch(page) for page in range(1, total_pages + 1)]
        all_page_data = await asyncio.gather(*page_tasks)

        # Flatten the list of articles across all pages
        articles = [item for sublist in all_page_data for item in sublist]
        articles = list({article["url"]: article for article in articles}.values())  # Remove duplicates
        total_articles = len(articles)

        # Fetch all abstracts concurrently
        detail_tasks = [
            fetch_with_retry(fetch_detail_page, 3, session, article["url"])
            for article in articles
        ]
        detail_results = await asyncio.gather(*detail_tasks)

        # Collect results
        for article, abstract in zip(articles, detail_results):
            if abstract:
                articles_with_abstracts += 1
                articles_data.append({
                    "url": article["url"],
                    "date": article["date"],
                    "abstract": abstract
                })
            else:
                articles_without_abstracts += 1


# Main entry point
async def main():
    global total_articles, articles_with_abstracts, articles_without_abstracts, articles_data

    total_pages = 1026  # Adjust as needed
    await process_pages(total_pages)

    # Save the filtered data to JSON
    data = {
        "total_articles": total_articles,
        "articles_with_abstracts": articles_with_abstracts,
        "articles_without_abstracts": articles_without_abstracts,
        "articles": articles_data
    }

    with open('ecolex_filtered_articles_with_dates.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Save failed requests for debugging
    with open('failed_requests.json', 'w') as f:
        json.dump(failed_requests, f, indent=4)

    # Output final statistics
    print(f"Data saved to ecolex_filtered_articles_with_dates.json")
    print(f"Total articles retrieved: {total_articles}")
    print(f"Articles with abstracts: {articles_with_abstracts}")
    print(f"Articles excluded (no abstracts): {articles_without_abstracts}")
    print(f"Failed requests saved to failed_requests.json")


# Run the script
if __name__ == "__main__":
    asyncio.run(main())

