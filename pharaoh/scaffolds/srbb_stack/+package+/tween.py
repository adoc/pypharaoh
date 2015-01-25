"""
"""



def consume_queue():
    """
    """

    pass


# 
#
#


class _tween_factory(object):
    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

        # one-time configuration code goes here

    def __call__(self, request):
        # code to be executed for each request before
        # the actual application code goes here

        response = self.handler(request)

        # code to be executed for each request after
        # the actual application code goes here

        return response