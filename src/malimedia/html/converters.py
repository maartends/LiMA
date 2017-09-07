#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       converters.py
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
import subprocess
import os


def main():

    return 0

if __name__ == '__main__':
    main()

class Html2pdf:
    """
    class Html2pdf

    """

    def __init__(self):
        """init"""
        pass

    def to_pdf(self, inputfile, outputdir):
        """
        def to_pdf(self, inputfile)
        """
        iname = os.path.split(inputfile)[1].split('.')[0]
        cmd = 'wkhtmltopdf {i} {o}/{iname}.pdf'.format(i=inputfile, o=outputdir, iname=iname)

        message_job = 'Converting {i} {o}/{iname}.pdf'
        message_succes = 'Converting {i} {o}/{iname}.pdf succeeded!'
        message_failure = 'Converting {i} {o}/{iname}.pdf failed! Error: {e}'
        print(message_job.format(i=inputfile, o=outputdir, iname=iname))
        try:
            subprocess.call(cmd, shell=True)
            logging.info(message_job.format(i=inputfile, o=outputdir, iname=iname))
        except Exception as e:
            logging.exception(message_failure.format(inputfilename=inputfilename, e=e))
            print(message_failure.format(i=inputfile, o=outputdir, iname=iname, e=e))
            x = raw_input('Press Enter to exit...')
            sys.exit(1)
