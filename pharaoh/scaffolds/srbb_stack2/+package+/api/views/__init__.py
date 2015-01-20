import time
import datetime
import pytz

import pyramid.view

from pprint import pprint


@pyramid.view.forbidden_view_config()
def api_forbidden_view(request):
    """Return HTTPUnauthorized when unauthorized API request is
    made."""
    return pyramid.httpexceptions.HTTPUnauthorized()


@pyramid.view.view_config(route_name="api_info", renderer="json",
                            permission="view")
def api_info(request):

    date_format = request.registry.settings['datetime.date_format']
    time_format = request.registry.settings['datetime.time_format']
    local_tz = request.registry.settings['datetime.local_timezone']

    utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    local_now = utc_now.astimezone(local_tz)

    return {
            'datetime': {
                'epoch_datetime': time.time(),
                'utc_date': utc_now.strftime(date_format),
                'local_date': local_now.strftime(date_format),
                'utc_time': utc_now.strftime(time_format),
                'local_time': local_now.strftime(time_format),
                'local_tz': local_tz.zone}}