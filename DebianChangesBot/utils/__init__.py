# -*- coding: utf-8 -*-

import email.quoprimime

def quoted_printable(val):
    try:
        if type(val) is str:
            return email.quoprimime.header_decode(val)
        else:
            return unicode(email.quoprimime.header_decode(str(val)), 'utf-8')

    except Exception, e:
        # We ignore errors here. Most of these originate from a spam
        # report adding a synopsis of a message with broken encodings.
        pass

    return val

from parse_mail import parse_mail
