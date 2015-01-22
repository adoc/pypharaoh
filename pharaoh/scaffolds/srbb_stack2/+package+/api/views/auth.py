"""
"""
import pyramid.security


import core.models.auth


def login_view(request):
    """API Login View. Returns "success" is True when successfully
    logged in.
    """
    # TODO: Validate params.
    try:
        params = request.json_body
    except ValueError:
        params = request.params
    username = params.get('login')
    password = params.get('password')
    set_cookie = params.get('set_cookie', True)
    if username and password:
        challenge_user = core.models.auth.get_user_byname(username)
        if challenge_user and challenge_user.check_password(password):
            # TODO: Another ticket method will be needed if set_cookie is False.
            if set_cookie is True:
                request.response.headerlist.extend(
                    pyramid.security.remember(request, challenge_user.ident))
            else:
                raise NotImplementedError("No ticket method implemented for "
                                            "'set_cookie' false.")
            return {'success': True}
    return {'success': False}
login_view.renderer = 'json'


def logout_view(request):
    """API Logout View.
    """
    try:
        params = request.json_body
    except ValueError:
        params = request.params
    set_cookie = params.get('set_cookie', True)
    if set_cookie is True:
        request.response.headerlist.extend(pyramid.security.forget(request))
    else:
        raise NotImplementedError("No ticket method implemented for "
                                    "'set_cookie' false.")
    return {'success': True}
logout_view.renderer = 'json'