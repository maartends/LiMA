#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       premailer.py
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
import httplib
import urllib
import json
import sys
import subprocess
import codecs

# get logger
log = logging.getLogger(__name__)

def main():

    return 0

if __name__ == '__main__':
    main()

class Premailer:
    """
    class Premailer
    BEWARE: this premailer doesn't support UTF-8!! Feed it ascii strings.
    """

    def __init__(self, local=False):
        """init"""
        self.local = local
        if not local:
            self.endpoint = 'http://premailer.dialect.ca/api/0.1/documents'
            self.c = httplib.HTTPConnection('premailer.dialect.ca')
            self.headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Accept": "text/plain"}
        else:
            pass

    def replace_html_entities(self, html):
        return html.replace('%5B%5B', '[[').replace('%5D%5D', ']]').\
                    replace('%7B%7B', '{{').replace('%7D%7D', '}}')

    def premail(self, data, to_file=False, link_query_string=None,
                remove_classes=True):
        """
        def premail(self, data, link_query_string=None, remove_classes=False)
            data: either url, html-string (or ezine object)
            to_file: boolean, if True saves to:
                /tmp/{ezine-id}.html
                /tmp/{ezine-id}.txt
            returns dict: d['documents']['html'] and d['documents']['txt']
        """
        params_dict = ({
            'link_query_string' : link_query_string,
            'remove_classes'    : remove_classes,
        })
        # data is url or html-string?
        if hasattr(data, 'subject'):
            log.info('Premailing ezine: {s}...'.format(s=data.cid))
            params_dict['html'] = data.html.encode('utf8')
        elif data[0:4] == 'http':
            log.info('Premailing url: {s}...'.format(s=data))
            params_dict['url'] = data
        else:       # assume html-string
            log.info('Premailing html-string: {s}...'.format(s=data[0:50].replace('\n', '').replace('\r', '')))
            params_dict['html'] = data.encode('utf8')
        d = dict()
        d['documents'] = dict()
        # Premail via API (http://premailer.dialect.ca)
        if not self.local:
            log.info('Premailing with public API...')
            try:
                params = urllib.urlencode(params_dict)
            except Exception as e:
                log.error(e)
                raise e
            else:
                log.info('Posting premail request to endpoint "{e}"...'.format(e=self.endpoint))
                try:
                    self.c.request("POST", "/api/0.1/documents", params, self.headers)
                except Exception as e:
                    log.exception('Posting premail request failed: {e}'.format(e=e.message))
                response = self.c.getresponse()

                if response.status == 201:
                    log.info('Premail request succes: status code = {s}'.format(s=response.status))
                    data = response.read()
                    d = json.loads(data)
                    log.info('Premail response documents: {s}'.format(s=d['documents']))
                else:
                    log.warning('Premail request failed: status code = {s}'.format(s=response.status))
        # Premail using local ruby gem
        else:
            log.info('Premailing with local gem...')
            # Premail html
            proc = subprocess.Popen(['premailer', '-m', 'html'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
            # TODO: this won't work if we feed it an URL
            try:
                res = proc.communicate(params_dict['html'])[0]
            except UnicodeEncodeError as e:
                log.error(e)
                raise e
            else:
                html = self.replace_html_entities(res)
                if to_file:
                    outfile = '/tmp/' + '.'.join((str(data.cid), 'html'))
                    log.info('Saving to {o}.'.format(o=outfile))
                    with codecs.open(outfile, 'w', encoding='utf-8') as f:
                        f.write(html.decode('utf8'))
            # HTML 2 txt via Premailer or Pandoc if fail
            """
            proc = subprocess.Popen(['pandoc', '--columns', '80',
                                     '-f', 'html',
                                     '-t', 'markdown'],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    )
            """
            proc = subprocess.Popen(['premailer', '-m', 'txt'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
            try:
                res = proc.communicate(params_dict['html'])[0]
            except UnicodeEncodeError as e:
                log.error(e)
                raise e
            else:
                txt = self.replace_html_entities(res)
                if to_file:
                    outfile = '/tmp/' + '.'.join((str(data.cid), 'txt'))
                    log.info('Saving to {o}.'.format(o=outfile))
                    with codecs.open(outfile, 'w', encoding='utf-8') as f:
                        f.write(txt.decode('utf8'))
        # Finally: check to return unicode
        d['documents']['html']  = html.decode('utf8')
        d['documents']['txt']   = txt.decode('utf8')
        return d
