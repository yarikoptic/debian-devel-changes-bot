# -*- coding: utf-8 -*-

import email

from DebianChangesBot.utils import quoted_printable

def parse_mail(fileobj):
    headers, body = {}, []
    msg = email.message_from_file(fileobj)

    def decode(val):
        return unicode(val, 'utf-8', 'replace').replace('\n', '')

    for k, v in msg.items():
        v = quoted_printable(v)
        headers[k] = decode(v).strip()

    for line in email.iterators.body_line_iterator(msg):
        body.append(decode(line))

    # Merge lines joined with "=\n"
    i = len(body) - 1
    while i > 0:
        i -= 1
        prev = body[i]
        if len(prev) == 74 and prev.endswith('='):
            body[i] = body[i][:-1] + body[i + 1]
            del body[i + 1]

    # Remove =20 from end of lines
    i = 0
    while i < len(body):
        if body[i].endswith('=20'):
            body[i] = body[i][:-3] + ' '
        i += 1

    return headers, body
