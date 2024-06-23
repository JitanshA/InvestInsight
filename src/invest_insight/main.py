import os
import json
import requests
from dotenv import load_dotenv
from newspaper import Article
import yfinance as yf
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Access the API key and endpoint from environment variables
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_SEARCH_ARTICLE_ENDPOINT = os.getenv('NEWS_API_SEARCH_ARTICLE_ENDPOINT')

# Request headers for News API
NEWS_API_REQ_HEADERS = {
    'X-Api-Key': NEWS_API_KEY
}

# List of company names to search for
COMPANIES_NAMES = [
    # "+NVIDIA",
    # "+Vanguard",
    "+Blackrock"
]

# Define the ticker symbol
COMPANIES_TICKER_SYMBOLS = [
    "BLK"
]

# Define the time period
DATA_START_DATE = '2010-01-01'
DATA_END_DATE = '2023-06-01'


def create_directory_if_not_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def sanitize_filename(filename):
    """Sanitize the filename to remove invalid characters."""
    return "".join(c for c in filename if c.isalnum() or c in (' ', '_')).rstrip()


def save_content_to_text_file(content_text, directory, filename):
    """Save content to a text file."""
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content_text)
    print(f"Content saved to {filepath}")


def fetch_and_save_article_content(url, company_name=''):
    """Fetch article content from URL and save to file."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        content_text = article.text.strip()

        if content_text:
            directory = f'articles_fetched/{company_name[1:]}'
            create_directory_if_not_exists(directory)
            filename = sanitize_filename(os.path.basename(url)) + '.txt'
            save_content_to_text_file(content_text, directory, filename)
        else:
            print(f"No content found for {url}")

    except Exception as e:
        print(f"Error fetching {url}: {e}")


def make_api_request(company_name):
    """Make API request to fetch articles for a company."""
    try:
        req_params = {
            'q': company_name + ' AND stocks',
            'searchIn': 'content',
            'language': 'en',
            'sortBy': 'relevancy',
        }

        response = requests.get(url=NEWS_API_SEARCH_ARTICLE_ENDPOINT,
                                headers=NEWS_API_REQ_HEADERS,
                                params=req_params)

        if response.ok:
            log_api_success_response(response, company_name)
        else:
            log_api_error_response(response, company_name)

    except requests.RequestException as e:
        print(f"Request failed for {company_name}: {e}")


def log_api_success_response(response, company_name):
    """Log successful API response and fetch articles."""
    filename = f'response_logs_articles/{company_name[1:]}.json'
    save_json_response_to_file(response, filename)
    response_data = response.json()

    for article in response_data.get('articles', []):
        fetch_and_save_article_content(article['url'], company_name)


def log_api_error_response(response, company_name):
    """Log error API response."""
    filename = f'response_logs_articles/{company_name[1:]}-error-log.json'
    save_json_response_to_file(response, filename)


def save_json_response_to_file(response, filename):
    """Save API response JSON to file."""
    directory = os.path.dirname(filename)
    create_directory_if_not_exists(directory)

    with open(filename, 'w') as file:
        json.dump(response.json(), file, indent=4)


def fetch_and_save_historical_data(ticker_symbol):
    ticker_data = yf.Ticker(ticker_symbol)

    # Fetch the historical data
    historical_data = ticker_data.history(start=DATA_START_DATE, end=DATA_END_DATE)

    create_directory_if_not_exists("historical_data")

    # Define the filename for the text file
    csv_filename = "historical_data/" + ticker_symbol + ".csv"

    # Save DataFrame to a CSV file (which can be renamed to .txt if needed)
    historical_data.to_csv(csv_filename, sep='\t', index=True, header=True)


def main():
    """Main function to orchestrate API calls for each company."""
    # for company_name in COMPANIES_NAMES:
    #     make_api_request(company_name)

    for ticker_symbol in COMPANIES_TICKER_SYMBOLS:
        fetch_and_save_historical_data(ticker_symbol)


if __name__ == "__main__":
    main()
