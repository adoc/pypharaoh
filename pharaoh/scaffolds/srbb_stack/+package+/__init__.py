"""
"""

import pyramid.config


def main(global_config, **local_config):
    """ This function returns a Pyramid WSGI application.
    """
    print("Initializing Platform Web Application...")

    config = pyramid.config.Configurator(settings=local_config)


    if 'authentication_policy' in global_config:
        config.set_authentication_policy(global_config['authentication_policy'])

    if 'authorization_policy' in global_config:
        config.set_authorization_policy(global_config['authorization_policy'])


    return config.make_wsgi_app()