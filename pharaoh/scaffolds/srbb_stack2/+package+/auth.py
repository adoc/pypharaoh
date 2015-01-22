"""Model agnostic authentication utility functions.
"""

import pyramid.security


def init_auth(config, settings):
    """
    """

    global get_user
    global get_groups_callback
    global get_groups
    global get_this_user
    global has_permission_bool

    # Retreive the `get_user` function as specified in the ini.
    _get_user = settings['auth.get_user_func']
    _get_user_byname = settings['auth.get_user_byname_func']

    def get_user(request, userid):
        return _get_user(userid)

    def get_user_byname(request, username):
        return _get_user_byname(username)

    def get_groups_callback(userid, request):
        """Get a list of groups the user belongs to.
        Used as the AuthTktAuthenticationPolicy callback.

        Note: Due to AuthTktAuthenticationPolicy code, the callback
        requires `userid` as the first param and `request as the
        second.
        """

        user = get_user(request, userid)
        if user:
            return ['g:%s' % g.name for g in user.groups]

    def get_groups(request, userid):
        return get_groups_callback(userid, request)

    def get_this_user(request):
        """
        """
        userid = pyramid.security.unauthenticated_userid(request)
        if userid:
            return get_user(request, userid)

    def has_permission_bool(request, permission, context):
        """Boolean return for ``request.has_permission``.
        """
        return isinstance(request.has_permission(permission, context),
                            pyramid.security.Allowed)

    config.add_request_method(get_user, property=False, reify=False)
    config.add_request_method(get_user_byname, property=False, reify=False)
    config.add_request_method(get_groups, property=False, reify=False)
    config.add_request_method(get_this_user, name='this_user', property=True,
                                reify=False)
    config.add_request_method(has_permission_bool, property=False, reify=False)
