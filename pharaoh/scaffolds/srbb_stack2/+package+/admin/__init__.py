import pyramid.config

import core


def main(global_config, **local_config):
    print("Initializing Platform Admin Dashboard...")

    config, settings = core.init_config(global_config, local_config)

    config.scan('admin.views')
    return config.make_wsgi_app()