#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  views.py
#
#  Copyleft 2014 Mali Media Group
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
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#

from __future__ import (
    absolute_import,
    unicode_literals
    )
import logging
import requests
from pyramid.view import (
    view_config,
    forbidden_view_config,
    )
from pyramid.renderers import render_to_response, render
from pyramid.httpexceptions import HTTPFound, HTTPOk
from pyramid.exceptions import Forbidden
from formalchemy import FieldSet, Grid
#~ from faforms import FieldSet, Grid
from fa.jquery.utils import Flash
from .run import Runner

from lima.models.models import *
import transaction
from .malimedia.helpers.helper import Helper

# SQLAlchemy
from sqlalchemy import desc

# security
from .security import USERS
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    unauthenticated_userid,
    effective_principals,
    )

from .helpers import RawSqlConstruct
from lima.malimedia.html.premailer import Premailer
from .malimedia.mailers import Mailjet

# custom template filters
from .template_filters.chameleon.filters import templateFilters

# get logger
log = logging.getLogger(__name__)

# sort dictionary
def sortedDictValues3(adict):
    keys = adict.keys()
    keys.sort()
    return map(adict.get, keys)

@view_config(route_name ='home',
             renderer   ='templates/index.html.pt',
             permission ='admin')
def home_view(request):
    ezines      = DBSession.query(Ezine).order_by(desc(Ezine.send_date))
    auctions    = DBSession.query(Auction).order_by(desc(Auction.cid))
    return {
        'Ezines'    : ezines,
        'Auctions'  : auctions,
        }

@view_config(route_name='Dashboard',
             renderer='templates/index.html.pt',
             permission='admin')
def Dashboard_view(request):
    ezines = DBSession.query(Ezine).order_by(desc(Ezine.send_date))
    auctions    = DBSession.query(Auction).order_by(desc(Auction.cid))
    return {
        'Ezines'    : ezines,
        'Auctions'  : auctions,
        'c_data'    : False,
        }

@view_config(route_name='EzineManager',
             renderer='templates/EzineManager/home.html.pt',
             permission='admin')
def EzineManager_view(request):
    ezines      = DBSession.query(Ezine).order_by(desc(Ezine.send_date))
    auctions    = DBSession.query(Auction).order_by(desc(Auction.cid))
    reports     = DBSession.query(ClangMailjetSyncReport).order_by(desc(ClangMailjetSyncReport.cid))
    return {
        'Ezines'    : ezines,
        'Auctions'  : auctions,
        'c_data'    : False,
        'Auction'   : False,
        'reports'   : reports,
        }

@view_config(route_name='AuctionManager',
             renderer='templates/AuctionManager/home.html.pt',
             permission='admin')
def AuctionManager_view(request):
    auctions    = DBSession.query(Auction).order_by(desc(Auction.cid))
    return {
        'Auctions'  : auctions,
        'c_data'    : False,
        }

@view_config(route_name='CustomerManager',
             renderer='templates/customermanager.html.pt',
             permission='admin')
def CustomerManager_view(request):
    auctions    = DBSession.query(Auction).order_by(desc(Auction.cid))
    return {
        'Auctions'  : auctions,
        'c_data'    : False,
        }

@view_config(route_name='CustomerManager_customer',
             renderer='templates/CustomerManager/customer_xhr.html.pt',
             permission='admin')
def CustomerManager_customer_view(request):
    s = RawSqlConstruct()
    sql = s.viewcustomer(request)
    try:
        c = DBSession.connection()
        c.execute('commit')
        res = c.execute(sql).fetchall()
        c.close()
        for i in res:
            data = dict((k, serialize_value(v)) for (k, v) in i.items())
    except Exception as e:
        request.session.flash('FAILED: {e}'.format(e=e))
        log.warning('FAILED: {e}'.format(e=e))
        data = e
    return {
        'customer': data,
    }

@view_config(route_name='AuctionManager_auction',
             renderer='templates/AuctionManager/auction_xhr.html.pt',
             permission='admin')
def AuctionManager_auction_view(request):
    s = RawSqlConstruct()
    sql = s.viewauction(request)
    try:
        c = DBSession.connection()
        c.execute('commit')
        res = c.execute(sql).fetchall()
        c.close()
        for i in res:
            data = dict((k, serialize_value(v)) for (k, v) in i.items())
    except Exception as e:
        request.session.flash('FAILED: {e}'.format(e=e))
        log.warning('FAILED: {e}'.format(e=e))
        data = e
    return {
        'auction': data,
    }

