from unittest import mock
from flask import Flask

from app.blueprints import Search
from tests.conftest import Fixture


def test_home(client: Fixture[Flask]) -> None:
    response = client.get('/')
    assert b'<title>Price Comparison</title>' in response.data
    assert response.status_code == 200


def test_search(client: Fixture[Flask]) -> None:
    response = client.post('/search', data={'comment.s': 'test query', 'check': 1})
    assert response.status_code == 200


def test_search_post(my_app: Fixture[Flask]) -> None:
    query = 'test query'
    item_condition = 1

    with mock.patch('app.blueprints.search.render_template') as mock_render_template:
        with mock.patch('app.blueprints.search.run_search') as mock_run_search:

            mock_run_search.return_value = 'test result'
            mock_render_template.return_value.status_code = 200

            with my_app.test_request_context(path='/search', method='POST',
                                             data={'comment.id': query, 'check': '1'},
                                             content_type='multipart/form-data'):

                search_view = Search()
                response = search_view.post()

                mock_run_search.assert_called_once_with(query, item_condition)
                mock_render_template.assert_called_with('table.html', data='test result')

                assert response.status_code == 200
                assert response == mock_render_template.return_value



