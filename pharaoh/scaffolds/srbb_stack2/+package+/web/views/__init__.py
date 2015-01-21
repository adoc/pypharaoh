"""
"""

import pyramid.view


@pyramid.view.view_config(route_name="home", renderer="home.html_mako",
                            permission="public")
def home(request):
    """
    """
    return {}


@pyramid.view.view_config(route_name="common.js", renderer="common.js_mako",
                            permission="public")
def common_js(request):
    """
    """
    request.response.content_type = "application/javascript"
    return {}


@pyramid.view.view_config(route_name="config.js", renderer="config.js_mako",
                            permission="public")
def config_js(request):
    """
    """
    request.response.content_type = "application/javascript"
    return {}


    # return {'a': pyramid.security.remember(request, '12345')}
    # return {'static_path': request.static_map_path('static', ''),
    #         'title': request.site_meta_title, 'footer': request.site_meta_footer}