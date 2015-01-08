"""Initialize the core application services.
"""

import sqlalchemy
import pyramid.authorization
import pharaoh.auth

import core.models
import core.auth


def init_core(settings):
    """
    """

    database_enabled = settings.get('database.enable') is True
    auth_enabled = settings.get('auth.enable') is True
    authn_models_enabled = settings.get('authn.models.enable') is True

    if database_enabled:
        core.models.init_models(settings)

    if all([auth_enabled, authn_models_enabled, database_enabled]):
        core.models.auth.init_auth_models(settings)