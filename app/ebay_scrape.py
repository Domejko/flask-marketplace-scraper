from app.engine import SearchEngine
from app.constants import EBAY_URLs, EBAY_MAIN_TAGS, EBAY_FIND_ALL_TAG
from app.models.db_models import EBay


def ebay(item_condition: int = 0) -> SearchEngine:
    """
    Description:
        Function that returns SearchEngine class object set up for
        EBay scraping.

    Parameters:
        item_condition (int): int representing item condition (default 0).

                                0 -- represents new items

                                1 -- represents used items

                                2 -- represents new and used items"""

    ebay_search = SearchEngine(url=EBAY_URLs[item_condition],
                               base_url=EBAY_URLs[3],
                               find_all_tag=EBAY_FIND_ALL_TAG,
                               main_tags=EBAY_MAIN_TAGS,
                               db_model=EBay)

    return ebay_search
