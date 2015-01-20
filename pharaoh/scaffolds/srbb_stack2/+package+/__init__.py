"""Initialize the core application services.
"""

import logging
log = logging.getLogger(__name__)

import os
import functools
import rutter.urlmap
import pytz
import pyramid.settings
import pyramid.security
import pyramid.path

import pharaoh.auth

import core.models
import core.models.auth
import core.auth


from pprint import pprint



class RootFactory:
    """RootFactory used for all composite apps. ACL's are set from the
    config ini.
    """

    def __init__(self, request):
        self.request = request


def init_settings(settings):
    """Set application specific settings."""

    resolver = pyramid.path.DottedNameResolver(
                                    pyramid.path.caller_package())

    settings['datetime.date_format'] = settings.get('datetime.date_format',
                                                    '%Y-%m-%d')
    settings['datetime.time_format'] = settings.get('datetime.time_format',
                                                    '%I:%M:%S%p')
    settings['datetime.local_timezone'] = pytz.timezone(
                                settings.get('datetime.local_timezone', 'UTC'))
    settings['database.enable'] = pyramid.settings.asbool(
                                        settings.get('database.enable', False))
    settings['database.epoch'] = settings.get('database.epoch', '1970-1-1')
    settings['database.timezone'] = pytz.timezone(
                                    settings.get('database.timezone', 'UTC'))
    settings['database.initialize.drop_all'] = pyramid.settings.asbool(
                            settings.get('database.initialize.drop_all', False))
    settings['auth.enable'] = pyramid.settings.asbool(
                                            settings.get('auth.enable', False))

    # settings['auth.uri.login'] = settings.get('auth.uri.login', '/login')
    # settings['auth.uri.logout'] = settings.get('auth.uri.logout', '/logout')
    # settings['auth.uri.after_logout'] = settings.get('auth.uri.after_logout',
    #                                                    '/')

    # aslist parse (group:level)
    def parse_groups():
        for init_group in pyramid.settings.aslist(
                                    settings.get('auth.initialize.groups', [])):
            group, level = init_group.split(':')
            yield {'name': group.strip(), 'level': level.strip()}

    settings['auth.initialize.groups'] = list(parse_groups())

    # aslist parse (user:password:group1[, group2])
    def parse_users():
        for init_users in pyramid.settings.aslist(
                                    settings.get('auth.initialize.users', [])):
            username, password, groups = init_users.split(':')

            yield {'name': username.strip(),
                    'password': password.strip(),
                    'groups': [group.strip() for group in groups.split(',')]}

    settings['auth.initialize.users'] = list(parse_users())

    settings['auth.get_user_func'] = resolver.resolve(
                settings.get('auth.get_user_func', 'core.models.auth:get_user'))

    settings['authn.models.enable'] = pyramid.settings.asbool(
                                    settings.get('authn.models.enable', False))
    settings['authn.models.user.tablename'] = settings.get(
                                        'authn.models.user.tablename', 'users')
    settings['authn.models.group.tablename'] = settings.get(
                                    'authn.models.group.tablename', 'groups')
    settings['authn.models.user_group.tablename'] = settings.get(
                            'authn.models.user_group.tablename', 'users_groups')
    assert settings['authn.models.identity.secret'], ("Config settings "
                "'authn.models.identity.secret' missing. Application cannot "
                "initialize.")
    settings['authn.models.identity.use_password'] = pyramid.settings.asbool(
                    settings.get('authn.models.identity.use_password', False))
    settings['authz.models.enable'] = pyramid.settings.asbool(
                                    settings.get('authz.models.enable', False))

    settings['authz.models.permissions.tablename'] = settings.get(
                            'authz.models.permissions.tablename', 'permissions')

    def parse_root_permissions():
        for init_perms in pyramid.settings.aslist(
                            settings.get('authz.root_factory.permissions', [])):
            action, principal, permissions = init_perms.split(':')

            action = (pyramid.security.Allow
                        if action.strip() == 'allow' else pyramid.security.Deny)
            
            if principal == 'all':
                principal = pyramid.security.Everyone
            else:
                principal = ':'.join(['g', principal])

            def parse_permissions():
                for permission in permissions.split(','):
                    if permission == 'all':
                        permission = pyramid.security.ALL_PERMISSIONS
                    yield permission

            permissions = tuple(parse_permissions())

            yield (action, principal, permissions)

    settings['authz.root_factory.permissions'] = list(parse_root_permissions())

    def parse_static_mapping():
        for mapping in pyramid.settings.aslist(settings['static.mapping']):
            url, directory, cache_max_age = mapping.split('|')
            yield (url, (directory, int(cache_max_age)))

    if 'static.mapping' in settings:
        settings['static.mapping'] = dict(parse_static_mapping())

    settings['static.serve'] = pyramid.settings.asbool(
                                            settings.get('static.serve', False))


