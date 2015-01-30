"""Admin Panel Views.
"""

import pyramid.view


@pyramid.view.view_config(route_name="home", renderer="home.html_mako",
                            permission="admin")
def home(request):
    """
    """
    return {}


@pyramid.view.view_config(route_name="security", renderer="security.html_mako",
                            permission="admin")
def security(request):
    """
    """
    return {}