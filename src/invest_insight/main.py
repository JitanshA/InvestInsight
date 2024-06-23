import requests
import os
from dotenv import load_dotenv
import json
from newspaper import Article


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
    # "+Vanguard",
    "+Blackrock"
]


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def sanitize_filename(filename):
    # Sanitize the filename to remove invalid characters
    return "".join(c for c in filename if c.isalnum() or c in (' ', '_')).rstrip()


def fetch_article_content(url, company_name=''):
    try:
        # Download and parse the article
        article = Article(url)
        article.download()
        article.parse()

        # Extract the article content
        content_text = article.text

        if content_text:
            # Create the directory if it doesn't exist
            create_directory(f'articles_fetched/{company_name}')
            # Create a sanitized filename
            filename = sanitize_filename(url) + '.txt'
            filepath = os.path.join(f'articles_fetched/{company_name}', filename)
            # Write the content to a new text file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content_text)
            print(f"Content saved to {filepath}")
        else:
            print(f"No content found for {url}")

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_company_request_params(company_name):
    return {
        'q': company_name + ' AND stocks',
        'searchIn': 'content',
        'language': 'en',
        'sortBy': 'relevancy',
    }


def log_api_response_result(response, company_name):
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
            fetch_article_content(article['url'], company_name)


def make_api_call_for_each_company(company_name):
    req_params = get_company_request_params(company_name)

    response = requests.get(url=NEWS_API_SEARCH_ARTICLE_ENDPOINT,
                            headers=NEWS_API_REQ_HEADERS,
                            params=req_params)

    log_api_response_result(response, company_name)


for company_name in COMPANIES_NAMES:
    make_api_call_for_each_company(company_name)

