#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       run.py
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

from __future__ import (
    absolute_import,
    unicode_literals
    )

import logging
import os
try:
    import pynotify
    import yaml
except:
    pass

from .settings import Settings
from .malimedia.clang.api import Api
from .malimedia.ezine.transfer import Ftp
from .malimedia.helpers.helper import Helper
from .malimedia.html.premailer import Premailer
from .malimedia.html.converters import Html2pdf
from fa.jquery.utils import Flash
from pyramid.settings import asbool

log = logging.getLogger(__name__)

class Runner:
    """
    """
    def __init__(self, request=None):
        self.request    = request

    def main(self, ezine):
        """
        main(ezine)

        """
        # initialize variables
        newsletter =    '.'.join((ezine.name, 'html'))
        subject =       ezine.subject
        brand =         ezine.type

        log.info('{n} started'.format(n='run.py'))
        try:
            n = pynotify.Notification ('{n} started'.format(n='run.py'), '')
            n.show()
        except:
            f = Flash()
            f.critical('{n} started'.format(n='run.py'))

        # READ SETTINGS
        s = Settings(brand)
        log.debug('Settings read are: {s}'.format(s=s))
        # Did we get a filename?
        if newsletter or subject:
            if newsletter:
                s.filenames = (newsletter, )
            if subject:
                s.email_properties['subject'] = subject

        # START RUN FOR...
        if s.yamlfile:
            log.info('Reading yaml file')
            with open(s.yamlfile, 'r') as f:
                data = yaml.load(f)
        else:
            pass

        # TODO: check if list or str, and if dir: dan alle files

        for file in s.filenames:
            if not newsletter:
                s.filepath = os.path.join(s.mainpath, file)
            s.email_name =  file.split('.')[0].capitalize()
            s.email_properties['name'] = s.email_name
            log.info('Handling file: {n}.'.format(n=s.email_name))
            if s.yamlfile:
                with open(s.yamlfile, 'r') as f:
                    data = yaml.load(f)
                for d in data['mails']:
                    if d == s.email_name:
                        s.email_properties['subject'] = data['mails'][d]['Subject']

            # MAKE EZINE
            if s.todo['make']:
                ezine = s.ezine

            # UPLOAD EZINE TO FTP
            if s.todo['upload']:
                log.debug('Brand is "{b}".'.format(b=brand))
                log.debug('File is "{f}".'.format(f=file))
                try:
                    f = Ftp(s.host, s.ftpuser, s.ftppasswd, s.remotedir)
                except Exception as e:
                    raise e
                else:
                    if asbool(self.request.registry.settings['local_devel']):
                        if newsletter:
                            resource = '/'.join(('http://lima.malimedia.be.devel', 'ezine', brand, file))
                        else:
                            resource = os.path.join(s.mainpath, s.filename)
                    else:
                        resource = '/'.join(('http://lima.malimedia.be', 'ezine', brand, file))
                    log.debug('Resource is "{r}".'.format(r=resource))
                    ezine_url = f.upload(resource)

            # PREMAIL EZINE
            if s.todo['premail']:
                p = Premailer()
                #~ link_query_string = 'utm_source={s}&utm_medium=email'.format(s=s.email_name)
                data = p.premail(ezine_url)
                urlsdict = dict({
                    'htmlContent': data['documents']['html'],
                    'textContent': data['documents']['txt'],
                })
                t = Helper().read_url(urlsdict['htmlContent'])
                urlsdict['htmlContent'] = t.decode('utf-8').replace('%7B%7B', '{{').replace('%7D%7D', '}}')
                t = Helper().read_url(urlsdict['textContent'])
                urlsdict['textContent'] = t.decode('utf-8').replace('%7B%7B', '{{').replace('%7D%7D', '}}')
                # put in email_properties dict
                s.email_properties.update(urlsdict)

            # SAVE PREMAILED HTML
            if s.todo['save_premail_html']:
                ext = 'html'
                t = Helper().make_filename(file, ext)
                filepath = '/'.join((s.pre_html_path, t))
                with open(filepath, 'w') as f:
                    f.write(s.email_properties['htmlContent'])
                log.info('Premailed {t} saved in {p}'.format(t=ext, p=filepath))

            # SAVE PREMAILED TXT
            if s.todo['save_premail_txt']:
                ext = 'txt'
                t = Helper().make_filename(file, 'txt')
                filepath = '/'.join((s.pre_txt_path, t))
                with open(filepath, 'w') as f:
                    f.write(s.email_properties['textContent'])
                log.info('Premailed {t} saved in {p}'.format(t=ext, p=filepath))

            # SAVE PDF VERSION
            if s.todo['save_pdf']:
                c = Html2pdf()
                c.to_pdf(s.filepath, s.pdf_path)

            # CONNECT TO CLANG
            if s.todo['upsert'] or s.todo['send_test']:
                a = Api(s.wsdl, s._token)

            # UPSERT
            if s.todo['upsert']:
                # did we premail first or not (and in the latter case: we should have ezine.html_pre)
                if not s.todo['premail']:
                    s.email_properties['htmlContent'] = ezine.html_pre
                # make ezine object from htmlurl and texturl
                ezine = a.create_Emailobject_from_wsdl(s.email_properties)
                # put ezine in Clang
                # using "upsert" so we also need something to distinguish this object
                # ie., name & folder, id, ...
                response = a.email_upsert(ezine, name=s.email_properties['name'],
                                                 folder=s.email_properties['folder'])

            # SEND TEST
            # TODO: alleen send test werkt niet (response?)
            if s.todo['send_test']:
                response = a.email_sendToGroup(response.msg.id, s.test_group_id)

        log.info('{n} terminated'.format(n='run.py'))

        try:
            n = pynotify.Notification ('{n} terminated'.format(n='run.py'),
                                       '')
            n.show()
        except:
            pass

#~ if __name__ == '__main__':
    #~ main(ezine)
