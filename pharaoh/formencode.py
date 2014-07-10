""" """
from __future__ import absolute_import


import logging
import json
import formencode
import pyramid.httpexceptions
import pharaoh.cors


def validate_view(params=None, match=None, headers=pharaoh.cors.gen_headers,
                   json=json,
                   invalid_params_exc=pyramid.httpexceptions.HTTPBadRequest,
                   invalid_match_exc=pyramid.httpexceptions.HTTPNotFound
                   ):
    """Basic validation decorator for usage in `view_config`.

    Takes `params` and `match` as arguments. 
        `params` - Schema to use to and instruct to validate requests.params
        `match` - Schema to use to and isntruct to validate request.match

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
                data = request.json_body or request.params
                try:
                    data = params.to_python(data)
                except formencode.Invalid as e:
                    logging.error("`validate_model` failed on request.params "
                                  "%s. Error: %s" % (data, e.msg))
                    body = json.dumps({'msg': e.unpack_errors()})
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
                    body = json.dumps({'msg': e.unpack_errors()})
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
