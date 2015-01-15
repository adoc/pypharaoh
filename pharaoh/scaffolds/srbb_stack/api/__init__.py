import functools
import urllib.parse
import pyramid.config

import core

from pprint import pprint



def main(global_config, **local_config):
    """
    """
    print("Initializing Platform API...")
    config, settings = core.init_config(global_config, local_config)

    config.add_route('api_info', '/info')
    config.scan('api.views')

    # Set up API's for any composite applications.
    for key, val in settings['composite'].items():
        base = key if key.endswith('/') else key+'/'
        key_uri = functools.partial(urllib.parse.urljoin, base)

        if val == 'admin':
            config.add_route('api_admin_info', key_uri('info'))
            config.add_route('api_admin_users', key_uri('users'))
            config.scan('admin.api')

    return config.make_wsgi_app()