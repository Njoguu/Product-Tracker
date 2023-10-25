# Product Tracker

This project provides a user interface to interact with a price tracking web scraper. Currently the tracker scrapes [jumia.co.ke](https://jumia.co.ke), but could be configured to scrape multiple sources.

## Libraries/Frameworks/Modules/Tools

This project uses:

- Nodejs
- Django
- BeautifulSoup
- PostgreSQL

## Using the Scraper

Install all dependencies, start the Django backend, run the node frontend and interact with the tool.

### Setup Python Django Backend

- `pip install -r requirements.txt`
- `cd product_tracker`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`

### Running the Node Frontend

- `cd frontend_sample`
- `node index.js`
