# Marketplace Scraper

A simple Flask web application for scraping products from **Amazon.nl**, **eBay.nl** and **Marktplaats.nl**. Provides
a division into new and used products and returns results in table format.

## Installing

    python -m venv env
    source env/bin/activate
    pip install -e .
    export FLASK_ENV=development
    flask run

- http://localhost:5000

### Saving results to SQL database

- Add `.env` file with your db setup corresponding to Settings class format from `config.py`.
- In `main.py` to `run_search()` function add parameter `add_to_database = True`.

## Running with uWSGI

Run

    uwsgi app.ini

- http://localhost:8080
