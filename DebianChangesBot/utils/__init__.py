# -*- coding: utf-8 -*-

def tidy_bug_title(title, package):
    # Strip package name prefix from title
    for prefix in ('%s: ', '[%s]: '):
        if title.lower().startswith(prefix % package.lower()):
            title = title[len(package) + len(prefix) - 2:]

    return title

from decoding import header_decode, quoted_printable
from parse_mail import parse_mail
from format_email_address import format_email_address