@view_config(route_name='auction_view',
             renderer='templates/AuctionManager/auction-view.html.pt',
             permission='admin')
def auction_view_view(request):
    id = request.matchdict['id']
    auctions    = DBSession.query(Auction).order_by(desc(Auction.cid))
    auction     = DBSession.query(Auction).filter(Auction.cid==id).first()
    return {
        'Auctions'    : auctions,
        'Auction'     : auction,
        'c_data'    : True,
        }

@view_config(route_name='OrderManager_order',
             renderer='templates/OrderManager/order_xhr.html.pt',
             permission='admin')
def OrderManager_order_view(request):
    s = RawSqlConstruct()
    sql = s.vieworder(request)
    try:
        c = DBSession.connection()
        c.execute('commit')
        res = c.execute(sql).fetchall()
        c.close()
        for i in res:
            data = dict((k, serialize_value(v)) for (k, v) in i.items())
    except Exception as e:
        request.session.flash('FAILED: {e}'.format(e=e))
        log.warning('FAILED: {e}'.format(e=e))
        data = e
    return {
        'order': data,
    }

@view_config(route_name='OrderManager',
             renderer='templates/ordermanager.html.pt',
             permission='admin')
def OrderManager_view(request):
    return {
        'c_data': False,
        }

@view_config(route_name='settings',
             renderer='templates/settings.html.pt',
             permission='admin')
def settings_view(request):
    settings = ''
    return {'c_data': False,}

@view_config(route_name='help',
             renderer='templates/help.html.pt',
             permission='admin')
def help_view(request):
    return {'c_data': False,}

@view_config(route_name='help',
             renderer='templates/help_xhr.html.pt',
             permission='admin',
             xhr=True)
def help_view_xhr(request):
    return {'c_data': False,}

@view_config(route_name='about',
             renderer='templates/about.html.pt',
             permission='admin')
def about_view(request):
    return {'c_data': False,}

@view_config(route_name='about',
             renderer='templates/about_xhr.html.pt',
             permission='admin',
             xhr=True)
def about_view_xhr(request):
    import pkg_resources
    lima_info = pkg_resources.get_distribution('Lima')
    return {'lima_info': lima_info, 'c_data': False,}

@view_config(route_name='ezine', permission='view')
def ezine_view(request):
    t = templateFilters()
    name = request.matchdict['name']
    type = request.matchdict['type']
    renderer= '/'.join(('templates', 'ezines', type, 'ezine.html.pt'))
    ezine = DBSession.query(Ezine).filter(Ezine.name==name).first()
    debug = False
    mailer = 'mailjet'
    if request.GET:
        g = request.GET
        if 'action' in g:
            if g['action'] == 'download':
                request.response.content_disposition = 'attachment; file-name={n}.html'.format(n=name)
        if 'mailer' in g:
            mailer = g['mailer'] if g['mailer'] in ['mailjet', 'clang'] else 'mailjet'
    return render_to_response(renderer,
                              {'Ezine': ezine,
                               'mailer': mailer,
                               'templateFilters': t,
                               'debug': debug,},
                               request=request)

@view_config(route_name='ezine_view',
             renderer='templates/EzineManager/ezine-view.html.pt',
             permission='admin')
def ezine_view_view(request):
    id = request.matchdict['id']
    ezines      = DBSession.query(Ezine).order_by(desc(Ezine.send_date))
    auctions    = DBSession.query(Auction).order_by(desc(Auction.cid))
    ezine       = DBSession.query(Ezine).filter(Ezine.cid==id).first()
    return {
        'Ezines'    : ezines,
        'Auctions'  : auctions,
        'Ezine'     : ezine,
        }

@view_config(route_name='content_view',
             renderer='templates/EzineManager/content-view.html.pt',
             permission='admin')
def content_view_view(request):
    id = request.matchdict['id']
    ezines      = DBSession.query(Ezine).order_by(desc(Ezine.send_date))
    auctions    = DBSession.query(Auction).order_by(desc(Auction.cid))
    auction     = DBSession.query(Auction).filter(Auction.cid==id).first()
    return {
        'Ezines'    : ezines,
        'Auctions'  : auctions,
        'Auction'   : auction,
        'c_data'    : True,
        }

@view_config(route_name='content_edit',
             renderer='templates/EzineManager/rest-items.html.pt',
             permission='admin',
             xhr=True)
