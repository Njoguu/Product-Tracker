import os, json
from requests import post


JUMIA = "https://www.jumia.co.ke"
AMAZON = "https://amazon.com"

URLS = { 
    JUMIA: {    
        "product_selector": {
            'element': 'article',
            'class': 'prd'
        }
    },
    AMAZON: {
    }
}

def save_results(results):
    data = {"data": results}
    FILE = os.path.join("web-scraper", "scraped_data.json")
    with open(FILE, "w") as f:
        json.dump(data, f)


def post_results(results, source_url, search_text):
    headers = {
        "Content-Type": "application/json"
    }
    data = {"data": results, "search_text": search_text, "source": source_url}

    print("Sending request to", "/results/")
    response = post("http://localhost:8000" + "/results/",
                    headers=headers, json=data)
    print("Status code:", response.status_code)
