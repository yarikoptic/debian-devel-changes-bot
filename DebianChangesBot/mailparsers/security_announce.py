
from DebianChangesBot import MailParser
from DebianChangesBot.messages import SecurityAnnounceMessage

import re

SUBJECT = re.compile(r'^\[SECURITY\] \[DSA ([-\d]+)\] New ([^ ]+) packages fix (.*)$')
DATE = re.compile(r'(20\d\d)')

class SecurityAnnounceParser(MailParser):

    def parse(self, headers, body):
        if headers['List-Id'] != '<debian-security-announce.lists.debian.org>':
            return

        msg = SecurityAnnounceMessage()

        m = SUBJECT.match(headers['Subject'])
        if m:
            msg.dsa_number = m.group(1)
            msg.package = m.group(2)
            msg.problem = m.group(3)
        else:
            return

        m = DATE.search(headers['Date'])
        if m:
            msg.year = m.group(1)
        else:
            return

        return msg
