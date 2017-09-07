#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       settings.py
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

import logging
import os

log = logging.getLogger(__name__)

def main():
    print('Settings file. Not script.')

if __name__ == '__main__':
    print('Settings file. Doesn\'t do anything in itself.')

class Settings():
    """
    class Settings
    # TODO: reserve the settings file for imutable settings (?), make new file for mutable settings
    """

    def __init__(self, brand):
        """init"""
        # [BRAND]
        # possible values: vakbe, vaknl, aosta, veiling, touche, biedmee
        self.brand = brand
        # [TODO]
        self.todo = dict({
            'make': False,
            'upload': False,
            'premail': False,
            'save_premail_html': False,
            'save_premail_txt': False,
            'save_pdf': False,
            'upsert': True,
            'send_test': True,
        })
        # [PATHS]
        self.yamlfile = False
        # TODO: fix this to put pdf's and alike in the static server
        self.mainpath = '/tmp'

        self.xml_src_path =     os.path.join(self.mainpath, 'src/xml/xml')
        self.pre_html_path =    os.path.join(self.mainpath, 'pre/html')
        self.pre_txt_path =     os.path.join(self.mainpath, 'pre/txt')
        self.pdf_path =         os.path.join(self.mainpath, 'pdf')

        # [FTP]
        self.host = ''
        self.ftpuser = ''
        self.ftppasswd = ''
        if self.brand == 'vakbe':
            self.remotedir = '/ezine'
        elif self.brand == 'aosta':
            self.remotedir = '/valledaosta'
        elif self.brand == 'veiling':
            self.remotedir = '/veilingen/Marketing'
        elif self.brand == 'biedmee':
            self.remotedir = '/ent/ezine/type/biedmee/ezine'
        else:
            log.warn('\033[34;47mOops: {e} is not a valid brand. Exiting...\033[00;00m'.format(e=self.brand))

        # [API]
        self.api_version = '1.10'
        wsdl_url = 'https://secure.myclang.com/app/api/soap/public/index.php?wsdl&version={v}'
        self.wsdl = wsdl_url.format(v=self.api_version)
        if self.brand == 'vakbe':
            self._token = 'a809b83d-4ec3-4b10-b4f0-b6b71748a4f2' #vak.be & veilingen
        elif self.brand == 'aosta':
            self._token = '2f8190d1-60dc-4c2a-a7c4-0badaf397740' #aosta
        elif self.brand == 'veiling':
            self._token = 'a809b83d-4ec3-4b10-b4f0-b6b71748a4f2' #vak.be & veilingen
        elif self.brand == 'touche':
            self._token = '313436b8-f147-4dd6-bdc5-7263c1f9830e' #touché
        elif self.brand == 'biedmee':
            self._token = '1-ce901606-2b4c-11e3-ac90-3bf3240fdb67' #biedmee
        else:
            log.warn('\033[34;47mOops: {e} is not a valid brand. Exiting...\033[00;00m'.format(e=self.brand))
        # [EZINE]
        # folders: /tmp, /Ezines/yyyy
        self.email_properties = dict({
            'class': 'EMAIL',
            'type': 'MULTIPART',
            'name': 'email_name',
            # TODO: read from xml!
            'subject': u'Vakantie.be toppers',
            'htmlContent': 'htmlContent',
            'textContent': 'Indien u ons e-magazine niet goed kan lezen, ga dan naar "{{viewurl}}"',
            'createdBy': 'Suds SOAP client (Mali Media Group)',
        })
        # TODO: year should be dynamic: `ezine.send_date.year`
        if self.brand == 'vakbe':
            self.email_properties['folder'] = '/Ezines/2015'
            self.email_properties['fromName'] = 'Vakantie.be | Sanne'
            self.email_properties['fromAddress'] = 'sanne@vakantie.be'
            self.test_group_id = 79
        elif self.brand == 'aosta':
            self.email_properties['folder'] = '/Newsletters/2015'
            self.email_properties['fromName'] = 'Visit Aosta'
            self.email_properties['fromAddress'] = 'newsletter@visitaosta.nl'
            self.test_group_id = 7
        elif self.brand == 'veiling':
            self.email_properties['folder'] = '/Veilingen.vakantie.be/Marketing/News'
            self.email_properties['fromName'] = 'Vakantieveilingen | Sanne'
            self.email_properties['fromAddress'] = 'veilingen@vakantie.be'
            self.test_group_id = 79
        elif self.brand == 'touche':
            self.email_properties['folder'] = '/Newsletters'
            self.email_properties['fromName'] = 'Touché Gent'
            self.email_properties['fromAddress'] = 'info@touche-gent.be'
            self.test_group_id = 1
        elif self.brand == 'biedmee':
            self.email_properties['folder'] = '/Marketing/Ezines/2015'
            self.email_properties['fromName'] = 'Biedmee.be'
            self.email_properties['fromAddress'] = 'veilingen@biedmee.be'
            self.test_group_id = 4
        else:
            log.warn('\033[34;47mOops: {e} is not a valid brand. Exiting...\033[00;00m'.format(e=self.brand))
        # test groepen vak.be: test mali = 79, test_maarten = 77
        # test groepen aosta: testing Glenaki = 6, test_mali = 7
        # test groep touché: Testing = 1
        # profielen: Basis = 1

        # TODO: onderstaande socials inwerken
        # [SOCIAL MEDIA]
        # [FACEBOOK]
        # [TWITTER]
        log.info('Settings read from settings.py')
