# Marketplace Scraper

A simple Flask web application for scraping products from **Amazon.nl**, **eBay.nl** and **Marktplaats.nl**. Provides
a division into used and used products and returns date in table format.

## Installing

    python -m venv env
    source env/bin/activate
    pip install -e .
    export FLASK_ENV=development
    flask run

- http://localhost:5000

## Running with uWSGI

Run

    uwsgi app.ini

- http://localhost:8080
