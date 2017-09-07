import os

from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.config import Configurator
from pyramid.events import NewRequest
from sqlalchemy import engine_from_config

# settings
#~ from pyramid.registry.Registry import settings

# security
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authentication import RemoteUserAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from lima.security import groupfinder

from urlparse import urlparse
try:
    import pymongo
    from gridfs import GridFS
except Exception as e:
    print('Module pymongo couldn\'t be imported: {e}'.format(e=e))

#~ from pyramid_formalchemy.resources import Models

from lima.models.models import *
#~ from lima.faforms import *

#~ from lima_routing import LimaRoutes
from lima_routing import (
    dashboard_include,
    ezinemanager_include,
    auctionmanager_include,
    ordermanager_include,
    customermanager_include,
    )


# variables
here = os.path.dirname(os.path.abspath(__file__))

#~ class ModelsWithACL(Models):
    #~ """A factory to override the default security setting"""
    #~ __acl__ = [
            #~ (Allow, 'admin', ALL_PERMISSIONS),
            #~ (Allow, Authenticated, 'view'),
            #~ (Allow, 'editor', 'edit'),
            #~ (Allow, 'manager', ('new', 'edit', 'delete')),
        #~ ]

def add_mongo_db(event):
    settings = event.request.registry.settings
    db = settings['mongo_db_conn'][settings['mongo_db_name']]
    event.request.mongo_db = db
    event.request.fs = GridFS(db)

def _add_routes(config):
    config.add_route('home',        '/')
    config.add_route('login',       '/login')
    config.add_route('logout',      '/logout')
    config.add_route('settings',    '/settings')
    config.add_route('help',        '/help')
    config.add_route('about',       '/about')
    config.add_route('eventtracker','/event-tracker/{source}')
    config.add_route('test',        '/test')
    config.add_route('ezine',       '/ezine/{type}/{name}.html')
    config.add_route('upload',      '/ezine/{id}/upload')
    config.add_route('json',        '/json/{model}{groupby:.*}')
    config.add_route('json_auctions', '/json_auctions/{view}/{filter}')
    config.add_route('action',      '/action/{action}')

def _add_rest_routes(config):
    # rest: prefix '/rest'
    config.add_route('rest_home',           '/{collection:[^/]*}')
    config.add_route('rest_object',         '/{collection}/{id:\d+}')
    config.add_route('rest_object_relation','/{collection}/{id:\d+}/{relation}')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    session_factory = UnencryptedCookieSessionFactoryConfig(
                            'RI8iA0A8vDootKiQQSivZCTj'
                            )
    # sql db settings
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    # TODO: moet dit in __init__ blijven? Verhuizen naar populate?
    Base.metadata.create_all(engine)
    config = Configurator(settings=settings,
                          session_factory=session_factory,
                          root_factory='lima.models.models.RootFactory')

    # security
    authn_policy = AuthTktAuthenticationPolicy(
                        'RI8iA0A8vDootKiQQSivZCTj',
                        callback=groupfinder,
                        hashalg='sha512')
    #~ authn_policy = RemoteUserAuthenticationPolicy(callback=groupfinder, debug=True)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    #~ config.set_default_permission('admin')
    #~ config.include('pyramid_whoauth')
    #~ config.include('pyramid_persona')

    # nosql db
    #~ commented out, might be implemented some day in the future...
    #~ mongo_db_uri = settings['mongo_db_uri']
    #~ conn = pymongo.Connection(mongo_db_uri)
    #~ config.registry.settings['mongo_db_conn'] = conn
    #~ config.add_subscriber(add_mongo_db, NewRequest)

    # pyramid_formalchemy's configuration
    #~ config.include('lima.fainit')
    #~ config.include('pyramid_formalchemy')
    #~ config.include('fa.jquery')
    #~ config.include('pyramid_fanstatic')

    # LiMA routing
    config.include(dashboard_include,       route_prefix='/Dashboard')
    config.include(ezinemanager_include,    route_prefix='/EzineManager')
    config.include(auctionmanager_include,  route_prefix='/AuctionManager')
    config.include(ordermanager_include,    route_prefix='/OrderManager')
    config.include(customermanager_include, route_prefix='/CustomerManager')
    """
    # register an admin UI (basic)
    config.formalchemy_admin('admin',
                             package='lima',
                             factory=ModelsWithACL,
                             )
    """
    """
    # register an admin UI (fa.jquery)
    config.formalchemy_admin('/admin',
                             package='lima',
                             forms=faforms,
                             #~ models=[VakBeEzine, AuctionEzine, Content, Offer, Auction, Relatie],
                             #~ view='lima:MM_ModelView',
                             view='fa.jquery.pyramid.ModelView',
                             factory=ModelsWithACL,
                             )
    """

    # register a custom model view
    #~ config.formalchemy_model('/ezines',
                             #~ package='lima',
                             #~ model='lima:models.Ezine',
                             #~ session_factory=DBSession,
                             #~ view='lima:P_ModelView',
                             #~ view='lima:MM_ModelView',
                             #~ )


    config.add_static_view(name=settings['gen_static_location'],
                           path='gen:static/',
                           cache_max_age=3600)

    config.add_static_view(name=settings['app_static_location'],
                           path='lima:static/',
                           cache_max_age=3600)

    config.add_static_view(name=settings['ezine_static_location'],
                           path='ezine:static/',
                           cache_max_age=3600)

    # routing
    config.include(_add_rest_routes,    route_prefix='/rest')
    _add_routes(config)

    config.scan()
    return config.make_wsgi_app()
