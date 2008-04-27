# -*- coding: utf-8 -*-

import re

# Import these directly due to funkiness in Python 2.4's email library
import email.Header
import email.quopriMIME

def header_decode(s):
    def unquote_match(match):
        s = match.group(0)
        return chr(int(s[1:3], 16))

    s = s.replace('_', ' ')
    return re.sub(r'=\w{2}', unquote_match, s)

def quoted_printable(val):
    try:
        if type(val) is str:
            save = header_decode(val)
            val = ' '.join([chunk.decode(encoding or 'ascii', 'replace') for chunk, encoding in
                email.Header.decode_header(val)])

            if len(val) > len(save):
                val = unicode(save, 'utf-8', 'replace')

        else:
            return unicode(email.quopriMIME.header_decode(str(val)), 'utf-8', 'replace')

    except Exception, e:
        # We ignore errors here. Most of these originate from a spam
        # report adding a synopsis of a message with broken encodings.
        pass

    return val
