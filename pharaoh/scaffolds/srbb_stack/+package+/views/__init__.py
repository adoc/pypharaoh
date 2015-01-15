

import pyramid.view

import core.auth


@pyramid.view.view_config(route_name="info", renderer="json",
                            permission="public")
def info(request):

    return {'a': pyramid.security.remember(request, '12345')}

    return {'static_path': request.static_map_path('static', ''),
            'title': request.site_meta_title, 'footer': request.site_meta_footer}