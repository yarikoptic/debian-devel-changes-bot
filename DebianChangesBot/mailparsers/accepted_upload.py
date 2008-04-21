# -*- coding: utf-8 -*-

from DebianChangesBot import MailParser
from DebianChangesBot.messages import AcceptedUploadMessage

class AcceptedUploadParser(MailParser):

    @staticmethod
    def parse(headers, body):
        if headers.get('List-Id', '') != '<debian-devel-changes.lists.debian.org>':
            return

        msg = AcceptedUploadMessage()

        mapping = {
            'Source': 'package',
            'Version': 'version',
            'Distribution': 'distribution',
            'Urgency': 'urgency',
            'Changed-By': 'by',
            'Closes': 'closes',
        }

        for line in body:
            for field, target in mapping.iteritems():
                if line.startswith('%s: ' % field):
                    val = line[len(field) + 2:]
                    setattr(msg, target, val)
                    del mapping[field]
                    break

            # If we have found all the field, stop looking
            if len(mapping) == 0:
                break

        try:
            if msg.closes:
                msg.closes = [int(x) for x in msg.closes.split(' ')]
        except ValueError:
            return

        return msg
