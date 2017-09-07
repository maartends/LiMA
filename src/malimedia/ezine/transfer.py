#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       transfer.py
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
import sys
from ftplib import FTP
from urllib import urlopen
from urlparse import urlparse

log = logging.getLogger(__name__)

def main():

    return 0

if __name__ == '__main__':
    main()

class Ftp:
    """An FTP client class.

    To create a connection, call the class using these arguments:
            host, ftpuser, ftppasswd, remotedir
    """

    def __init__(self, host, ftpuser='Anonymous', ftppasswd='Anonymous', remotedir=None):
        """Initiates the FTP connection

        :param host:
        :param ftpuser:
        :param ftppasswd:
        :param remotedir:
        """
        self.host       = host
        self.ftpuser    = ftpuser
        self.ftppasswd  = ftppasswd
        self.remotedir  = remotedir
        try:
            self.ftp = FTP(self.host)
            self.ftp.login(self.ftpuser, self.ftppasswd)
            self.ftp.cwd(self.remotedir)
        except Exception as e:
            log.exception('Connection to {h} failed: {e}'.format(h=self.host, e=e))
            raise e

    def upload(self, resource, filename=None):
        """Uploads the resource (uri or local file) to ftp

        :param resource: The resource to upload.
        :type name: str
        :param filename: Filename to give to the uploaded resource (optional)
        :type state: str
        :returns:  str -- URI of the uploaded resource (on ftp server)
        """
        o = urlparse(resource)
        # if we didn't get a filename, we assume resource ending as filename
        if not filename:
            filename = o.path.split('/')[-1:][0]
        log.info(u'Uploading file {f} to {u}'.format(f=filename, u=self.host))
        STORcmd = ' '.join(['STOR', filename])
        # read file and upload to FTP
        #~ with open(resource, 'rb') as f:
        try:
            f = urlopen(resource)
            self.ftp.storbinary(STORcmd, f, callback=None)
        except Exception as e:
            log.warn('Uploading failed: {e}'.format(e=e))

        # close connection
        self.ftp.quit()
        s = 'http://{host}{remotedir}/{filename}'
        fileURL = s.format(filename=filename, remotedir=self.remotedir, host=self.host)
        log.debug(u'URL is {u}'.format(u=fileURL))
        return fileURL
