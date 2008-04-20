# -*- coding: utf-8 -*-

import email

def parse_mail(fileobj):
    headers, body = {}, []
    msg = email.message_from_file(fileobj)

    for k, v in msg.items():
        val = v.strip().replace('\n', '')
        headers[k] = unicode(val)

    for line in email.iterators.body_line_iterator(msg):
        val = unicode(line.rstrip())
        body.append(val)

    # Merge lines joined with "=\n"
    i = len(body) - 1
    while i > 0:
        i -= 1
        prev = body[i]
        if len(prev) == 74 and prev.endswith('='):
            body[i] = body[i][:-1] + body[i + 1]
            del body[i + 1]


    return headers, body
