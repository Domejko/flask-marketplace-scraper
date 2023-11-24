import pytest
from bs4 import BeautifulSoup

import app.tools


@pytest.mark.parametrize('price', [
    '<span class="ux-textspans">EUR 2.340,00</span>',
    '<span class="ux-textspans">€ 2.340,00</span>',
    '<span class="ux-textspans"> 2.340,00</span>',
    '<span class="ux-textspans">EUR 2340 tot EUR 2500</span>'
])
def test_price_converter(price: str):
    soup = BeautifulSoup(price, 'html.parser')
    assert app.tools.price_converter(soup) == 2340


def test_price_converter_failure():
    soup = BeautifulSoup('<span class="ux-textspans">$2.340,00</span>', 'html.parser')
    with pytest.raises(ValueError):
        app.tools.price_converter(soup)


def test_build_re_expression(search_string='find test item'):
    assert app.tools.build_re_expression(search_string) == '(?=.*find)(?=.*test)(?=.*item)'
