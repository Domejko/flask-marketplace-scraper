import operator
import queue
import threading

import app.amazon_scrape
import app.ebay_scrape
import app.marktplaats_scrape


def search_and_append_result(search_func, result_list, *args, **kwargs):
    result = search_func(*args, **kwargs)
    result_list.extend(result)


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
    num_threads = 3
    threads = []
    search_results = []

    if item_condition != 0:
        item_condition -= 1

    mk = app.marktplaats_scrape.marktplaats(item_condition)
    eb = app.ebay_scrape.ebay(item_condition)
    am = app.amazon_scrape.amazon(item_condition)

    search_queue = queue.Queue()
    for marketplace, search_func in zip([mk, eb, am], [mk.search, eb.search, am.search]):
        search_queue.put((search_func, search_results,
                          marketplace, query))

    for _ in range(num_threads):
        func, results, marketplace, query = search_queue.get()

        if marketplace == am and item_condition in [1, 2]:
            scraper_func = marketplace.page_scrape
        else:
            scraper_func = marketplace.main_page_scrape

        thread = threading.Thread(target=search_and_append_result, args=(func, results, scraper_func, query))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    try:
        search_results = sorted(search_results, key=operator.itemgetter('Price'), reverse=True)
    except KeyError:
        return search_results

    return search_results
