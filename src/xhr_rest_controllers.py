#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  xhr_rest_controllers.py
#
#  Copyleft 2013 Mali Media Group
#  <admin@malimedia.be>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You can find the GNU General Public License on:
#  http://www.gnu.org/copyleft/gpl.html
#

from pyramid.view import (
    view_config,
    forbidden_view_config,
    view_defaults
    )
import lima.models.models as ModelsBase
from lima.models.models import DBSession
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError, IntegrityError
from sqlalchemy.orm.attributes import InstrumentedAttribute
from datetime import datetime
# i18n
from pyramid.i18n import (
    get_localizer,
    get_locale_name,
    TranslationStringFactory
    )
_ = TranslationStringFactory('Rest')
# logging
import logging
log = logging.getLogger(__name__)

# Constants
mapping = dict()
mapping['EzineItem_Auction'] = {
    'image'     : 'image',
    'title'     : 'title',
    'openprice' : 'openprice',
    'text'      : 'auct_intro',
}

@view_defaults(
        route_name=('rest_home'),
        )
class RestHome(object):
    """
    RestHome Class
    """
    def __init__(self, request):
        # We get a request anyway
        self.request    = request

    def __call__(self):
        return {}


@view_defaults(
        route_name=('rest_object'),
        xhr=True,
        renderer='json',
        )
