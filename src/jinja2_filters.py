#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib import quote_plus, urlencode
from urlparse import urlparse, parse_qs, parse_qsl, urlunparse

# default utm codes
DEF_UTM_DICT = {
    'utm_medium'    : 'email',
    'utm_source'    : 'e-zine',
    #~ 'utm_campaign'  : '',
    #~ 'utm_channel'   : '',
}

# domains utm code
UTM_NETLOCS = (
    'www.vakantie.be',
    'veilingen.vakantie.be',
    'www.biedmee.be',
)

# vakantie.be forward uri
FORWARD_URI = 'http://www.vakantie.be/pages/forward.aspx?RedirectPage='

def url_prepare(uri, ezine_name=None):
    parse_result = urlparse(uri)
    if parse_result.netloc not in UTM_NETLOCS:
        return ''.join(( FORWARD_URI, quote_plus(uri) ))
    else:
        return append_utmcodes(uri, ezine_name)

def url_encode(uri, ezine_name=None):
    parse_result = urlparse(uri)
    if parse_result.netloc in UTM_NETLOCS:
        return quote_plus(append_utmcodes(uri, ezine_name))
    else:
        return quote_plus(uri)

def append_utmcodes(uri, ezine_name=None):
    parse_result = urlparse(uri)
    if parse_result.netloc in UTM_NETLOCS:
        query_list   = parse_qsl(parse_result.query)
        query_dict   = parse_qs(parse_result.query)
        DEF_UTM_DICT['utm_campaign'] = ezine_name
        for k, v in DEF_UTM_DICT.iteritems():
            if not k in query_dict.keys():
                query_list.append((k, v))
        query_string = urlencode(query_list)
        parse_result_tuple = (
            parse_result.scheme,
            parse_result.netloc,
            parse_result.path,
            parse_result.params,
            query_string,
            parse_result.fragment
        )
        uri = urlunparse(parse_result_tuple)
        return uri

def parse_result_astuple(parse_result):
    t = (
        parse_result.scheme,
        parse_result.netloc,
        parse_result.path,
        parse_result.params,
        parse_result.query,
        parse_result.fragment
    )
    return t

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)
