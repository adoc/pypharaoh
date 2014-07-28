""" """
from __future__ import absolute_import


import logging
import json
import formencode
import pyramid.httpexceptions
import pharaoh.cors


class BadMatch(pyramid.httpexceptions.HTTPNotFound):
    """
    """
    pass


class BadParams(pyramid.httpexceptions.HTTPBadRequest):
    """
    """
    pass




"""
Implemented

    decorators=(validate_view(),)
"""


def validate_view2(params=None, match=None, variable_decode=True,
                 variable_decode_dict_char=".", variable_decode_list_char="-",
                 reify_params=True, reify_match=True, raise_exc=True,
                 json_exc=False,
                 invalid_params_exc=BadParams, invalid_match_exc=BadMatch,
                 exc_headers_func=pharaoh.cors.gen_headers,
                 valid_params_attr="validated_params",
                 valid_match_attr="validated_match",
                 invalid_params_attr="error_params",
                 invalid_match_attr="error_match"):

    params_schema = callable(params) and params() or params
    match_schema = callable(match) and match() or match

    if (params_schema is None and
            match_schema is None):
        raise ValueError("`validate_view` expected a `params` or `match` "
                         "Formencode schema.")

    if (params_schema and 
        not isinstance(params_schema, (formencode.Schema,
                                       formencode.FancyValidator))):
        raise ValueError("`validate_view` expects `params` to be a "
                         "Formencode Schema or FancyValidator.")

    if (match_schema and 
        not isinstance(match_schema, (formencode.Schema,
                                      formencode.FancyValidator))):
        raise ValueError("`validate_view` expects `match` to be a "
                         "Formencode Schema or FancyValidator.")

    def _decorator(view_callable):
        def _decorated_view(context, request):
            def _raise(exc, msgdata):
                # Prepare and raise exception.
                exc_params = {'headers': exc_headers_func(request)}
                if json_exc is True:
                    exc_params['body'] = json.dumps({'msg': msgdata})
                raise exc(**exc_params)

            def validate_params(context):
                """Method to handle the validation of `request.params`.
                """
                try:
                    data = request.json_body
                except ValueError:
                    data = request.params

                if variable_decode is True:
                    data = formencode.variabledecode.variable_decode(data,
                                        dict_char=variable_decode_dict_char,
                                        list_char=variable_decode_list_char)

                try:
                    return params_schema.to_python(data)
                except formencode.Invalid as exc:
                    unpacked = exc.unpack_errors()
                    logging.warning("Formencode validation errors: %s" % unpacked)
                    request.set_property(lambda ctx: unpacked,
                                         invalid_params_attr, reify=True)
                    if raise_exc is True:
                        _raise(invalid_params_exc, unpacked)
                    else:
                        return {}

            def validate_match(context):
                """Method to handle the validation of `request.matchdict`.
                """
                try:
                    return match_schema.to_python(request.matchdict)
                except formencode.Invalid as exc:
                    unpacked = exc.unpack_errors()
                    request.set_property(lambda ctx: unpacked,
                                         invalid_match_attr, reify=True)
                    if raise_exc is True:
                        _raise(invalid_match_exc, unpacked)
                    else:
                        return {}

            if params_schema:
                request.set_property(validate_params, valid_params_attr,
                                        reify=reify_params)
            if match_schema:
                request.set_property(validate_match, valid_match_attr,
                                        reify=reify_params)

            return view_callable(context, request)
        return _decorated_view
    return _decorator

