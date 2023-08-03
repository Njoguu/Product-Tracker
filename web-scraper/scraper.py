import os, json
import asyncio
from playwright.async_api import async_playwright
from requests import post
from jumia import get_product as get_jumia_product  


JUMIA = "https://www.jumia.co.ke/"

URLS = {
    JUMIA: {
        "search_field_query": 'input[name="q"]',
        "search_button_query": 'button.btn._prim._md.-mls.-fsh0',
        "product_selector": "article.prd"
    }
}


available_urls = URLS.keys()

def load_auth():
    FILE = os.path.join("web-scraper", "auth.json")
    with open(FILE, "r") as f:
        return json.load(f)
    
# place your bright data credentials in auth.json file with keys: "username", "password" and "host"
cred = load_auth()
auth = f'{cred["username"]}:{cred["password"]}'
browser_url = f'wss://{auth}@{cred["host"]}'


async def search(metadata, page, search_text):
    print(f"Searching for {search_text} on {page.url}")
    search_field_query = metadata.get("search_field_query")
    search_button_query = metadata.get("search_button_query")

    if search_field_query and search_button_query:
        print("Filling input field")
        search_box = await page.wait_for_selector(search_field_query)
        await search_box.type(search_text)
        print("Pressing search button")
        button = await page.wait_for_selector(search_button_query)
        await button.click()
    else:
        raise Exception("Could not search.")

    await page.wait_for_load_state()
    return page

async def get_products(page, search_text, selector, get_product):
    print("Retreiving products.")
    product_divs = await page.query_selector_all(selector)
    valid_products = []
    words = search_text.split(" ")

    async with asyncio.TaskGroup() as tg:
        for div in product_divs:
            async def task(p_div):
                product = await get_product(p_div)

                if not product["price"] or not product["url"]:
                    return

                for word in words:
                    if not product["name"] or word.lower() not in product["name"].lower():
                        break
                else:
                    valid_products.append(product)
            tg.create_task(task(div))

    return valid_products

def save_results(results):
    data = {"results": results}
    FILE = os.path.join("web-scraper", "results.json")
    with open(FILE, "w") as f:
        json.dump(data, f)

def post_results(results, endpoint, search_text, source):
    headers = {
        "Content-Type": "application/json"
    }
    data = {"data": results, "search_text": search_text, "source": source}

    print("Sending request to", endpoint)
    response = post("http://localhost:8000" + endpoint,
                    headers=headers, json=data)
    print("Status code:", response.status_code)

async def main(url, search_text):
    metadata = URLS.get(url)
    if not metadata:
        print("Invalid URL.")
        return

    async with async_playwright() as pw:
        print('Connecting to browser.')
        browser = await pw.chromium.connect_over_cdp(browser_url)
        page = await browser.new_page()
        print("Connected.")
        await page.goto(url, timeout=120000)
        print("Loaded initial page.")
        search_page = await search(metadata, page, search_text)

        def func(x): return None
        if url == JUMIA:
            func = get_jumia_product
        else:
            raise Exception('Invalid URL')

        results = await get_products(search_page, search_text, metadata["product_selector"], func)
        print("Saving results.")
        # post_results(results, response_route, search_text, url)
        save_results(results=results)

        await browser.close()

if __name__ == "__main__":
    # test script
    asyncio.run(main(JUMIA, "ryzen 9 3950x"))
