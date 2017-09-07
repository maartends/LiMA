#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       forms.py
#
#       Copyright 2012 Mali Media Group <admin@malimedia.be>
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
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

# see https://github.com/FormAlchemy/pyramid_formalchemy/issues/22
from formalchemy import FieldSet, Grid

from fa.jquery import renderers as jquery
FieldSet.default_renderers.update(jquery.default_renderers)
Grid.default_renderers.update(jquery.default_renderers)