"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from webob import exc
from afpyrosite.model.meta import Session

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        ua = environ.get('HTTP_USER_AGENT', '').lower()
        if 'msie ' in ua:
            Session.remove()
            return exc.HTTPFound(location='http://www.w3junkies.com/toocool/')(environ, start_response)

        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()
