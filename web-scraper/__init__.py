from jumia import scrape_product_data
import sys
import asyncio

if __name__ == '__main__':
    # Extract command-line arguments
    if len(sys.argv) < 3:
        print('Usage: python -m package_name url search_text')
        sys.exit(1)

    url = sys.argv[1]
    search_text = sys.argv[2]
    endpoint = sys.argv[3]

    # Run the scraper asynchronously
    asyncio.run(scrape_product_data(url, search_text))