def content_view_view_xhr(request):
    id = request.matchdict['id']
    ezines      = DBSession.query(Ezine).order_by(desc(Ezine.send_date))
    auctions    = DBSession.query(Auction).order_by(desc(Auction.cid))
    auction     = DBSession.query(Auction).filter(Auction.cid==id).first()
    return {
        'Ezines'    : ezines,
        'Auctions'  : auctions,
        'Auction'   : auction,
        'c_data'    : True,
        }

@view_config(route_name='content_view',
             renderer='templates/EzineManager/content-view-xhr.html.pt',
             permission='admin',
             xhr=True)
def content_view_view_xhr(request):
    t = templateFilters()
    Ezine = dict()
    Ezine['name'] = 'preview'
    id = request.matchdict['id']
    a = DBSession.query(Auction).filter(Auction.cid==id).first()
    return {
        'templateFilters': t,
        'item': a,
        'Ezine': Ezine,
        }

@view_config(route_name='ezine_crud_view',
             renderer='templates/EzineManager/ezine-view.html.pt',
             permission='admin')
def ezine_crud_view_view(request):
    id = request.matchdict['id']
    ezines = DBSession.query(Ezine).order_by(desc(Ezine.send_date))
    ezine = DBSession.query(Ezine).filter(Ezine.cid==id).first()
    debug = False
    ezine_file = '.'.join((ezine.name.lower(), 'html'))
    ezine_size = None
    return {
        'Ezines': ezines,
        'Ezine': ezine,
        'ezine_file': ezine_file,
        'ezine_size': ezine_size,
        }

@view_config(route_name='eventtracker',
             renderer='json')
def event_tracker(request):
    s = request.matchdict['source']
    log.debug('Event source is: "{s}".'.format(s=s))
    try:
        b = request.json_body
    except ValueError as e:
        log.error('No JSON body detected...')
    else:
        t = b['event']
        log.debug('Event type is: "{t}".'.format(t=t))
        # Send event and parameters to Clang
        r = requests.post('http://myclang.com/3/3fde87cb23a1c092d24365d696c5c6f35363b6c443056753e2e096a031c2b527e2b4a2c666c6d1a4420094a',
                          data=b)
        log.debug('Status code: "{c}".'.format(c=r.status_code))
    return {}

@view_config(route_name='json', renderer='json', permission='admin')
def json_view(request):
    json = list()
    grouper = False
    #~ c = DBSession.connection()
    model = request.matchdict['model']
    ezines_query = DBSession.query(globals()[model])
    assert model in globals(), model + ' is not a valid class name '\
                                       '(valid Classnames in models.py)'
    groupby = request.matchdict['groupby'].strip('/')
    if groupby:
        grouper = list()
        #~ for v in ezines_query.distinct(groupby):
            #~ grouper.append(v)
        #~ grouper = c.execute('SELECT DISTINCT {g} FROM ezines;'.format(g=groupby)).all()
        #~ grouper = ezines_query.distinct(groupby)
        #~ grouper = ezines_query.filter(getattr(globals()[model], groupby)
    if request.GET:
        # for now we only support one filter criterium
        assert len(request.GET.keys()) == 1, 'for now we only support one '\
                                             'filter criterium'
        ft = request.GET.keys()[0]
        fv = request.GET[ft]
        ezines = ezines_query.filter(getattr(globals()[model], ft) == fv).all()
    else:
        ezines = ezines_query.all()
    for i in ezines:
        json.append(i.serialize)
    debug = False
    return {
        'identifier': 'id',
        'label': 'name',
        'groupby': groupby,
        #~ 'grouper': ezines_query,
        'items': json,
        }

def serialize_value(v):
    from decimal import Decimal
    from datetime import datetime
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, datetime):
        return v.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return v

