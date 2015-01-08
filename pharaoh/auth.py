
import pyramid.authentication


def auth_tkt_from_config(settings, callback=None, prefix="auth_tkt"):
    """Configure AuthTktAuthenticationPolicy based on settings from
    the ini.
    """

    def jk(key):
         return '.'.join([prefix, key])

    auth_tkt_kwa = {
        'callback': callback
    }

    if jk('secret') not in settings:
        raise KeyError(""""secret" is required to configure """
                """AuthTktAuthenticationPolicy.""")

    if jk('callback') in settings:
        raise KeyError(""""callback" is not expected in the config ini for """
                """AuthTktAuthenticationPolicy.""")

    for key, val in settings.items():
        if key.startswith(prefix):
            key = key.split('.')[-1]
            auth_tkt_kwa[key] = val

    return pyramid.authentication.AuthTktAuthenticationPolicy(secret,
                                                                **auth_tkt_kwa)