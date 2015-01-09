"""Initialize the core application services.
"""
import pyramid.settings

import core.models
import core.models.auth
import core.auth


def init_core(settings):
    """
    """

    database_enabled = pyramid.settings.asbool(settings.get('database.enable')) is True
    auth_enabled = pyramid.settings.asbool(settings.get('auth.enable')) is True
    authn_models_enabled = pyramid.settings.asbool(settings.get('authn.models.enable')) is True

    print(settings.get('database.enable'))

    if database_enabled:
        core.models.init_models(settings)

    if all([auth_enabled, authn_models_enabled, database_enabled]):
        core.models.auth.init_auth_models(settings)