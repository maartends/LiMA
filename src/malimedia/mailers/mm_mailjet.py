#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mailjet.py
#
#  Copyright 2014 Mali Media Group
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
import mailjet
import logging
import codecs
from urllib2 import HTTPError
from exceptions import UnicodeEncodeError
from pyramid.renderers import render_to_response, render
from lima.template_filters.chameleon.filters import templateFilters
from lima.malimedia.helpers.helper import Helper
from lima.malimedia.html.premailer import Premailer

# get logger
log = logging.getLogger(__name__)


class Mailjet:
    """
    class Mailjet

    """

    def __init__(self, request=None):
        """init"""
        self.request = request
        # open client
        log.debug('Init Mailjet API...')
        try:
            self.mapi = mailjet.Api(api_key=os.environ['MJ_APIKEY_PUBLIC'],
                                secret_key=os.environ['MJ_APIKEY_PRIVATE'])
        except Exception as e:
            logging.exception('Init Mailjet API failed: {e}'.format(e=e.message))
            raise e
        else:
            log.debug('Mailjet API init OK')

    def _check_existing_campaigns(self, ezine):
        # check if campaign exists in "draft"
        # TODO: status param doesn't seem to work in API
        # TODO: should also check for "programmed" or "sent" and prompt user
        c = self.mapi.message.campaigns()
        # check campaign titles
        match_list = [l for l in c['result'] if l['title'] == ezine.name and l['status'] == 'draft']
        return match_list

    def upload(self, ezine):
        """"""
        # create campaign
        log.debug('Ezine params: subject = {s} - name = {n}'.format(s=ezine.subject, n=ezine.name))
        log.debug(ezine.subject)
        log.debug('subject type: {t}'.format(t=type(ezine.subject)))
        params = {
            'method': 'POST',
            'subject': ezine.subject.encode('utf8'),
            'list_id': 610716,
            'lang': 'nl',
            'from': 'veilingen@biedmee.be',
            'from_name': 'Biedmee.be | Veilingen',
            'reply_to': 'veilingen@biedmee.be',
            'footer': 'default',
            'edition_mode': 'html',
            'edition_type': 'full',
            #~ 'callback': 'http://www.malimedia.be/',
            #~ 'token': ezine.name,  /* TODO: Hoe werkt dit? */
            'title': ezine.name
        }
        match_list = self._check_existing_campaigns(ezine)
        if not match_list:
            log.info(u'No matching campaign found in "drafts": creating new '
                      'campaign')
            try:
                resp = self.mapi.message.createcampaign(**params)
            except HTTPError as e:
                log.error(u'CreateCampaign failed with code {c}: '
                           '{m}.'.format(c=e.code, m=e.reason))
                raise e
            else:
                campaign_id = int(resp['campaign']['id'])
                log.info(u'Mailjet campaign created. '
                          'Id = {i}'.format(i=campaign_id))
        else:
            campaign_id = int(match_list[0]['id'])
            params['id'] = campaign_id
            log.info(u'Matching campaign found in "drafts": reusing existing '
                      'campaign. Id = {i}'.format(i=campaign_id))
            try:
                resp = self.mapi.message.updatecampaign(**params)
            except HTTPError as e:
                log.error(u'UpdateCampaign failed with code {c}: '
                           '{m}.'.format(c=e.code, m=e.reason))
                raise e
            else:
                log.info(u'Mailjet campaign updated. '
                          'Id = {i}'.format(i=campaign_id))
        """
        # add html to campaign
        t = templateFilters()
        renderer = 'lima:' + '/'.join(('templates', 'ezines', 'biedmee', 'ezine.html.pt'))
        try:
            html = render(renderer,
                                  {'Ezine': ezine,
                                   'mailer': 'mailjet',
                                   'templateFilters': t,
                                   'debug': False,},
                                   request=self.request)
        except Exception as e:
            log.error(e.message)
            raise e
        else:
            # premail HTML
            log.info('Premailing ezine...')
            p = Premailer(local=True)
            data = p.premail(html)
            urlsdict = dict({
                'htmlContent': data['documents']['html'],
                'textContent': data['documents']['txt'],
            })
            t = Helper().read_url(urlsdict['htmlContent'])
            log.debug('htmlContent type before: {t}'.format(t=type(t)))
            urlsdict['htmlContent'] = t.decode('utf-8').replace('%5B%5B', '[[').replace('%5D%5D', ']]')
            log.debug('htmlContent type after: {t}'.format(t=type(urlsdict['htmlContent'])))
            t = Helper().read_url(urlsdict['textContent'])
            urlsdict['textContent'] = t.decode('utf-8').replace('%5B%5B', '[[').replace('%5D%5D', ']]')
            params_html = {
                'method': 'POST',
                'id'    : campaign_id,
                'html'  : urlsdict['htmlContent'].encode('utf8'),
                'text'  : urlsdict['textContent'].encode('utf8'),
            }
        """

        params_html = {
            'method': 'POST',
            'id'    : campaign_id,
            'html'  : ezine.html_pre.encode('utf8'),
            'text'  : ezine.txt.encode('utf8'),
        }
        log.debug('sethtmlcampaign for campaign_id: {i}'.format(i=campaign_id))
        try:
            resp_html = self.mapi.message.sethtmlcampaign(**params_html)
        except UnicodeEncodeError as e:
            log.debug(e)
            params_html['html'] = ezine.html_pre
            params_html['text'] = ezine.txt
            try:
                resp_html = self.mapi.message.sethtmlcampaign(**params_html)
            except UnicodeEncodeError as e:
                log.error(e)
                raise e
        except HTTPError as e:
            log.error(u'sethtmlcampaign failed with code {c}: '
                       '{m}.'.format(c=e.code, m=e.reason))
            raise e
        else:
            log.debug(resp_html)

        return campaign_id

    def send_test(self, campaign_id, email):
        """"""
        params = {
            'method': 'POST',
            'id'    : campaign_id,
            'email' : email,
        }
        try:
            resp_test = self.mapi.message.testcampaign(**params)
        except Exception as e:
            log.error(e)
            raise e
        else:
            log.info('Test sent to "{e}" for campaign "{i}".'.format(e=email, i=campaign_id))
        return True

    def unsub_contact(self, email, list_id='3jNz'):
        """"""
        params = {
            'method'    : 'POST',
            'contact'   : email,
            'id'        : list_id,
        }
        try:
            resp = self.mapi.lists.unsubcontact(**params)
        except Exception as e:
            log.error(e)
            raise e
        else:
            log.info('Unsub customer with email "{e}" from '
                     'list "{i}".'.format(e=email, i=list_id))
        return True
