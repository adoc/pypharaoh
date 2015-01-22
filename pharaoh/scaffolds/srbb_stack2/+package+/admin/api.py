"""Hook API views.
Note: This module should not be loaded from `admin` initialization but
from `api` initialization.
"""

import pyramid.view

from {{project}} import db
from {{project}} import models


from pprint import pprint


@pyramid.view.view_config(route_name="admin_api_info", renderer="json",
                            permission="admin")
def api_admin_info(request):
    """
    """
    pprint(request.registry.settings)
    return {}


@pyramid.view.view_config(route_name="admin_api_users", renderer="json",
                            permission="admin")
def api_admin_users(request):
    """
    """
    # this_user = core.auth.get_this_user(request)

    # Temporary
    this_user = core.models.Session.query(core.models.auth.User).get(2)

    return (core.models.Session
                .query(core.models.auth.User)
                .filter(this_user.level >= core.models.auth.User.level)
                .all())