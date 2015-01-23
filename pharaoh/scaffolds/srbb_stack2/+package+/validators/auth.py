"""Core package Authentication validators.
"""


import formencode


def init(config, settings):
    """
    """

    global LoginSchema

    class LoginSchema(formencode.schema.Schema):
        allow_extra_fields = True
        filter_extra_fields = True
        ignore_key_missing = True

        login = formencode.validators.String(min=3,
                                max=settings['auth.allow_email_login'] is True
                                    and 128 or 64, if_missing=None)
        password = formencode.validators.String(min=4, max=128, if_missing=None)