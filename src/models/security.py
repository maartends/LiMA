#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  security.py
#
#  Copyleft 2012 Mali Media Group <admin@malimedia.be>
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
#  You can find the GNU General Public License on:
#  http://www.gnu.org/copyleft/gpl.html
#
#

from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    ALL_PERMISSIONS,
    )

class RootFactory(object):
    """

    """
    __acl__ = [ (Allow, 'g:administrators', ALL_PERMISSIONS),
                (Allow, 'g:viewers',        'view'),
                (Allow, Everyone,           'view'),
                ]

    def __init__(self, request):
        pass