@view_config(route_name='json_auctions', renderer='json', permission='view')
def json_auctions_view(request):
    """
    json_auctions_view
    route form: '/json_auctions/{view}/{filter}'
    used for:
    view | filter
        - topauctions    | query:startdate=, enddate=
        - charts         | week, mpnth
        - filterselect   | partner_titel
    """
    # initialize final vars
    identifier =    'id'
    json       =    list()
    item_count =    0
    max_values =    dict()
    totals     =    dict()
    avgs       =    dict()
    filter     =    request.matchdict['filter']

    s = RawSqlConstruct(request)
    sql = s.as_string()

    if request.matchdict['view'] == 'topauctions':
        identifier = 'dist'
    elif request.matchdict['view'] == 'charts':
        identifier = 'ident'

    try:
        c = DBSession.connection()
        c.execute('commit')
        res = c.execute(sql).fetchall()
        c.close()
    except Exception as e:
        request.session.flash('SQL FAILED! SQL was {s}: {e}'.format(s=s, e=e))
        log.warning('SQL FAILED! SQL was {s}. Error: {e}'.format(s=s, e=e))
    else:
        item_count = len(res)
        for i in res:
            r = dict((k, serialize_value(v)) for (k, v) in i.items())
            json.append(r)
        if request.matchdict['view'] == 'charts':
            for i in json[0].keys():
                if i in ('week', 'month', 'omzet', 'n'):
                    max_values[i] = (max(row[i] for row in json))
            if 'format' in request.GET:
                format = request.GET['format']
                if format == 'gdatatable':
                    import gviz_api
                    # Creating the data
                    description = {filter   : ("string", filter.title()),
                                   "n"      : ("number", "Number"),
                                   "revenue": ("number", "Revenue"),
                                   }
                    # Loading it into gviz_api.DataTable
                    data_table = gviz_api.DataTable(description)
                    data_table.LoadData(json)
                    # Creating a JSon string
                    json = data_table.ToJSon(columns_order=(filter, "n"),
                                             order_by=filter)
                    return render_to_response('string', json)

        if request.matchdict['view'] == 'topauctions':
            totals['eur_tot_marge'] = sum( [x['eur_tot_marge'] for x in json if x['eur_tot_marge'] is not None] )
            totals['occ'] = sum( [x['occ'] for x in json if x['occ'] is not None] )
            l = [x['proc_marge'] for x in json if x['proc_marge'] is not None]
            avgs['proc_marge'] = round(sum(l) / len(l), 1)
    return {
        'identifier'    : identifier,
        'items'         : json,
        'item_count'    : item_count,
        'max_values'    : max_values,
        'totals'        : totals,
        'avgs'          : avgs,
    }

@view_config(route_name='action', renderer='json', xhr=True)
def action_view_xhr(request):

    def render_ezine(ezine, mailer):
        """Render Ezine for a certain mass mailer"""
        t = templateFilters()
        renderer = 'lima:' + '/'.join(('templates', 'ezines',
                                       'biedmee', 'ezine.html.pt'))
        # Render to html
        try:
            html = render(renderer, {'Ezine': ezine, 'mailer': mailer,
                                     'templateFilters': t, 'debug': False,},
                                    request=request)
        except Exception as e:
            m = e.message if bool(len(e.message)) else e.reason
            log.error('Rendering failed: {m}.'.format(m=m))
            response += 'Rendering failed: {m}.\n'.format(m=m)
            mailjet_ok = False
        else:
            ezine.html = html
            # Premail html
            log.info('Premailing ezine...')
            prem = Premailer(local=True)
            d = prem.premail(ezine, to_file=True)
            ezine.html_pre = d['documents']['html']
            ezine.txt = d['documents']['txt']

    json = list()
    url = ''
    action = request.matchdict['action']
    response = 'Nothing happened...'
    p = request.POST
    ezine_cid = p['id']
    mailjet_ok  = True
    clang_ok    = True
    if action == 'update_veilingen_db':
        if request.POST:
            url = request.POST['url']
            try:
                response = Helper().update_veilingen_db(url)
                log.info('New file written to: {o}'.format(o='/tmp/sheet2copy.csv'))
            except Exception as e:
                response = e
                request.session.flash('Database updating FAILED: {e}'.format(e=response))
            s = RawSqlConstruct()
            sql = s.update_veilingen_db()
            try:
                c = DBSession.connection()
                c.execute('commit')
                c.execute(sql)
                c.close()
                log.info('New table(s) created')
            except Exception as e:
                response = e
                request.session.flash('Table creation FAILED: {e}'.format(e=response))
                log.warning('Table creation FAILED: {e}'.format(e=response))
        else:
            url = 'wrong'
            response = 'wrong'
    elif action == 'upload_to_clang':
        ezine = DBSession.query(Ezine).filter(Ezine.cid==ezine_cid).first()
        debug = False
        ezine_file = '.'.join((ezine.name.lower(), 'html'))
        try:
            r = Runner()
            r.main(ezine, request)
            response = 'Ezine "{n}" werd gepremailed en geüpload naar Clang'.format(n=ezine.name)
        except Exception as e:
            response = e
    elif action == 'upload_ezine':
        response = ''
        log.debug(p)
        ezine = DBSession.query(Ezine).filter(Ezine.cid==ezine_cid).first()

        # upload to Mailjet?
        if 'opt_tomailjet' in p:
            # Render ezine to html first
            render_ezine(ezine, 'mailjet')
            log.info('Uploading "{n}" to Mailjet...'.format(n=ezine.name))
            m = Mailjet(request)
            try:
                campaign_id = m.upload(ezine)
            except Exception as e:
                m = e.message if bool(len(e.message)) else e.reason
                log.error('Maljet upload failed with message: {m}.'.format(m=m))
                response += 'Maljet upload failed with message: {m}.\n'.format(m=m)
                mailjet_ok = False
            else:
                mailjet_ok = True
                response += 'Ezine "{n}" werd gepremailed en geüpload naar Mailjet.\n'.format(n=ezine.name)
        else:
            log.debug('Upload to mailjet not selected.')

        if 'opt_sendtestmailjet' in p and mailjet_ok:
            log.info('Testsending "{n}" via Mailjet...'.format(n=ezine.name))
            m = Mailjet(request)
            try:
                m.send_test(campaign_id, p['testaddress'])
            except Exception as e:
                response += 'Send test through mailjet failed: '\
                            '{m}.\n'.format(m=e.message)
            else:
                response += 'Ezine "{n}" werd via Mailjet verzonden naar '\
                            '{e}.\n'.format(n=ezine.name, e=p['testaddress'])
        else:
            log.debug('Sending test via mailjet not selected.')

        # upload to Clang?
        if 'opt_toclang' in p:
            # Render ezine to html first
            render_ezine(ezine, 'clang')
            log.info('Uploading "{n}" to Clang...'.format(n=ezine.name))
            debug = False
            ezine_file = '.'.join((ezine.name.lower(), 'html'))
            try:
                r = Runner(request)
                r.main(ezine)
            except Exception as e:
                response += e.message + '\n'
                clang_ok = False
            else:
                clang_ok = True
                response += 'Ezine "{n}" werd gepremailed en geüpload '\
                             'naar Clang.\nTest werd verzonden naar '\
                             'GroepID "4".'.format(n=ezine.name)
        else:
            log.debug('Upload to Clang not selected.')

        if 'opt_sendtestclang' in p and clang_ok:
            log.debug('Sending test via clang...')
        else:
            log.debug('Not sending test via clang...')

    log.debug('Response sent to browser: '
               '"{r}"'.format(r=response.replace('\n', ' ')))

    return {
        'url': url,
        'action': action,
        'response': response,
        }

