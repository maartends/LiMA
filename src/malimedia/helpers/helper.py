#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       helper.py
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

import sys
import logging
import urllib
import string
import hashlib
import codecs
from urlparse import urlparse
from random import choice
from datetime import datetime

log = logging.getLogger(__name__)

def main():

    return 0

if __name__ == '__main__':
    main()

class Helper:
    """
    class Helper

    """

    def __init__(self):
        """init"""
        pass

    def read_url(self, url):
        """
        def read_url(self, url)

        """
        o = urlparse(url)
        try:
            c = urllib.urlopen(url)
            log.info(u'Read_url request posted to: {o}'.format(o=url))
        except Exception as e:
            log.error(u'Posting read_url request failed: {e}'.format(e=e))
        response = c.getcode()
        if response == 200:
            log.info(u'Read_url request succes: status code = {s}'.format(s=response))
            data = c.read()
        else:
            log.info(u'Read_url request failed: status code = {s}'.format(s=response))
        c.close()
        return data

    def make_filename(self, name, ext):
        """
        def make_filename(self, name, ext)
            generate filename with given extension ext from name
            if name has extension: replace
            if not: append
        """
        if '.' in name:
            return '.'.join((name.split('.')[0], ext))
        else:
            return '.'.join((name, ext))

        """
        def vakbe_hash(self, password, salt)
            generate password hash
        """
        val = salt + '_' + password
        hash = hashlib.sha1(val).hexdigest()
        return hash

    def generate_simple_password(self, size=8):
        """
        generate_simple_password(self, size=8):
            generate password
        """
        password = ''.join([choice(string.ascii_uppercase + string.digits) for i in range(size)])
        return password

    def update_veilingen_db(self, url):
        """
        update_veilingen_db(url):
        """
        try:
            data = urllib.urlretrieve(url, '/tmp/sheet.csv')
        except Exception as e:
            data = e
        else:
            log.info(u'Read_url request posted to: {o}'.format(o=url))
            """
            f = open(data[0], 'rb')
            n = codecs.open('/tmp/sheet2copy.csv', encoding='utf-8', mode='w')
            n.write(f.readline().replace(' ', '_').lower().decode('iso-8859-1'))
            n.write(f.read().decode('iso-8859-1'))
            """
            d = open(data[0], 'r')
            f = d.readline().replace(' ', '_').lower()
            with open('/tmp/sheet2copy.csv', 'w') as n:
                n.write(f)
                n.write(d.read())
            log.info(u'New file written to: {o}'.format(o='/tmp/sheet2copy.csv'))
            data = data[0]
        return data

    def jsonify(self, query):

        return query
