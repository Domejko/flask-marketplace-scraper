from flask import Blueprint

from .home import Index
from .search import Search


# Defining two routers
routes = (Index, Search)

# The view object is created as a Blueprint, which allows the routes to be organized and registered as a modular
# set of views.
# The template_folder parameter is set to '../templates', which specifies the folder where the view templates are
# located.
view = Blueprint('view', __name__, template_folder='../templates')

# A loop is used to iterate over the routes tuple, and for each route, an URL rule is added using the add_url_rule
# function.
for route in routes:
    view.add_url_rule(route.path, view_func=route.as_view(route.name))
