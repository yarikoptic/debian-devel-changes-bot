# -*- coding: utf-8 -*-

from DebianChangesBot import MailParser
from DebianChangesBot.messages import SecurityAnnounceMessage

import re

SUBJECT = re.compile(r'^\[SECURITY\] \[DSA ([\d]+)-([\d+])\] New ([^ ]+) packages fix (.*)$')
DATE = re.compile(r'(20\d\d)')

class SecurityAnnounceParser(MailParser):

    @staticmethod
    def parse(headers, body):
        if headers.get('List-Id', '') != '<debian-security-announce.lists.debian.org>':
            return

        msg = SecurityAnnounceMessage()

        m = SUBJECT.match(headers.get('Subject', ''))
        if m:
            try:
                msg.dsa_number = int(m.group(1))
                msg.dsa_revision = int(m.group(2))
            except ValueError:
                return

            msg.package = m.group(3)
            msg.problem = m.group(4)

        m = DATE.search(headers.get('Date', ''))
        if m:
            try:
                msg.year = int(m.group(1))
            except ValueError:
                return

        return msg
