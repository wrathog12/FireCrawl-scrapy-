Web Scraping Project Using Firecrawl API
This project uses the Firecrawl API to scrape URLs provided in a CSV file. The scraped content is cleaned (HTML and Markdown) and saved in a structured JSON format.

Prerequisites
To set up and run this project, you will need the following:

Python 3.x installed on your system

A Firecrawl API key

A CSV file containing the URLs you want to scrape

1. Set Up Firecrawl API Key
Go to the Firecrawl API Website and sign up for an account.

Once signed in, navigate to your API Keys section and generate an API key.

Copy your API key, as you’ll need it for the next step.

2. Setting Up the .env File
To securely store your Firecrawl API key, we use the .env file. This file contains sensitive information like your API key.

In your project directory, create a file named .env.

Add the following content to the .env file:

plaintext
Copy
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
Replace your_firecrawl_api_key_here with the actual API key you generated from Firecrawl.

Why use .env?

The .env file keeps sensitive information like API keys out of your codebase. This prevents accidental exposure when sharing or deploying your code.

It also allows you to keep different environment settings for development, testing, and production.

3. Install Required Libraries
In your project directory, create a requirements.txt file with the following content:

plaintext
Copy
firecrawl-py
pandas
requests
python-dotenv
beautifulsoup4
markdown
To install the necessary dependencies, run the following command:

bash
Copy
pip install -r requirements.txt
4. How to Use the Script
Prepare your CSV file (e.g., URLs.csv) containing a column named URL with the URLs you want to scrape.

Run the Python script using the following command:

bash
Copy
python fire1.py
The script will scrape each URL, clean the content, and save the results in a timestamped JSON file (e.g., scrape_results_20230912_103030.json).

5. Understanding the Rate Limit (20 Seconds Between Scrapes)
The script includes a rate limit that ensures no more than 3 URLs are scraped per minute. This is achieved by introducing a time.sleep(20) delay between each batch of 3 URLs.

Why is the 20-second limit set?
Avoiding Overloading Firecrawl API: By limiting the scraping rate to 3 URLs per minute, we ensure that we don't exceed the Firecrawl API rate limits, preventing potential throttling or blocking of requests.

Respecting Server Load: Scraping at a slower pace reduces the load on Firecrawl's servers and ensures fair usage for all users.

Handling Large Data: Scraping large amounts of data in batches helps maintain the quality of the scraped content and ensures that the process remains stable without causing memory or performance issues.

You can modify this rate limit in the script by adjusting the time.sleep(20) value to either reduce or increase the wait time based on your needs.

6. Directory Structure
bash
Copy
/your-project-directory
    ├── .env                # Store your Firecrawl API key here
    ├── fire1.py            # Main Python script to scrape and process URLs
    ├── URLs.csv            # CSV file containing URLs to scrape
    ├── requirements.txt    # List of required dependencies
    └── scrape_results_YYYYMMDD_HHMMSS.json  # Output file with the scraped data
Conclusion
This project allows you to scrape data from URLs in an efficient and controlled manner using the Firecrawl API. By using the rate limiting and structured output, the scraping process is optimized for stability and usability.

If you have any issues or questions, feel free to reach out!
