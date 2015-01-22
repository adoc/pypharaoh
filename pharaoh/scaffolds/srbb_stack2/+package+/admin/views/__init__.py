"""
"""

import pyramid.view


@pyramid.view.view_config(route_name="home", renderer="home.html_mako",
                            permission="admin")
def home(request):
    """
    """
    return {}


    # return {'a': pyramid.security.remember(request, '12345')}
    # return {'static_path': request.static_map_path('static', ''),
    #         'title': request.site_meta_title, 'footer': request.site_meta_footer}