@view_config(route_name='test',
             renderer='templates/test.html.pt',
             permission='admin')
def test_view(request):
    debug = False
    f = Flash()
    f.critical('flashin test...')
    #~ relaties = DBSession.query(Relatie)
    relaties_dinsdag = request.mongo_db['relaties'].find({"Relatie.children.news.children.day.text": "dinsdag"})
    relaties_vrijdag = request.mongo_db['relaties'].find({"Relatie.children.news.children.day.text": "dinsdag"})
    records = dict()
    records['dinsdag'] = dict((record['_id'], type(record['_id'])) for record in relaties_dinsdag)
    records['vrijdag'] = dict((record['_id'], record) for record in relaties_vrijdag)
    l = type(records['dinsdag'].items())
    #~ g = TestView.get_grid(Relatie, relaties)
    debug = '\n'.join((str(type(records)), str(l)))
    userid = authenticated_userid(request)
    if userid is None:
        raise Forbidden()
    return {'relaties': records,
            'greeting': 'Hello, {n}!'.format(n=userid),
            'debug': debug,
            'flash': f.render(),
            }

@view_config(route_name='login', renderer='templates/login.html.pt')
@forbidden_view_config(renderer='templates/login.html.pt')
def login(request):
    message = ''
    login = ''
    password = ''
    # first: test db connection
    try:
        c = DBSession.connection()
        c.close()
        request.session.flash("PostgreSQL up and running")
    except Exception as e:
        response = e
        request.session.flash("PostgreSQL not running: {e}".format(e=e))
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    else:
        request.session.flash("Need to be logged in to view {u}".format(
                                                        u=referrer))
    came_from = request.params.get('came_from', referrer)
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            request.environ['REMOTE_USER'] = login
            headers = remember(request, login)
            request.session.flash(authenticated_userid(request))
            request.session.flash(effective_principals(request))
            return HTTPFound(location = came_from,
                             headers = headers)
        message = "Failed login: username/password combination didn't match."

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('home'),
                     headers = headers,)
