#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       api.py
#
#       Copyright 2011 Mali Media Group
#       <admin@malimedia.be>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program. If not, see <http://www.gnu.org/licenses/>.

from suds.client import Client
import logging
import sys

log = logging.getLogger(__name__)

def main():
    print('Sorry, not yet to be invoked from command line... :-)')
    return 0

if __name__ == '__main__':
    main()

class Api:
    """
    class Api

    This class provides convenient acces to the most used API calls in Clang.
    Furthermore, acces to all methods is available via the client attribute.
    """

    def __init__(self, wsdl, _token):
        """init"""

        self.wsdl = wsdl
        self._token = _token
        self.exitmsg = ('Press Enter to exit...')
        # open client
        log.info(u'Creating client on {w} ...'.format(w=self.wsdl))
        try:
            self.client = Client(self.wsdl)
            log.info('Client created on "{w}"'.format(w=self.wsdl))
        except Exception as e:
            log.error('Client creation to "{w}" failed: {e}'.format(e=e, w=self.wsdl))

    def create_object_from_wsdl(self, classname):
        """
        def create_object_from_wsdl(classname)

        Takes one argument: classname to instantiate as string.
        For a list of possible classes: see the Clang Api documentation on
        the Clang website.
        """
        log.debug(u'Instantiating {name} object...'.format(name=classname))
        try:
            obj = self.client.factory.create(classname)
            log.info('{name} object instantiated.'.format(name=classname))
        except Exception as e:
            log.error(u'{name} object instantiation failed: {e}'.format(name=classname, e=e))
        return obj

    def create_Emailobject_from_wsdl(self, properties):
        """
        def create_Emailobject_from_wsdl(properties)

        Takes one argument: properties
        properties is a dictionary of name-value pairs
        e.g.: dict({'name': 'E-zine_2012_w12-2'})
        """
        log.debug(u'Creating Email object...')
        email = self.create_object_from_wsdl('Email')
        email = self.object_populate(email, properties)
        return email

    def create_Optionobject_from_wsdl(self, properties):
        """
        def create_Optionobject_from_wsdl(properties)

        Takes one argument: properties
        properties is a dictionary of name-value pairs
        e.g.: dict({'name': 'E-zine_2012_w12-2'})
        """
        log.debug(u'Creating Option object...')
        Option = self.create_object_from_wsdl('Option')
        Option = self.object_populate(Option, properties)
        return Option

    def object_populate(self, object, properties):
        """
        def object_populate(self, object, properties)
        """
        mi1 = 'Populating object property: "{n}" with "{m}"'
        for key, value in properties.items():
            # would normally be: 'm=value[:64].replace("\n","")'
            log.info(mi1.format(n=key, m='some content (needs changing, see api.py, line 96)'))
            object.__dict__[key] = value
        return object

    def email_find(self, email):
        """
        def email_find(self, email)
        returns
        """
        mf1 = ('Email deletion failed: {e}')
        mf2 = ('Email deletion failed! Response code was "{code}". Msg was "{msg}".')
        ms1 = ('Email deleted. Response code was "{code}". Msg was "{msg}".')

        log.debug(u'Searching Email object in Clang.')
        try:
            response = self.client.service.email_getByObject(self._token, email)
        except Exception as e:
            log.error(u'Email searching failed: {e}'.format(e=e))
        return response

    def email_upsert(self, email, **kwargs):
        """
        def email_upsert(self, email)
        """
        # search for email object by **kwargs
        #~ needle = self.create_Emailobject_from_wsdl(dict({'name': email.name}))
        needle = self.create_Emailobject_from_wsdl(kwargs)
        response = self.email_find(needle)
        #~ log.debug('response was {r}'.format(r=response))
        if response.msg == "":
            pass
        elif len(response.msg[0]) == 1:
            email.id = response.msg[0][0].id
            log.info('Email object found in Clang: \033[00;31mwill overwrite!\033[00;00m')
        else:
            log.warning('More than one email with provided proporties found in Clang!')

        log.info(u'Upserting Email object in Clang. Folder={f}'.format(f=email.folder))
        try:
            email = self.client.service.email_upsert(self._token, email)
            log.info(u'Email object upserted in Clang. Email id={id}'.format(id=email.msg.id))
        except Exception as e:
            log.error(u'Email upserting failed: {e}'.format(e=e))
            raise e
        return email

    def make_multipartemail_from_urls(self, urlsdict):
        """
        def make_multipartemail_from_urls(self, urlsdict)
        """
        pass

    def email_sendToGroup(self, emailId, groupId, manualOptions=None, Options=None):
        """
        def email_sendToGroup(self, emailId, groupId, manualOptions=None, Options=None)

        Sends the provided Email to a specific Group (including subgroups)
        """
        try:
            response = self.client.service.email_sendToGroup(self._token, emailId, groupId, manualOptions, Options)
        except Exception as e:
            log.error(u'Email sending failed: {e}'.format(e=e))
        if response.code == 0:
            log.info(u'Email sent. Response code was "{code}". Msg was "{msg}".'.format(code=response.code, msg=response.msg))
        else:
            log.info(u'Email sending failed! Response code was "{code}". Msg was "{msg}".'.format(code=response.code, msg=response.msg))
        return response

    def email_sendToCustomer(self, emailId, groupId, manualOptions=None, Options=None):
        """
        def email_sendToCustomer(string uuid, int emailId, int customerId, Option[ ] manualOptions, Option[ ] options)

        Sends the provided Email to a specific Customer
        """
        try:
            response = self.client.service.email_sendToCustomer(self._token, emailId, customerId, manualOptions, Options)
        except Exception as e:
            log.error(u'Email sending failed: {e}'.format(e=e))
        if response.code == 0:
            log.info(u'Email sent. Response code was "{code}". Msg was "{msg}".'.format(code=response.code, msg=response.msg))
        else:
            log.info(u'Email sending failed! Response code was "{code}". Msg was "{msg}".'.format(code=response.code, msg=response.msg))
        return response

    def email_delete(self, emailId):
        """
        def email_delete(self, emailId)

        Deletes the provided Email
        """
        mf1 = (u'Email deletion failed: {e}')
        mf2 = (u'Email deletion failed! Response code was "{code}". Msg was "{msg}".')
        ms1 = (u'Email deleted. Response code was "{code}". Msg was "{msg}".')
        try:
            response = self.client.service.email_delete(self._token, emailId)
        except Exception as e:
            log.error(mf1.format(e=e))
        if response.code == 0:
            log.info(ms1.format(code=response.code, msg=response.msg))
        else:
            log.warning(mf2.format(code=response.code, msg=response.msg))
        return response

    def email_getAll(self):
        """
        def email_getAll(self)


        """
        log.info('Retreiving all emails in brand...')
        try:
            obj = client.service.email_getAll(_token)
            log.info('Emails retreived.')
        except Exception as e:
            log.error('Email retreival failed: {e}'.format(e=e))
        return obj
