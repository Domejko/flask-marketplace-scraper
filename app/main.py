import functools
import operator

import app.amazon_scrape
import app.ebay_scrape
import app.marktplaats_scrape
from app.engine import SearchEngine


def run_search(query: str, item_condition: int = 0) -> list[dict]:
    """
    Description:
        This function is used to run a search query on multiple online marketplaces. It takes a query string and an
        optional item_condition parameter as input and returns a list of dictionaries containing the search results.

    Parameters:
        query: A string representing the search query.
        item_condition: An integer representing the condition of the items to be searched. Default value is 0.
                        Valid values are 0, 1, and 2. If item_condition is not provided or is 0, it will be considered
                        as new condition.
                        If it is 1, it will be considered as used items only. If it is 2, it will be considered as used
                        and new items.

    Returns:
        A list of dictionaries representing the search results. Each dictionary contains information about a specific
        product found during the search. The dictionaries may contain the following keys:
            'Item': A string representing the title or name of the product.

            'Price': A float representing the price of the product.

            'Link': A string representing auction link to the given item.

            'Img': A string representing img link to the auction thumbnail.

    Example Usage:
        search_results = run_search("iPhone", 1)

        print(search_results)

    Output:
        [{'Item': 'iPhone 11', 'Price': 699.99, 'Link': 'https://marktplaats.nl/iPhone',
        'Img': 'https://marktplaats.nl/iPhone.jpg'},

        {'Item': 'iPhone 11 Pro', 'Price': 999.99, 'Link': 'https://eBay.nl/iPhone',
        'Img': 'https://eBay.nl/iPhone.jpg'},

        {'Item': 'iPhone XR', 'Price': 599.99, 'Link': 'https://Amazon.nl/iPhone', 'Img': 'Amazon.nl/iPhone.jpg'}]
    """
    if item_condition != 0:
        item_condition -= 1

    mk = app.marktplaats_scrape.marktplaats(item_condition)
    eb = app.ebay_scrape.ebay(item_condition)
    am = app.amazon_scrape.amazon(item_condition)

    products_found = [mk.search(mk.main_page_scrape, query),
                      eb.search(eb.main_page_scrape, query),
                      am.search(am.page_scrape, query) if item_condition in [1, 2]
                      else am.search(am.main_page_scrape, query)]

    try:
        search_result = functools.reduce(operator.iconcat, products_found, [])
        search_result = sorted(search_result, key=operator.itemgetter('Price'), reverse=True)
    except KeyError:
        return products_found[0]

    return search_result
