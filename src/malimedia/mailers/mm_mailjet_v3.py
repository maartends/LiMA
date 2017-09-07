#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mm_mailjet_v3.py
#
#  Copyright 2016 Mali Media Group
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

###############################################################################
#
#   mm_mailjet_v3.py
#
#   export MJ_APIKEY_PUBLIC='...'
#   export MJ_APIKEY_PRIVATE='...'
#
###############################################################################

# System imports
from __future__ import (
    absolute_import,
    unicode_literals
    )
import os
import logging
import codecs
from urllib2 import HTTPError
from exceptions import UnicodeEncodeError
from pyramid.renderers import render_to_response, render
# Third-party imports
import requests
from mailjet_rest import Client

from lima.malimedia.html.premailer import Premailer

# get logger
log = logging.getLogger(__name__)

# Get the Mailjet keys from environment, or, if not present, the configuration.
try:
    API_KEY = os.environ['MJ_APIKEY_PUBLIC']
except KeyError as e:
    log.error('API_KEY not present in environment.')
    exit(1)

try:
    API_SECRET = os.environ['MJ_APIKEY_PRIVATE']
except KeyError as e:
    log.error('API_SECRET not present in environment.')
    exit(1)


class Mailjet:
    """
    class Mailjet

    """

    def __init__(self, request=None):
        """init"""
        self.request    = request
        self.LIST_ID    = self.request.registry.settings['list_id']
        # Open client
        log.debug('Init Mailjet API...')
        try:
            self.mapi = Client(auth=(API_KEY, API_SECRET))
        except Exception as e:
            log.error('Init Mailjet API failed: {e}'.format(e=e.message))
            raise e
        else:
            log.debug('Mailjet API init OK')

    def _check_existing_newsletters(self, ezine):
        # check if a newsletter exists in "draft"
        # TODO: should also check for "programmed" or "sent" and prompt user
        # Statusses:
        #   AXCanceled (-3)
        #   Deleted (-2)
        #   Archived (-1)
        #   Draft (0)
        #   Programmed (1)
        #   Sent (2)
        #   AXTested (3)
        #   AXSelected (4)
        #
        return False
        filters = {
          'Status': 3,
          'Limit': 1
        }
        filters = {
          'Limit': 10,
          'Drafts': True,
        }
        filters = {
          'Limit': 10,
          'Title': 'Biedmee_2016_w23-1',
        }
        result = self.mapi.newsletter.get(filters=filters)
        # check campaign titles
        match_list = [l for l in c['result'] if l['title'] == ezine.name and l['status'] == 'draft']
        return match_list

    def upload(self, ezine):
        """"""
        # create campaign
        log.debug('Ezine params: subject = {s} - name = {n}'.format(s=ezine.subject, n=ezine.name))
        log.debug(ezine.subject)
        log.debug('subject type: {t}'.format(t=type(ezine.subject)))
        data = {
          'Locale': 'nl_NL',
          'Sender': 'Biedmee.be | Veilingen',
          'SenderName': 'Biedmee.be | Veilingen',
          'SenderEmail': 'veilingen@biedmee.be',
          'ReplyEmail': 'veilingen@biedmee.be',
          'Subject': ezine.subject,
          'ContactsListID': self.LIST_ID,
          'Title': ezine.name,
          'EditMode': 'html',
          'EditType': 'full',
        }
        log.debug(data)
        match_list = self._check_existing_newsletters(ezine)
        if not match_list:
            log.info(u'No matching campaign found in "drafts": creating new '
                      'campaign')
            resp = self.mapi.newsletter.create(data=data)
            if resp.status_code != 201:
                log.error(u'CreateCampaign failed with code %s: "%s".',
                          str(resp.status_code), resp.json()['ErrorInfo'] or resp.json()['ErrorMessage'])
                raise e
            else:
                campaign_id = resp.json()['Data'][0]['ID']
                log.info(u'Mailjet campaign created. '
                          'Id = {i}'.format(i=campaign_id))
        else:
            # TODO: ...
            campaign_id = match_list['...something...']
            log.info(u'Matching campaign found in "drafts": reusing existing '
                      'campaign. Id = {i}'.format(i=campaign_id))
            try:
                resp = self.mapi.newsletter.update(id=campaign_id, data=data)
            except HTTPError as e:
                log.error(u'UpdateCampaign failed with code {c}: '
                           '{m}.'.format(c=e.code, m=e.reason))
                raise e
            else:
                log.info(u'Mailjet campaign updated. '
                          'Id = {i}'.format(i=campaign_id))
        data = {
          'Html-part': ezine.html_pre.encode('utf8'),
          'Text-part': ezine.txt.encode('utf8'),
        }
        log.debug('sethtmlcampaign for campaign_id: {i}'.format(i=campaign_id))
        try:
            result = self.mapi.newsletter_detailcontent.update(id=campaign_id, data=data)
        except UnicodeEncodeError as e:
            log.debug(e)
            data = {
              'Html-part': ezine.html_pre.encode('utf8'),
              'Text-part': ezine.txt.encode('utf8'),
            }
            try:
                result = self.mapi.newsletter_detailcontent.create(id=campaign_id, data=data)
            except UnicodeEncodeError as e:
                log.error(e)
                raise e
        except HTTPError as e:
            log.error(u'sethtmlcampaign failed with code {c}: '
                       '{m}.'.format(c=e.code, m=e.reason))
            raise e
        else:
            log.debug(result.json())
        return campaign_id

    def send_test(self, campaign_id, email):
        """"""
        data = {
            'Email' : email,
            'Name' : 'Jan Met De Pet',
        }
        try:
            resp = self.mapi.newsletter_test(id=campaign_id, data=data)
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
