import requests
import os
from dotenv import load_dotenv
import json
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Access the API key
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_SEARCH_ARTICLE_ENDPOINT = os.getenv('NEWS_API_SEARCH_ARTICLE_ENDPOINT')

NEWS_API_REQ_HEADERS = {
    'X-Api-Key': NEWS_API_KEY
}

COMPANIES_NAMES = [
    # "+NVIDIA",
    "+Vanguard",
    "+Blackrock"
]


def fetch_article_content(url):
    def create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def sanitize_filename(filename):
        # Sanitize the filename to remove invalid characters
        return "".join(c for c in filename if c.isalnum() or c in (' ', '_')).rstrip()

    try:
        # Make a request to each article URL
        article_response = requests.get(url)
        soup = BeautifulSoup(article_response.content, 'html.parser')
        article_content = soup.find('article')

        if article_content:
            content_text = article_content.get_text()
            # Create the directory if it doesn't exist
            create_directory('articles_fetched')
            # Create a sanitized filename
            filename = sanitize_filename(url) + '.txt'
            filepath = os.path.join('articles_fetched', filename)
            # Write the content to a new text file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content_text)
            print(f"Content saved to {filepath}")
        else:
            print(f"No content found for {url}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_company_request_params(company_name):
    return {
        'q': company_name + ' AND stocks',
        'searchIn': 'content',
        'language': 'en',
        'sortBy': 'relevancy',
    }


def log_api_response_result(response):
    if not response.ok:
        error_filename = 'response_logs_articles/' + company_name[1:] + '-error-log.json'
        with open(error_filename, 'w') as f:
            json.dump(response.json(), f, indent=4)
    else:
        filename = 'response_logs_articles/' + company_name[1:] + '.json'
        with open(filename, 'w') as f:
            json.dump(response.json(), f, indent=4)

        response_json = response.json()
        for article in response_json['articles']:
            fetch_article_content(article['url'])


def make_api_call_for_each_company(company_name):
    req_params = get_company_request_params(company_name)

    response = requests.get(url=NEWS_API_SEARCH_ARTICLE_ENDPOINT,
                            headers=NEWS_API_REQ_HEADERS,
                            params=req_params)

    log_api_response_result(response)


for company_name in COMPANIES_NAMES:
    make_api_call_for_each_company(company_name)