class ValidView:
    """An even more advanced version of "validate_view".
    """
    # No clue how to get class based decorators working on pyramid views... sigh

    def __validate_imp(self):
        # Validate the implementation.
        if (self._params_schema is None and
                self._match_schema is None):
            raise ValueError("`validate_view` expected a `params` or `match` "
                             "Formencode schema.")

        if (self._params_schema and 
            not isinstance(self._params_schema, (formencode.Schema,
                                          formencode.FancyValidator))):
            raise ValueError("`validate_view` expects `params` to be a "
                             "Formencode Schema or FancyValidator.")

        if (self._match_schema and 
            not isinstance(self._match_schema, (formencode.Schema,
                                          formencode.FancyValidator))):
            raise ValueError("`validate_view` expects `match` to be a "
                             "Formencode Schema or FancyValidator.")

    def __init__(self, params=None, match=None,
                 reify_params=True, reify_match=True,
                 raise_exc=True, json_exc=False,
                 invalid_params_exc=BadParams,
                 invalid_match_exc=BadMatch,
                 exc_headers_func=pharaoh.cors.gen_headers,
                 valid_params_attr="validated_params",
                 valid_match_attr="validated_match",
                 invalid_params_attr="error_params",
                 invalid_match_attr="error_match"):
        """
        """
        # Schema can be passed instantiated or as the class. Simply
        # instantiate if it's a class.
        self._params_schema = callable(params) and params() or params
        self._match_schema = callable(match) and match() or match

        self._reify_params = reify_params
        self._reify_params = reify_match
        self._raise_exc = raise_exc
        self._json_exc = json_exc
        self._invalid_params_exc = invalid_params_exc
        self._invalid_match_exc = invalid_match_exc
        self._exc_headers_func = exc_headers_func
        self._valid_params_attr = valid_params_attr
        self._valid_match_attr = valid_match_attr
        self._invalid_params_attr = invalid_params_attr
        self._invalid_match_attr = invalid_match_attr

        self.__validate_imp()

    def __call__(self, view_callable):
        print("__call__")
        self._view_callable = view_callable
        #self.validated_view.__func__.__wraps__ = view_callable
        def wrapper(*args):
            return self.validated_view(*args)

        return wrapper
        #return view_callable

    def _validate_params(self):
        # Do validate params.
        # Check for a `json_body` first, otherwise get `params`.
        try:
            data = self.__request.json_body
        except ValueError:
            data = self.__request.params

        return self._params_schema.to_python(data)

    def _validate_match(self):
        # Do validate match.
        return self._match_schema.to_python(self.__request.matchdict)

    def _raise(self, exc, data):
        exc_params = {'headers': self._exc_headers_func(self.__request)}
        if self._json_exc is True:
            exc_params['body'] = json.dumps({'msg': data})
        raise exc(**exc_params)

    def validate_params(self, ctx):
        """Method to handle the validation of `request.params`.
        """
        try:
            return self._validate_params()
        except formencode.Invalid as exc:
            unpack = exc.unpack_errors()
            self.__request.set_property(lambda: unpack,
                                        self._invalid_params_attr,
                                        reify=True)
            if self._raise_exc is True:
                self._raise(self._invalid_params_exc, unpack)

    def validate_match(self):
        """Method to handle the validation of `request.matchdict`.
        """
        try:
            return self._validate_match()
        except formencode.Invalid as exc:
            unpack = exc.unpack_errors()
            self.__request.set_property(exc.unpack_errors,
                                        self._invalid_match_attr,
                                        reify=True)
            if self._raise_exc is True:
                self._raise(self._invalid_match_exc, unpack)

    def validated_view(self, context, request):
        """Validate and execute `view_callable`.
        """
        print("validated_view")
        self.__request = request

        if self._params_schema:
            request.set_property(self.validate_params, self._valid_params_attr,
                                    reify=self._reify_params)
        if self._match_schema:
            request.set_property(self.validate_match, self._valid_match_attr,
                                    reify=self._reify_params)

        return self._view_callable(context, request)




def validate_view(params=None, match=None, headers=pharaoh.cors.gen_headers,
                   json=json,
                   json_errors=True,
                   invalid_params_exc=BadMatch,
                   invalid_match_exc=BadParams
                   ):
    """Basic validation decorator for usage in `view_config`.

    Takes `params` and `match` as arguments. 
        `params` - Schema to use to and instruct to validate requests.params
        `match` - Schema to use to and instruct to validate request.match

    Usage in @view_config():
        decorators=(validate_model(params=ParamsSchema,
                                   headers=config.headers)

    """
    
    if params is None and match is None: # Validate the usage of the validator!
        raise ValueError("`validate_model` expected a `params` schema or a "
                         "`match` schema.")

    # Check to see if Validator works as well.
    if params and issubclass(params, (formencode.Schema,
                                      formencode.FancyValidator)):
        params = params()
    elif params is not None:
        raise ValueError("`params` expected a `formencode.Schema` type.")

    if match and issubclass(match, (formencode.Schema,
                                    formencode.FancyValidator)):
        match = match()
    elif match is not None:
        raise ValueError("`match` expected a `formencode.Schema` type.")

    def _decorator(view_callable):
        def _inner(context, request):
            def validate_params(this):
                try:
                    data = request.json_body
                except ValueError:
                    data = request.params

                try:
                    data = params.to_python(data)
                except formencode.Invalid as e:
                    logging.error("`validate_model` failed on request.params "
                                  "%s. Error: %s" % (data, e.msg))

                    if json_errors is True:
                        body = json.dumps({'msg': e.unpack_errors()})
                    else:
                        body = "" #e.unpack_errors()

                    raise invalid_params_exc(headers=headers(request),
                                                                body=body)
                else:
                    return data

            def validate_match(this):
                try:
                    print(request.matchdict)
                    data = match.to_python(request.matchdict)
                except formencode.Invalid as e:
                    logging.error("`validate_model` failed on request.matchdict"
                                  " %s." % request.matchdict)

                    if json_errors is True:
                        body = json.dumps({'msg': e.unpack_errors()})
                    else:
                        body = "" #e.unpack_errors()

                    raise invalid_match_exc(headers=headers(request),
                                                              body=body)
                else:
                    return data

            if params:
                request.set_property(validate_params, 'validated_params',
                                        reify=True)
            if match:
                request.set_property(validate_match, 'validated_matchdict',
                                        reify=True)
            return view_callable(context, request)
        return _inner
    return _decorator
