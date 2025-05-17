import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from datetime import datetime
import asyncio
from bs4 import BeautifulSoup
import markdown

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment
FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')

# Ensure the API key is loaded correctly
if not FIRECRAWL_API_KEY:
    raise ValueError("Firecrawl API key is not set in the .env file.")

# Initialize FirecrawlApp with the API key
app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# Load the CSV file with URLs
df = pd.read_csv('C:/Users/hp/Desktop/Combiner/Safety_Data_Collection.csv')  # Assuming the CSV file has a column named 'URL'
df.columns = df.columns.str.strip()  # Clean column names in case of spaces
urls = df['URL'].tolist()  # Extract the list of URLs

# Function to clean and structure HTML content
def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unnecessary tags (e.g., img, links)
    for tag in soup.find_all(['a', 'img', 'script', 'style']):
        tag.decompose()

    # Get the clean text
    clean_text = soup.get_text(separator=' ', strip=True)
    return clean_text

# Function to clean and structure Markdown content
def clean_markdown(markdown_content):
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content)
    # Clean HTML content
    clean_text = clean_html(html_content)
    return clean_text

# Asynchronous function to scrape a single URL using Firecrawl
async def async_scrape(url):
    try:
        # Scrape the URL and get the result in markdown and html format
        scrape_result = app.scrape_url(url, formats=['markdown', 'html'])

        # Clean and structure both markdown and html
        markdown_cleaned = clean_markdown(scrape_result.markdown)
        html_cleaned = clean_html(scrape_result.html)

        # Return the cleaned and structured content
        result_data = {
            'url': url,
            'markdown': markdown_cleaned,  # Cleaned markdown content
            'html': html_cleaned           # Cleaned HTML content
        }
        return result_data
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Function to process URLs in batches and save results
async def process_urls():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    batch_results = []
    
    for i, url in enumerate(urls):
        print(f"Scraping URL {i+1}/{len(urls)}: {url}")
        
        # Scrape the URL asynchronously
        scrape_result = await async_scrape(url)
        
        # If scraping was successful, append the result
        if scrape_result:
            batch_results.append(scrape_result)

        # Save data after every scrape (or after every batch, depending on your needs)
        with open(f"scrape_results_{timestamp}.json", 'w') as json_file:
            json.dump(batch_results, json_file, indent=4)

        # Sleep for 20 seconds to maintain the rate limit (3 URLs per minute)
        if (i + 1) % 3 == 0:
            print(f"Rate limit reached. Sleeping for 20 seconds...")
            time.sleep(20)
    
    print(f"Scraping completed. Results saved in scrape_results_{timestamp}.json.")

# Main function to run the scraper
async def main():
    await process_urls()

# Run the scraper
if __name__ == '__main__':
    asyncio.run(main())