class XhrRestController(object):
    """
    XhrRestController Class
    """
    def __init__(self, request):
        self.request    = request
        self.collection = request.matchdict['collection']
        self.cid        = request.matchdict['id']
        self.M          = self._get_model()
        self.data       = dict()
        self.response   = str()

    def __call__(self):
        return {}

    def _get_model(self):
        try:
            M = getattr(ModelsBase, str(self.collection))
        except AttributeError as e:
            raise
        else:
            return M

    def _set_model_attributes(self, m, controls):
        """
        TODO: doe in __init__
        PLUS: doe dit beter! Via een constante? Detectie van type?

        """
        for k,v in controls.iteritems():
            #~ log.debug('key: {k} | value: {v}'.format(k=k, v=v))
            if hasattr(m, k):
                try:
                    part = k.split('_')[1]
                except IndexError:
                    setattr(m, k, v)
                else:
                    if part == 'date':
                        setattr(m, k, datetime.strptime(v.split('+')[0], '%Y-%m-%dT%H:%M:%S'))
                    else:
                        setattr(m, k, v)
        return m

    @view_config(request_method='POST')
    def create_object(self):
        controls = self.request.POST
        """
        col_keys        = self.M.__table__.columns.keys()
        post_keys       = controls.keys()
        settable_cols   = filter(callback1, col_keys, post_keys)
        relations       = filter(callback2, col_keys, post_keys)
        """
        m = self.M()
        m = self._set_model_attributes(m, controls)
        if isinstance(m, ModelsBase.BiedmeeEzine):
            self._create_BiedmeeEzine(m)
        if isinstance(m, ModelsBase.Auction):
            self._create_Auction(m)
        else:
            try:
                DBSession.add(m)
            except SQLAlchemyError as e:
                self.response = _('Creation of "{m}" with id "{i}": FAILED. '
                            '{e}'.format(m=str(self.collection), i=self.cid, e=e))
                log.warning(self.response)
                self.request.response.status = 500
            except ProgrammingError as e:
                self.response = _('Creation of "{m}" with id "{i}": FAILED. '
                            '{e}'.format(m=str(self.collection), i=self.cid, e=e))
                log.warning(self.response)
                self.request.response.status = 500
            else:
                self.response = _('Creation of "{m}" with id "{i}": succes.'
                            ''.format(m=str(self.collection), i=self.cid))
                log.debug(self.response)
        return self.response

    @view_config(request_method='PUT')
    def update_object(self):
        controls = self.request.POST
        m = DBSession.query(self.M).filter(self.M.cid == self.cid).first()
        m = self._set_model_attributes(m, controls)
        if isinstance(m, ModelsBase.BiedmeeEzine):
            # first simply remove all relations to any auction
            m.ezine_items[:] = []
            # get new Auction id's
            auct_cids = self.request.params.getall('ezine_items_auctions')
            log.debug('auct_cids received: {a}'.format(a=str(auct_cids)))
            # set position to 1
            i = 1
            for auct_cid in auct_cids:
                log.debug(auct_cid)
                ezine_item  = ModelsBase.EzineItem(item_pos=i)
                auction     = DBSession.query(ModelsBase.Auction).filter(ModelsBase.Auction.cid == auct_cid).first()
                for k, v in mapping['EzineItem_Auction'].iteritems():
                    setattr(ezine_item, k, getattr(auction, v))
                ezine_item.auction = auction
                m.ezine_items.append(ezine_item)
                i += 1
        DBSession.add(m)
        try:
            self.response = m.name
        except AttributeError:
            self.response = m.title
        return self.response

    def _create_BiedmeeEzine(self, m):
        """ temp function """
        if 'ezine_items_auctions' in self.request.params:
            i = 1
            for id in self.request.params.getall('ezine_items_auctions'):
                log.debug(id)
                ezine_item  = ModelsBase.EzineItem(item_pos=i)
                auction     = DBSession.query(ModelsBase.Auction).filter(ModelsBase.Auction.cid == id).first()
                for k, v in mapping['EzineItem_Auction'].iteritems():
                    setattr(ezine_item, k, getattr(auction, v))
                ezine_item.auction = auction
                m.ezine_items.append(ezine_item)
                i += 1
        DBSession.add(m)
        try:
            DBSession.flush()
        except IntegrityError as e:
            self.response = _('Creation of "{m}" with id "{i}": FAILED. '
                        '{e}'.format(m=str(self.collection), i=self.cid, e=e))
            log.warning(self.response)
            self.request.response.status = 500
        except ProgrammingError as e:
            self.response = _('Creation of "{m}" with id "{i}": FAILED. '
                        '{e}'.format(m=str(self.collection), i=self.cid, e=e))
            log.warning(self.response)
            self.request.response.status = 500
        else:
            self.response = _('Creation of "{m}" with id "{i}": succes.'
                        ''.format(m=str(self.collection), i=str(m.cid)))
            log.debug(self.response)
        return self.response

    def _create_Auction(self, m):
        """ temp function """
        DBSession.add(m)
        try:
            DBSession.flush()
        except IntegrityError as e:
            self.response = _('Creation of "{m}" with id "{i}": FAILED. '
                        '{e}'.format(m=str(self.collection), i=self.cid, e=e))
            log.warning(self.response)
            self.request.response.status = 500
        except ProgrammingError as e:
            self.response = _('Creation of "{m}" with id "{i}": FAILED. '
                        '{e}'.format(m=str(self.collection), i=self.cid, e=e))
            log.warning(self.response)
            self.request.response.status = 500
        else:
            self.response = _('Creation of "{m}" with id "{i}": succes.'
                        ''.format(m=str(self.collection), i=str(m.cid)))
            log.debug(self.response)
        return self.response

    @view_config(request_method='GET')
    def retrieve_object(self):
        q = DBSession.query(self.M).filter(M.cid == self.cid)
        return {
            'values': q,
            }

    @view_config(request_method='DELETE')
    def delete_object(self):
        m = DBSession.query(self.M).filter(self.M.cid == self.cid).first()
        log.debug('Deletion request for "{m}" with id "{i}".'
                  ''.format(m=str(self.collection), i=self.cid))
        if not m:
            self.request.response.status = 404
            self.response = _('Deletion failed. Resource "{m}" with id "{i}" '
                        'not found.'.format(m=str(self.collection), i=self.cid))
            log.debug(self.response)
        else:
            try:
                DBSession.delete(m)
            except SQLAlchemyError as e:
                self.response = _('Deletion of "{m}" with id "{i}": FAILED. '
                        '{e}'.format(m=str(self.collection), i=self.cid, e=e))
                log.warning(self.response)
                self.request.response.status = 500
            else:
                self.response = _('Deletion of "{m}" with id "{i}": succes.'
                        ''.format(m=str(self.collection), i=str(m.cid)))
                log.debug(self.response)
        return self.response


@view_defaults(
        route_name=('rest_object_relation'),
        xhr=True,
        renderer='json',
        )
