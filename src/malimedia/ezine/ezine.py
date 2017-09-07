#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ezine.py
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

def main():

    return 0

if __name__ == '__main__':
    main()

class Ezine:
    """
    class Ezine

    """

    def __init__(self, api_version):
        """init"""
        # logging
        logging.basicConfig(filename='ezine.log',
                    format='%(asctime)s : %(name)s : %(levelname)s : on lineno %(lineno)d : %(message)s',
                    filemode='w',
                    level=logging.DEBUG)
