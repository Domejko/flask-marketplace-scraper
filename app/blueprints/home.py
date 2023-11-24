from flask.views import MethodView
from flask import render_template


class Index(MethodView):

    name = 'index'
    path = '/'

    def get(self):
        """
        Description:
            This method is called when a GET request is made to the index page.
            It returns the rendered template 'layout.html'.
        """
        return render_template('layout.html')
