from flask.views import MethodView
from flask import render_template, request

from app.main import run_search


class Search(MethodView):
    
    name = 'search'
    path = '/search'
    
    def post(self):
        """
        Description:
            This function is responsible for handling the POST request. It retrieves the query from the request form
            and processes it to perform a search. It also checks for any item conditions selected by the user and
            includes it in the search criteria. The search results are then rendered using the 'table.html' template.

        Returns:
            HTML template rendered with search results
        """
        query: str = ''

        # Retrieve query from request form for key in request.form
        for key in request.form:
            if key.startswith('comment.'):
                id_ = key.partition('.')[-1]
                query = request.form[key]

        # If input have been filled and POST method have been sent function
        # checks the checkboxes values and pass them with query variable to
        # a searching function and returns html template with a search result
        if len(query) != 0 and request.method == 'POST':
            temp = request.form.getlist('check')
            item_condition = sum(list(map(int, temp)))

            return render_template('table.html', data=run_search(query, item_condition))
    