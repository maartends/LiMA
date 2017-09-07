# -*- coding: utf-8 -*-

from urllib import quote_plus, urlencode
from urlparse import urlparse, parse_qs, parse_qsl, urlunparse

class templateFilters:
    """
    """
    # default utm codes
    DEF_UTM_DICT = {
        'utm_medium'    : 'email',
        'utm_source'    : 'e-zine',
        #~ 'utm_campaign'  : '',
        #~ 'utm_channel'   : '',
    }

    # domains utm code
    UTM_NETLOCS = (
        'vakantie.be',
        'www.vakantie.be',
        'nieuwsbrief.vakantie.be',
        'veilingen.vakantie.be',
        'biedmee.be',
        'www.biedmee.be',
        'account.biedmee.be',
    )

    def __init__(self):
        pass

    # vakantie.be forward uri
    FORWARD_URI = 'http://www.vakantie.be/pages/forward.aspx?RedirectPage='

    def url_prepare(self, uri, ezine_name=None):
        parse_result = urlparse(uri)
        if parse_result.netloc not in self.UTM_NETLOCS:
            return ''.join(( self.FORWARD_URI, quote_plus(uri) ))
        else:
            return append_utmcodes(uri, ezine_name)

    def url_encode(self, uri, ezine_name=None):
        parse_result = urlparse(uri)
        if parse_result.netloc in self.UTM_NETLOCS:
            return quote_plus(append_utmcodes(uri, ezine_name))
        else:
            return quote_plus(uri)

    def append_utmcodes(self, uri, ezine_name=None):
        parse_result = urlparse(uri)
        if parse_result.netloc in self.UTM_NETLOCS:
            query_list   = parse_qsl(parse_result.query)
            query_dict   = parse_qs(parse_result.query)
            self.DEF_UTM_DICT['utm_campaign'] = ezine_name
            for k, v in self.DEF_UTM_DICT.iteritems():
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
        else:
            return uri

    def parse_result_astuple(self, parse_result):
        t = (
            parse_result.scheme,
            parse_result.netloc,
            parse_result.path,
            parse_result.params,
            parse_result.query,
            parse_result.fragment
        )
        return t

    def datetimeformat(self, value, format='%H:%M / %d-%m-%Y'):
        return value.strftime(format)
