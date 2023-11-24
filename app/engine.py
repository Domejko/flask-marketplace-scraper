import re
import types
import functools
import operator
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError

import app.database
import app.connect
from app.tools import build_re_expression, price_converter


class SearchEngine:
    """
    Description:
        This class represents a search engine object used to scrape data from webpages and save the data to a database.

    Attributes:
        url (str): The base URL used for searching.

        base_url (str): The base URL used to construct complete links.

        find_all_tag (list): A list containing the tag name, attribute, and value used to locate items on a webpage.

        main_tags (dict): A dictionary containing the tag names, attributes, and values used to locate specific
                        information on the main page.

        db_model (app.database.Base): The database model used for storing scraped data.

        how_many_pages (int): The number of pages to scrape.

        db (types.ModuleType): The module used for connecting to the database.

        rating_tags (list[list, list]): A list of lists containing the tag names, attributes, and values used to locate
                        rating information on a webpage.

        page_tags (dict): A dictionary containing the tag names, attributes, and values used to locate specific
                        information on a subsequent page.

    Methods:
        url_search(search_string: str) -> list: Searches for items on the webpage and returns a list of found items.

        main_page_scrape(search_string: str) -> list[dict]: Scrapes information from the main page and returns a list of
        dictionaries containing the scraped data.

        get_links(search_string: str) -> list: Retrieves the links for the found items on the webpage and returns a
        list of links.

        page_scrape(search_string: str) -> list[dict]: Scrapes information from subsequent pages and returns a list of
        dictionaries containing the scraped data.

        find_tags(soup: BeautifulSoup, tags: dict) -> dict: Finds specified tags on a webpage and returns a dictionary
        containing the scraped data.

        save_to_database(items_list: list[dict] = None) -> None: Saves the scraped data to the database.

        page_search(search_string: str) -> list[dict]: Performs a page-based search, scrapes data from subsequent pages,
        and saves the data to the database. Returns a list of dictionaries containing the scraped data.

        main_search(search_string: str) -> list[dict]: Performs a main page search, scrapes data from the main page, and
        saves the data to the database. Returns a list of dictionaries containing the scraped data.
    """

    def __init__(self, url: str, base_url: str, find_all_tag: list, main_tags: dict, db_model: app.database.Base,
                 how_many_pages: int = 1, db: types.ModuleType = app.database, rating_tags: list[list, list] = None,
                 page_tags: dict = None) -> None:

        self.items_list = []

        self.how_many_pages = how_many_pages

        self.url = url
        self.base_url = base_url

        self.db_model = db_model
        self.db = db

        self.find_all_tag = find_all_tag
        self.main_tags = main_tags
        self.rating_tags = rating_tags
        self.page_tags = page_tags

    def url_search(self, search_string: str) -> list:
        """
        Description:
            Searches for items on the webpage and returns a list of found items.

        Parameters:
            search_string (str): The search string used to search for items on the webpage.

        Returns:
            result (list): A list of found items on the webpage.
        """
        temp_list = []

        for page in range(self.how_many_pages):
            url = app.connect.get_url(search_string, page, self.url)
            response, _ = app.connect.connection(url)
            soup = BeautifulSoup(response, 'html.parser')
            items = soup.find_all(self.find_all_tag[0], attrs={self.find_all_tag[1]: self.find_all_tag[2]})
            temp_list.append(items)

        result = functools.reduce(operator.iconcat, temp_list, [])

        return result

    def main_page_scrape(self, search_string: str) -> list[dict] | bool:
        """
        Description:
            Scrapes information from the main page using the provided search string and returns a list of dictionaries
            containing the scraped data.

        Parameters:
            search_string (str): The search string used to search for items on the main page.

        Returns:
            items_list (list[dict]): A list of dictionaries containing the scraped data from the main page.
            bool (False): If no results have been found.

        Raises:
            ValueError: If result_dict['Link'] value is missing.
        """
        result = self.url_search(search_string)

        if len(result) == 0:
            return False

        for soup in result:
            try:
                result_dict = self.find_tags(soup, self.main_tags)

                if result_dict['Link'] == f'{self.base_url}None':
                    raise ValueError
                self.items_list.append(result_dict)
            except AttributeError:
                continue
            except ValueError:
                continue

        return self.items_list

    def get_links(self, search_string: str) -> list:
        """
        Description:
            Retrieves the links for the found items on the webpage using the provided search string and returns a list
            of links.

        Parameters:
            search_string (str): The search string used to search for items on the webpage.

        Returns:
            temp_link_list (list): A list of links for the found items on the webpage.
        """
        result = self.url_search(search_string)
        expression = build_re_expression(search_string)
        temp_link_list = []

        for soup in result:
            item_title = soup.find(self.main_tags['Item'][0],
                                   attrs={self.main_tags['Item'][1]: self.main_tags['Item'][2]})

            if re.search(fr'{expression}', str(item_title), flags=re.IGNORECASE):
                item_link = self.base_url + soup.find(self.main_tags['Link'][0],
                                                      attrs={self.main_tags['Link'][1]: self.main_tags['Link'][2]}).get('href')
                temp_link_list.append(item_link)

        return temp_link_list

    def page_scrape(self, search_string: str) -> list[dict] | bool:
        """
        Description:
            Scrapes information from subsequent pages using the links of found items and returns a list of
            dictionaries containing the scraped data.

        Parameters:
            search_string (str): The search string used to search for items on the webpage.

        Returns:
            items_list (list[dict]): A list of dictionaries containing the scraped data from subsequent pages.
            bool (False): If no results have been found.
        """
        links_list = self.get_links(search_string)

        if len(links_list) == 0:
            return False

        for link in links_list:
            response, _ = app.connect.connection(link)
            soup = BeautifulSoup(response, 'html.parser')

            try:
                result_dict = self.find_tags(soup, self.page_tags)
                result_dict['Link'] = link
                self.items_list.append(result_dict)
            except AttributeError:
                continue
            except ValueError:
                continue

        return self.items_list

    def find_tags(self, soup: BeautifulSoup, tags: dict) -> dict:
        """
        Description:
            Finds specified tags on a webpage using BeautifulSoup and returns a dictionary containing the scraped data.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object representing the webpage.
            tags (dict): A dictionary containing the tag names, attributes, and values used to locate specific
                        information on the webpage.

        Returns:
            results_dict (dict): A dictionary containing the scraped data.

        Raises:
            Exception: If value[3] of tags dictionary is not set as int in range 0-5

        """
        results_dict = {}

        for key, value in tags.items():
            match value[3]:
                case 0:
                    results_dict[key] = soup.find(value[0], attrs={value[1]: value[2]})
                case 1:
                    results_dict[key] = price_converter(soup.find(value[0], attrs={value[1]: value[2]}))
                case 2:
                    results_dict[key] = soup.find(value[0], attrs={value[1]: value[2]}).text.strip()
                case 3:
                    results_dict[key] = soup.find(value[0], attrs={value[1]: value[2]}).get('src')
                case 4:
                    results_dict[key] = f'{self.base_url}{soup.find(value[0], attrs={value[1]: value[2]}).get("href")}'
                case 5:
                    results_dict[key] = soup.find(value[0]).get('src')
                case _:
                    raise Exception('Tag constant improperly formatted.')

        return results_dict

    def save_to_database(self, items_list: list[dict] = None) -> None:
        """
        Description:
            Saves the scraped data to the database.

        Parameters:
            items_list (list[dict], optional): A list of dictionaries containing the scraped data. Defaults to None.
        """
        for item in items_list:
            try:
                session = self.db.SessionLocal()

                data = self.db_model(item=item['Item'], price=item['Price'], link=f"{item['Link']}")

                session.add(data)
                session.commit()

            except IntegrityError:
                continue
            except ValueError:
                continue

    def page_search(self, search_string: str) -> list[dict]:
        """
        Description:
            Performs a page-based search, scrapes data from subsequent pages, and saves the data to the database.
            If page_scrape() haven't found any results then it returns bool and page_search returns 'No Results Found'
            message, else it returns a list of dictionaries containing the scraped data.

        Parameters:
            search_string (str): The search string used to search for items on the webpage.

        Returns:
            items_list (list[dict]): A list of dictionaries containing the scraped data from subsequent pages.
        """
        items_list = self.page_scrape(search_string)
        if not items_list:
            return [{'Msg': 'No Results Found.'}]

        self.save_to_database(items_list)

        return items_list

    def main_search(self, search_string: str) -> list[dict]:
        """
        Description:
            Performs a main page search, scrapes data from the main page, and saves the data to the database.
            If main_page_scrape() haven't found any results then it returns bool and main_search returns
            'No Results Found' message, else it returns a list of dictionaries containing the scraped data.

        Parameters:
            search_string (str): The search string used to search for items on the main page.

        Returns:
            items_list (list[dict]): A list of dictionaries containing the scraped data from the main page.
        """
        items_list = self.main_page_scrape(search_string)
        if not items_list:
            return [{'Msg': 'No Results Found.'}]

        self.save_to_database(items_list)

        return items_list
