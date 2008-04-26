# -*- coding: utf-8 -*-

import re

EMAIL = re.compile(r'^(.*) ?(<.+@.+>)$')
DEBIAN_EMAIL = re.compile(r'^<([-a-z0-9]+)@(?:merkel\.|master\.)?debian.org>$')

WHITESPACE = re.compile(r'\s{2,}')
CONTINUATION = re.compile(r'\.{3,}$')

def format_email_address(input, max_user=10, max_domain=8):
    m = EMAIL.match(input)
    if not m:
        return input

    # Name
    name = m.group(1).strip()
    name = WHITESPACE.sub(' ', name)

    # Remove quotes around name
    for quote in ("'", '"'):
        if len(name) > 0 and name[0] == quote and name[-1] == quote:
            name = name[1:-1]

    # Email address
    address = m.group(2).lower().replace(' ', '')
    address = WHITESPACE.sub(' ', address)

    if DEBIAN_EMAIL.match(address):
        address = DEBIAN_EMAIL.sub(r'(\1)', address)

        # Remove duplications of Debian user suffixed to name
        if name.lower().endswith(address.lower()):
            name = name[:-len(address)-1]

    else:
        # Shorten email address
        user, host = address[1:-1].split('@')
        if len(user) > max_user:
            user = "%s..." % user[:max_user]
        if len(host) > max_domain:
            host = "%s..." % host[:max_domain]

        # Normalise triple-dots
        user = CONTINUATION.sub('...', user)
        host = CONTINUATION.sub('...', host)

        address = "<%s@%s>" % (user, host)

    ret = "%s %s" % (name, address)
    return ret.strip()
