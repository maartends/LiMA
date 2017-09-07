import logging

log = logging.getLogger(__name__)

def dashboard_include(config):
    config.add_route('Dashboard', '/')
    log.info('LiMA Dashboard routes loaded')

def ezinemanager_include(config):
    config.add_route('EzineManager',    '/')
    config.add_route('ezine_view',      '/ezine/{id}/view')
    config.add_route('content_view',    '/content/{id}/view')
    config.add_route('content_edit',    '/content/{id}/edit')
    config.add_route('ezine_crud_view', '/crud/{model}/{id}')
    log.info('LiMA EzineManager routes loaded')

def auctionmanager_include(config):
    config.add_route('AuctionManager',      '/')
    config.add_route('auction_view',        '/auction/{id}/view')
    config.add_route('AuctionManager_auction', '/auction/{id}/{action}')
    log.info('LiMA AuctionManager routes loaded')

def ordermanager_include(config):
    config.add_route('OrderManager', '/')
    config.add_route('OrderManager_order', '/order/{id}/{action}')
    log.info('LiMA OrderManager routes loaded')

def customermanager_include(config):
    config.add_route('CustomerManager', '/')
    config.add_route('CustomerManager_customer', '/customer/{id}/{action}')
    log.info('LiMA CustomerManager routes loaded')
