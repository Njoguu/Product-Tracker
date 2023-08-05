from jumia import main
import sys
import asyncio

if __name__ == '__main__':
    # Extract command-line arguments
    if len(sys.argv) < 2:
        print('Usage: python -m package_name url search_text')
        sys.exit(1)

    url = sys.argv[1]
    search_text = sys.argv[2]

    # Run the scraper asynchronously
    asyncio.run(main(url, search_text))
