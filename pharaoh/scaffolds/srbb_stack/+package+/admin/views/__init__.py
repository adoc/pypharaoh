"""Admin Panel Views.
"""

import pyramid.view

from pprint import pprint

@pyramid.view.view_config(route_name="home", renderer="home.html_mako",
                            permission="admin")
def home(request):
    """
    """
    request.session['test'] = 'test'
    pprint(request.session._session())
    return {}


@pyramid.view.view_config(route_name="security", renderer="security.html_mako",
                            permission="admin")
def security(request):
    """
    """
    return {}