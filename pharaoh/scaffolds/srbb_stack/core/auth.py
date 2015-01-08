"""Model agnostic authentication utility functions.
"""

import pyramid.security


def init_auth(settings, config):
    global get_groups
    global get_this_user

    # Retreive the `get_user` function as specified in the ini.
    get_user = config.maybe_dotted(settings['auth.get_user_func'])

    def get_groups(userid, request):
        """Get a list of groups the user belongs to.
        Used as the AuthTktAuthenticationPolicy callback. 
        """

        user = get_user(userid, request)
        if user:
            return ['g:%s' % g.name for g in user.groups]

    def get_this_user(request):
        """
        """

        userid = pyramid.security.unauthenticated_userid(request)
        if userid:
            return get_user(userid, request)