from app.engine import SearchEngine
from app.constants import MARKTPLAATS_URLs, MARKTPLAATS_MAIN_TAGS, MARKTPLAATS_FIND_ALL_TAG
from app.models.db_models import Marktplaats


def marktplaats(item_condition: int = 0) -> SearchEngine:
    """
    Description:
        Function that returns SearchEngine class object set up for
        Marktplaats scraping.

    Parameters:
        item_condition (int): int representing item condition (default 0).

                                0 -- represents new items

                                1 -- represents used items

                                2 -- represents new and used items"""

    marktplaats_search = SearchEngine(url=MARKTPLAATS_URLs[item_condition],
                                      base_url=MARKTPLAATS_URLs[3],
                                      find_all_tag=MARKTPLAATS_FIND_ALL_TAG,
                                      main_tags=MARKTPLAATS_MAIN_TAGS,
                                      db_model=Marktplaats)

    return marktplaats_search
