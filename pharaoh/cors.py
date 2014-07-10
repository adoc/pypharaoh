import urllib.parse


def gen_headers(request, allowed_headers=['Content-Type'],
            allowed_methods=['GET', 'PUT', 'POST']):
    # Move this. It's not a formencode helper.
    # Change this to a class instance per request?

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
        # Always creds?
        ('Access-Control-Allow-Credentials', 'true'),
        ('Access-Control-Allow-Headers', ','.join(allowed_headers)),
        ('Access-Control-Allow-Methods', ','.join(allowed_methods))]
    # At first glance, this may appear insecure, but if the referer
    # should be checked, it should be checked elsewhere.
    if request.referer:
        refp = urllib.parse.urlparse(request.referer)
        origin = urllib.parse.urlunparse((refp.scheme, refp.netloc,
                                          '', '', '', ''))

        headers.append(('Access-Control-Allow-Origin', origin))
        #headers.append(('Access-Control-Allow-Origin', request.referer.rstrip('/')))
        #headers.append(('Access-Control-Allow-Origin', request.referer))
    return headers