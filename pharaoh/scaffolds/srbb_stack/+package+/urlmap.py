"""
Copyright (c) 2008-2011 Agendaless Consulting and Contributors.
(http://www.agendaless.com), All Rights Reserved

Portions (c) Ian Bicking.
"""

from rutter.urlmap import URLMap, _parse_path_expression

# Do not pass ``local_config`` as keyword args to preserve OrderedDict.
def urlmap_factory(loader, global_conf, local_conf):
    if 'not_found_app' in local_conf:
        not_found_app = local_conf.pop('not_found_app')
    else:
        not_found_app = global_conf.get('not_found_app')
    if not_found_app:
        not_found_app = loader.get_app(not_found_app, global_conf=global_conf)
    if not_found_app is not None:
        urlmap = URLMap(not_found_app=not_found_app)
    else:
        urlmap = URLMap()
    for path, app_name in local_conf.items():
        path = _parse_path_expression(path)
        app = loader.get_app(app_name, global_conf=global_conf)
        urlmap[path] = app
    return urlmap