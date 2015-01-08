import urllib.parse


def gen_headers(request, allowed_headers=['Content-Type'],
            allowed_methods=['GET', 'PUT', 'POST']):
    # TODO: Change this to a class instance per request?

    # Consider these headers:
    # X-CSRF-Token
    # X-Requested-With
    # Accept
    # Accept-Version
    # Content-Length
    # Content-MD5
    # Content-Type
    # Date
    # X-Api-Version
    headers = [
        ('Access-Control-Allow-Credentials', 'true'), # Always Allow-Credentials?
        ('Access-Control-Allow-Headers', ','.join(allowed_headers)),
        ('Access-Control-Allow-Methods', ','.join(allowed_methods))]
    # At first glance, this may appear insecure, but if the referer
    # should be checked, it should be checked elsewhere. Remember,
    # the referer is never a good security metric.
    if request.referer:
        refp = urllib.parse.urlparse(request.referer)  # User pyramid.compat here.
        origin = urllib.parse.urlunparse((refp.scheme, refp.netloc,
                                          '', '', '', ''))
        headers.append(('Access-Control-Allow-Origin', origin))
    return headers


def decorator(allowed_headers=['Content-Type'],
            allowed_methods=['GET', 'PUT', 'POST']):
    """View Decorator"""
    def _cors_view_decorator(view_callable):
        def _cors_view(context, request):
            request.response.headers.update(gen_headers(request, 
                                               allowed_headers=allowed_headers,
                                               allowed_methods=allowed_methods))
            return view_callable(context, request)
        return _cors_view
    return _cors_view_decorator