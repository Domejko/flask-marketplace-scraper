from app.engine import SearchEngine
from app.constants import AMAZON_URLs, AMAZON_PAGE_TAGS, AMAZON_MAIN_TAGS, AMAZON_FIND_ALL_TAG
from app.models.db_models import Amazon


def amazon(item_condition: int = 0) -> SearchEngine:
    """
    Description:
        Function that returns SearchEngine class object set up for
        Amazon scraping.

    Parameters:
        item_condition (int): int representing item condition (default 0).

                                0 -- represents new items

                                1 -- represents used items

                                2 -- represents new and used items"""

    amazon_search = SearchEngine(url=AMAZON_URLs[item_condition],
                                 base_url=AMAZON_URLs[3],
                                 find_all_tag=AMAZON_FIND_ALL_TAG,
                                 main_tags=AMAZON_MAIN_TAGS,
                                 page_tags=AMAZON_PAGE_TAGS,
                                 db_model=Amazon)

    return amazon_search
