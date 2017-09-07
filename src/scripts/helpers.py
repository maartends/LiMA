#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       helpers.py
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

#~ from lxml import etree
from xml.etree import ElementTree
import datetime

#date & time
today = datetime.date.today().isoformat()

def l_parse_xml_file(xmlfile):
    """ lxml version
        read xml file and return etree """
    with open(xmlfile, 'r') as f:
        tree = etree.parse(f)
    return tree

def parse_xml_file(xmlfile):
    """ read xml file and return ElementTree root element """
    with open(xmlfile, 'r') as f:
        tree = ElementTree.parse(f)
    return tree.getroot()

def l_xml_child_to_dict(child, **kwargs):
    """ lxml version
        process xml child and return attr dict
        any given number of class attributes can be given as kwargs
        their value should then be the xpaht within the child
        TODO: ideally a class instance is given as reference """
    attr_dict = dict()
    for key in kwargs:
        if key == 'active':
            try:
                attr_dict[key] = translate_value(child.xpath(kwargs[key])[0], 'Boolean')
            except Exception, e:
                print(attr_dict)
        else:
            try:
                attr_dict[key] = unicode(child.xpath(kwargs[key])[0])
            except Exception, e:
                print(attr_dict)
    return attr_dict

def base_dict_for_el(el):
    d = dict()
    d[el.tag] = dict()
    d[el.tag]['text'] = str()
    d[el.tag]['attributes'] = dict()
    d[el.tag]['children'] = list()
    return d

def single_el_to_dict(el):
    d = base_dict_for_el(el)
    try:
        el.text.split()
        if el.text.split():
            d[el.tag]['text'] = el.text
    except:
        pass
    d[el.tag]['attributes'] = el.attrib
    return d

#~ def xml_child_to_dict(child):
    #~ """ process xml child and return attr dict
        #~ any given number of class attributes can be given as kwargs
        #~ their value should then be the xpath within the child
        #~ TODO: ideally a class instance is given as reference """
    #~ # element with children, all the same
    #~ if list(child) > 1:
        #~ d = single_el_to_dict(child)
        #~ d[child.tag]['children'] = [xml_child_to_dict(c) for c in child._children]
    #~ # element without children
    #~ else:
        #~ d = single_el_to_dict(child)
    #~ return d

def xml_child_to_dict(child, **kwargs):
    """ process xml element and return attr dict
        any given number of class attributes can be given as kwargs
        their value should then be the xpath within the child
        If no kwargs are given, translation of entire xml tree to dictionary
        is assumed.
        TODO: ideally a class instance is given as reference """
    if kwargs:
        d = dict()
        for key in kwargs:
            # if attribute: starts with '@'?
            if kwargs[key][0] == '@':
                # attribute 'active' return should be integer (Boolean)
                if key == 'active':
                    try:
                        d[key] = translate_value(child.attrib[kwargs[key][1:]], 'Boolean')
                    except Exception, e:
                        print(d)
                # other attributes
                else:
                    try:
                        d[key] = child.attrib[kwargs[key][1:]]
                    except Exception, e:
                        print(d)
            # else: tag
            else:
                try:
                    d[key] = child.find(kwargs[key]).text
                except Exception, e:
                    print(d)
    else:
        # element with children, all the same
        if list(child) > 1:
            d = single_el_to_dict(child)
            d[child.tag]['children'] = [xml_child_to_dict(c) for c in child._children]
        # element without children
        else:
            d = single_el_to_dict(child)
    return d

def generate_xml_attributes(senddate=today, number='x'):
    d = datetime.datetime.strptime(senddate, "%Y-%m-%d")
    iso = d.isocalendar()
    y = str(iso[0])
    w = ''.join(('0',str(iso[1])))[-2:] # to pad singledigit weeks with a zero
    if number == 'x':
        if d.isoweekday() == 2:
            number = 1
        elif d.isoweekday() == 5:
            number = 2
        elif d.isoweekday() == 7:
            number = 3
        else:
            pass
    attributes = dict()
    attributes = {
        "year": y,
        "week": w,
        "date": str(senddate),
        "filename":'e-zine_{yyyy}_w{WW}-{x}'.format(yyyy=y, WW=w, x=number)
        }
    return attributes

def translate_value(value, type):
    if type == 'Boolean':
        if value in ('true', 'True', 'TRUE', '1', 1):
            #~ print('value was true')
            return 1
        elif value in ('false', 'False', 'FALSE', '0', 0):
            return 0
    else:
        return value
