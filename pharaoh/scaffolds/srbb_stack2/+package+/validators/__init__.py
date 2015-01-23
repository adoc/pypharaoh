"""Core package validators.
"""

import re


_alpha = re.compile('[\W_]+')


def init(config, settings):
    global month_style

    month_style = _alpha.sub('', settings['datetime.date_format']).lower()

