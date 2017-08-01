"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('', '/', controller='docs', action='index')
    map.connect('rss', '/afpyro.rss', controller='docs', action='rss')
    map.connect('docs', '/{id}.html', controller='docs', action='docs')
    map.connect('dates', '/dates/{id}.html', controller='docs', action='dates')
    map.connect('date', "/dates/{year}/{id}.html",controller="docs", action="dates")
    map.connect('code', "/hg/{path_info:.*}", controller='hg', action='index')

    return map
