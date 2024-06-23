import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Access the API key
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_SEARCH_ARTICLE_ENDPOINT = os.getenv('NEWS_API_SEARCH_ARTICLE_ENDPOINT')

NEWS_API_REQ_HEADERS = {
    'X-Api-Key': NEWS_API_KEY
}

TECH_COMPANIES_NAMES = [
    "+Apple",
    # "+Microsoft",
    # "+Alphabet",
    # "+Amazon.com",
    # "+Tesla",
    # "+NVIDIA",
    # "+Intel",
    # "+Adobe",
    # "+Cisco Systems"
]


def get_company_request_params(company_name):
    return {
        'q': company_name + ' AND stocks',
        'searchIn': 'title',
        'language': 'en',
        'sortBy': 'popularity',
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


def make_api_call_for_each_company(company_name):
    req_params = get_company_request_params(company_name)

    response = requests.get(url=NEWS_API_SEARCH_ARTICLE_ENDPOINT,
                            headers=NEWS_API_REQ_HEADERS,
                            params=req_params)

    log_api_response_result(response)


for company_name in TECH_COMPANIES_NAMES:
    make_api_call_for_each_company(company_name)



