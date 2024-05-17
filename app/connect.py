import requests
from requests import Response
from requests.exceptions import MissingSchema


def get_url(search_term: str, page_number: int, url: str) -> str:
    """
    Description:
        This function generates a URL by replacing placeholders in the given URL template with the search
        term and page number. The search term is formatted by replacing spaces with '+'. The generated URL is then
        returned as a string.

    Parameters:
        search_term (str): A string representing the search term.
        page_number (int): An integer representing the page number.
        url (str): A string representing the URL template.

    Returns:
        A string representing the generated URL.

    Raises:
        ValueError: If the page_number is not a valid integer.

    Example usage:
        search_term = "programming languages"

        page_number = 1

        url = "https://www.example.com/search?term={search}&page={page}"

        result = get_url(search_term, page_number, url)

        In this example, the function will generate and return the following
        URL: "https://www.example.com/search?term=programming+languages&page=1"
    """
    page = str(page_number)
    if page.isalpha():
        raise ValueError('Incorrect page format')
    template = url
    search_term = search_term.replace(' ', '+')

    return template.format(search=search_term, page=page_number)


def connection(url: str) -> (bytes, Response):
    """
    Description:
        The "connection" function takes in a URL as a parameter and returns two values: the response content
        (as bytes) and the response object.

    Parameters:
        url (str): The URL you want to make a GET request to.

    Returns:
        response_content (bytes): The content of the response as bytes.
        response_obj (Response): The full response object returned by the GET request.

    Exceptions:
        MissingSchema: If the URL passed as the parameter does not have a valid schema (e.g., "http://" or
        "https://"), a MissingSchema exception is raised.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        counter = 0
        print(response.status_code)
        while response.status_code != 200:
            print(url)
            counter += 1
            response = requests.get(url)
            if counter == 20:
                break
    except MissingSchema:
        raise Exception("The address you're trying to connect to is incorrect.")

    return response.content, response
