# Marketplace Scraper

A simple Flask web application for scraping products from **Amazon.nl**, **eBay.nl** and **Marktplaats.nl**. Provides
a division into new and used products and returns results in table format. Search results can be stored in database. 

## Installing

1. Create local venv and activate it:
```commandline
python -m venv env

source env/bin/activate
```
2. Install requirements:
```commandline
pip install -e .
```
3. Create copy of `.env.sample` for your PostgreSQL database (need to have PostgreSQL installed):
```commandline
cp .env.sample .env
```
4. Export environment variable:
```commandline
export FLASK_ENV=development
```
5. Run application:
```commandline
flask run
```

- http://localhost:5000

### Saving results to SQL database

- Add `.env` file with your db setup corresponding to Settings class format from `config.py`.
- In `main.py` to `run_search()` function and set parameter `add_to_database` to `True`.

## Running with uWSGI

Run:
```commandline
uwsgi app.ini
```

- http://localhost:8080
