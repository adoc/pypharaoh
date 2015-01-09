"""Initialize the core application services.
"""
import pyramid.settings

import core.models
import core.models.auth
import core.auth


def init_settings(settings, config):
    """Set application specific settings."""


    settings['datetime.date_format'] = settings.get('datetime.date_format',
                                                    '%Y-%m-%d')
    settings['datetime.time_format'] = settings.get('datetime.time_format',
                                                    '%I:%M:%S%p')
    settings['database.enable'] = pyramid.settings.asbool(
                                        settings.get('database.enable', False))
    settings['database.epoch'] = settings.get('database.epoch', '1970-1-1')
    settings['database.timezone'] = settings.get('database.timezone', 'UTC')
    settings['database.initialize.drop_all'] = pyramid.settings.asbool(
                            settings.get('database.initialize.drop_all', False))
    settings['auth.enable'] = pyramid.settings.asbool(
                                            settings.get('auth.enable', False))
    settings['auth.get_user_func'] = config.maybe_dotted(
                settings.get('auth.get_user_func', 'core.models.auth:get_user'))

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

def init_core(settings, config):
    """
    """

    print('"%s"' % settings['datetime.date_format'])

    init_settings(settings, config)



    if settings['database.enable']:
        core.models.init_models(settings)

    if all([settings['auth.enable'],
            settings['authn.models.enable'],
            settings['database.enable']]):
        core.models.auth.init_auth_models(settings)