def init_config(global_config, local_config):
    # Handle the settings/config
    settings = global_config
    settings.update(local_config)
    init_settings(settings)

    config = pyramid.config.Configurator(settings=settings)

    def get_val(value):
        def _get_val(request):
            return value
        return _get_val

    for key, value in settings.items():
        if key.startswith('site.meta.'):
            config.add_request_method(get_val(value),
                                            name=key.replace('.', '_'),
                                            property=True, reify=True)

    caller = pyramid.path.caller_package()
    resolver = pyramid.path.DottedNameResolver(caller)

    if any(key in settings for key in ['auth.uri.login', 'auth.uri.logout']):
        try:
            auth_views = resolver.resolve('.views.auth')
        except ImportError:
            # TODO: Find a better exception.
            raise Exception("""auth.uri.* key(s) were specified in config """
                    """but no auth views for package "%s" were found.""" % 
                                                                caller.__name__)

        if 'auth.uri.login' in settings:
            config.add_route('auth.uri.login', settings['auth.uri.login'])
            config.add_view(auth_views.login_view, route_name='auth.uri.login',
                            renderer=auth_views.login_view.renderer)

        if 'auth.uri.logout' in settings:
            config.add_route('auth.uri.logout', settings['auth.uri.logout'])
            config.add_view(auth_views.logout_view,
                            route_name='auth.uri.logout',
                            renderer=auth_views.logout_view.renderer)

        if 'auth.uri.after_logout' in settings:
            config.add_route('auth.uri.after_logout',
                                            settings['auth.uri.after_logout'])

    if 'authentication_policy' in settings:
        config.set_authentication_policy(settings['authentication_policy'])

    if 'authorization_policy' in settings:
        config.set_authorization_policy(settings['authorization_policy'])

    if 'root_factory' in settings:
        config.set_root_factory(settings['root_factory'])

    if 'static.mapping' in settings and settings['static.serve'] is True:
        static_map = settings['static.mapping']
        for name, value in static_map.items():
            path, cache_max_age = value
            config.add_static_view(name=name,
                                    path=path,
                                    cache_max_age=cache_max_age)

        def request_static_map(method):
            def _static_map(request, key, *path):
                directory, _ = static_map[key]
                return getattr(request, method)(os.path.join(directory, *path))
            return _static_map

        config.add_request_method(request_static_map('static_url'),
                                    name='static_map_url')
        config.add_request_method(request_static_map('static_path'),
                                    name='static_map_path')

    return config, settings


def core_factory(loader, global_config, **local_config):
    """
    """

    print("Initializing Platform Core...")
    init_settings(global_config)

    if global_config['database.enable']:
        print("    Database Models...")
        core.models.init_models(global_config)

    if all([global_config['auth.enable'],
            global_config['authn.models.enable'],
            global_config['database.enable']]):
        print("    Auth Models...")
        core.models.auth.init_auth_models(global_config)

    if global_config['auth.enable']:
        print("    Auth Policies...")
        core.auth.init_auth(global_config)

        global_config['authentication_policy'] = (
                                pharaoh.auth.auth_tkt_from_config(global_config,
                                    callback=core.auth.get_groups))

        global_config['authorization_policy'] = (
                                pyramid.authorization.ACLAuthorizationPolicy())

        RootFactory.__acl__ = global_config['authz.root_factory.permissions']
        global_config['root_factory'] = RootFactory

    global_config['composite'] = local_config

    return rutter.urlmap.urlmap_factory(loader, global_config, **local_config)