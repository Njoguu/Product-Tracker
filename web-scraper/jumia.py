import asyncio
import requests
from bs4 import BeautifulSoup
from scraper import URLS, JUMIA, post_results


async def scrape_product_data(url, product):
    name = product.replace(" ", "+")
    # Send an HTTP GET request to the website
    URL = url+f"/catalog/?q={name}"

    response = requests.get(URL)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: Failed to fetch the website. Status code: {response.status_code}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all product elements on the page (customize this based on the website's structure)
    product_elements = soup.find_all(URLS[JUMIA]["product_selector"]["element"], class_=URLS[JUMIA]["product_selector"]["class"])

    # List to store scraped product data
    products_data = []

    # Loop through each product element and extract product details
    for product_element in product_elements:
        # Extract product details such as name, price, image URL, etc.
        product_name = product_element.find('h3', class_='name').text.strip()
        product_price_raw = product_element.find('div', class_='prc').text.strip()
        product_image_url = product_element.find('img', class_="img")['data-src']
        product_url_element = product_element.find('a', class_="core")
        product_url = product_url_element['href'] if product_url_element else None

        if '-' in product_price_raw:
            product_price_raw= product_price_raw.split('-')[0].strip()
        product_price = product_price_raw.replace("KSh", "").replace(",", "").strip() if product_price_raw else None

        # Create a dictionary with the extracted data and add it to the list
        product_data = {
            'name': product_name,
            'price': product_price,
            'img': product_image_url,
            'url': url+product_url
        }
        products_data.append(product_data)

    return products_data

async def main(url, search_text):
    results = await scrape_product_data(JUMIA, product=search_text)
    post_results(results, JUMIA, search_text)
    

if __name__ == "__main__":
    asyncio.run(main(JUMIA, "ryzen 9 3950x"))
    