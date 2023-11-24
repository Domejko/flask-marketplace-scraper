AMAZON_URLs = ['http://www.amazon.nl/s?k={search}&page={page}&rh=p_n_condition-type%3A17170958031',
               'http://www.amazon.nl/s?k={search}&page={page}&rh=p_n_condition-type%3A17948759031',
               'http://www.amazon.nl/s?k={search}&page={page}',
               'http://www.amazon.nl']

AMAZON_PAGE_TAGS = {'Img': ['img', 'id', 'landingImage', 3],
                    'Item': ['span', 'class', 'a-size-large product-title-word-break', 2],
                    'Price': ['span', 'class', 'a-price-whole', 1],
                    'Rating': ['span', 'class', 'a-size-base a-color-base', 2]}

AMAZON_FIND_ALL_TAG = ['div', 'class', 'a-section a-spacing-base']

AMAZON_MAIN_TAGS = {'Img': ['img', 5, 5, 5],
                    'Item': ['span', 'class', 'a-size-base-plus a-color-base a-text-normal', 2],
                    'Price': ['span', 'class', 'a-price-whole', 1],
                    'Link': ['a', 'class', 'a-link-normal s-no-outline', 4]}

# --------------------------------------------------------------------------------------------------------------------#


MARKTPLAATS_URLs = ['https://www.marktplaats.nl/q/{search}/p/{page}/#f:30|searchInTitleAndDescription:true',
                    'https://www.marktplaats.nl/q/{search}/p/{page}/#f:31,32|searchInTitleAndDescription:true',
                    'https://www.marktplaats.nl/q/{search}/p/{page}/#f:30,31,32|searchInTitleAndDescription:true',
                    'https://www.marktplaats.nl']

MARKTPLAATS_FIND_ALL_TAG = ['div', 'class', 'hz-Listing-item-wrapper']

MARKTPLAATS_MAIN_TAGS = {'Img': ['img', 5, 5, 5],
                         'Item': ['h3', 'class', 'hz-Listing-title', 2],
                         'Price': ['span', 'class', 'hz-Listing-price hz-Listing-price--desktop hz-text-price-label',
                                   1],
                         'Link': ['a', 'class', 'hz-Link hz-Link--block hz-Listing-coverLink', 4]}

# --------------------------------------------------------------------------------------------------------------------#

EBAY_URLs = ['https://www.ebay.nl/sch/i.html?_nkw={search}&_pgn={page}&LH_ItemCondition=3&LH_PrefLoc=3',
             'https://www.ebay.nl/sch/i.html?_nkw={search}&_pgn={page}&LH_ItemCondition=4&LH_PrefLoc=3',
             'https://www.ebay.nl/sch/i.html?_nkw={search}&_pgn={page}&LH_ItemCondition=4|3&LH_PrefLoc=3',
             ' ']

EBAY_FIND_ALL_TAG = ['div', 'class', 's-item__wrapper clearfix']

EBAY_MAIN_TAGS = {'Img': ['img', 5, 5, 5],
                  'Item': ['span', 'role', 'heading', 2],
                  'Price': ['span', 'class', 's-item__price', 1],
                  'Link': ['a', 'class', 's-item__link', 4]}