class XhrRestControllerRelations(object):
    """
    XhrRestControllerRelations Class
    """
    def __init__(self, request):
        self.request    = request
        self.collection = request.matchdict['collection']
        self.cid        = request.matchdict['id']
        self.relation   = request.matchdict['relation']
        self.M          = self._get_model()
        self.data       = dict()
        self.response   = str()

    def __call__(self):
        return {}

    def _get_model(self):
        try:
            M = getattr(ModelsBase, str(self.collection))
        except AttributeError as e:
            raise
        else:
            return M

    @view_config(request_method='PUT')
    def update_object(self):
        """
        controls = self.request.POST
        m = DBSession.query(self.M).filter(self.M.cid == self.cid).first()
        for k,v in controls.iteritems():
            if hasattr(m, k):
                try:
                    part = k.split('_')[1]
                except IndexError:
                    setattr(m, k, v)
                else:
                    if part == 'date':
                        setattr(m, k, datetime.strptime(v.split('+')[0], '%Y-%m-%dT%H:%M:%S'))
        if isinstance(m, ModelsBase.BiedmeeEzine):
            # first simply remove all relations to any auction
            #~ for item in m.ezine_items:
                #~ m.ezine_items.remove(item)
            m.ezine_items[:] = []   # doens't seem to work
            # get new Auction id's
            auct_cids = self.request.params.getall('ezine_items_auctions')
            log.debug('auct_cids received: {a}'.format(a=str(auct_cids)))
            # set position to 1
            i = 1
            for auct_cid in auct_cids:
                log.debug(auct_cid)
                ezine_item  = ModelsBase.EzineItem(item_pos=i)
                auction     = DBSession.query(ModelsBase.Auction).filter(ModelsBase.Auction.cid == auct_cid).first()
                for k, v in mapping['EzineItem_Auction'].iteritems():
                    setattr(ezine_item, k, getattr(auction, v))
                ezine_item.auction = auction
                m.ezine_items.append(ezine_item)
                i += 1
        DBSession.add(m)
        return m.name
        """
        return 'ok!'

    def _create_BiedmeeEzine(self, m):
        """ temp function """
        if 'ezine_items_auctions' in self.request.params:
            i = 1
            for id in self.request.params.getall('ezine_items_auctions'):
                log.debug(id)
                ezine_item  = ModelsBase.EzineItem(item_pos=i)
                auction     = DBSession.query(ModelsBase.Auction).filter(ModelsBase.Auction.cid == id).first()
                for k, v in mapping['EzineItem_Auction'].iteritems():
                    setattr(ezine_item, k, getattr(auction, v))
                ezine_item.auction = auction
                m.ezine_items.append(ezine_item)
                i += 1
        DBSession.add(m)
        try:
            DBSession.flush()
        except IntegrityError as e:
            self.response = _('Creation of "{m}" with id "{i}": FAILED. '
                        '{e}'.format(m=str(self.collection), i=self.cid, e=e))
            log.warning(self.response)
            self.request.response.status = 500
        except ProgrammingError as e:
            self.response = _('Creation of "{m}" with id "{i}": FAILED. '
                        '{e}'.format(m=str(self.collection), i=self.cid, e=e))
            log.warning(self.response)
            self.request.response.status = 500
        else:
            self.response = _('Creation of "{m}" with id "{i}": succes.'
                        ''.format(m=str(self.collection), i=str(m.cid)))
            log.debug(self.response)
        return self.response

    def _create_Auction(self, m):
        """ temp function """
        DBSession.add(m)
        try:
            DBSession.flush()
        except IntegrityError as e:
            self.response = _('Creation of "{m}" with id "{i}": FAILED. '
                        '{e}'.format(m=str(self.collection), i=self.cid, e=e))
            log.warning(self.response)
            self.request.response.status = 500
        except ProgrammingError as e:
            self.response = _('Creation of "{m}" with id "{i}": FAILED. '
                        '{e}'.format(m=str(self.collection), i=self.cid, e=e))
            log.warning(self.response)
            self.request.response.status = 500
        else:
            self.response = _('Creation of "{m}" with id "{i}": succes.'
                        ''.format(m=str(self.collection), i=str(m.cid)))
            log.debug(self.response)
        return self.response

    @view_config(request_method='GET')
    def retrieve_object(self):
        q = DBSession.query(self.M).filter(M.cid == self.cid)
        return {
            'values': q,
            }

    @view_config(request_method='DELETE')
    def delete_object(self):
        m = DBSession.query(self.M).filter(self.M.cid == self.cid).first()
        log.debug('Deletion request for "{m}" with id "{i}".'
                  ''.format(m=str(self.collection), i=self.cid))
        if not m:
            self.request.response.status = 404
            self.response = _('Deletion failed. Resource "{m}" with id "{i}" '
                        'not found.'.format(m=str(self.collection), i=self.cid))
            log.debug(self.response)
        else:
            try:
                DBSession.delete(m)
            except SQLAlchemyError as e:
                self.response = _('Deletion of "{m}" with id "{i}": FAILED. '
                        '{e}'.format(m=str(self.collection), i=self.cid, e=e))
                log.warning(self.response)
                self.request.response.status = 500
            else:
                self.response = _('Deletion of "{m}" with id "{i}": succes.'
                        ''.format(m=str(self.collection), i=str(m.cid)))
                log.debug(self.response)
        return self.response
