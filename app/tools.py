import bs4
import re


def price_converter(price: bs4.element.Tag) -> int:
    """
    Description:
        This function takes in a price value as a bs4.element.Tag object and converts it into an integer.
        The function checks if the price contains either the Euro symbol (€) or the word "EUR" using regular
        expressions. If it does, it extracts the actual price value from the bs4.element.Tag object by stripping and
        splitting the text.The extracted price is then formatted by removing any thousands separators and replacing
        the decimal comma with a dot. Finally, the formatted price is rounded and converted into an integer.
        If the price contains the Dollar symbol ($), a ValueError is raised due to the fact that eBay marketplace
        sometimes contains offers outside of EU. If the price does not contain either the Euro symbol or the Dollar
        symbol, it is assumed to already be in the correct format and is simply stripped of any whitespace and
        returned as an integer.

    Parameters:
        price: A bs4.element.Tag object representing the price value.

    Returns:
        formatted_price: An integer representing the converted and formatted price value.

    Raises:
        ValueError: If price element.Tag contains a Dollar symbol ($).
    """
    if re.search(r'(€)|\bEUR\b', str(price)):
        formatted_price = price.text.strip().split()[1]
        formatted_price = round(float(formatted_price.replace('.', '').replace(',', '.')))
    elif re.search(r'(\$)', str(price)):
        raise ValueError
    else:
        formatted_price = price.text.strip()
        formatted_price = round(float(formatted_price.replace('.', '').replace(',', '.')))

    return formatted_price


def build_re_expression(search_string: str) -> str:
    """
    Description:
        This function takes in a search_string parameter, which is a string consisting of one or more words. It returns
        a regular expression pattern that can be used for searching for all the words in the search_string.

    Parameters:
        search_string (str): The input string containing the words to be searched.

    Returns:
        expression (str): The built regular expression pattern for searching the words in the search_string.

    Example Usage:
        search_string = 'hello world'

        pattern = build_re_expression(search_string)

        print(pattern)

    Output:
        (?=.*hello)(?=.*world)
    """
    words = search_string.split()
    pre_build = ['(?=.*' + word + ')' for word in words]
    expression = ''.join(pre_build)

    return expression
