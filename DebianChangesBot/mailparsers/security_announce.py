
from DebianChangesBot import MailParser
from DebianChangesBot.formatters import SecurityAnnounceFormatter

import re

SUBJECT = re.compile(r'^\[SECURITY\] \[DSA ([-\d]+)\] New ([^ ]+) packages fix (.*)$')
DATE = re.compile(r'(20\d\d)')

class SecurityAnnounceParser(MailParser):

    def parse(self, headers, body):
        if headers['List-Id'] != '<debian-security-announce.lists.debian.org>':
            return

        fmt = SecurityAnnounceFormatter()

        m = SUBJECT.match(headers['Subject'])
        if m:
            fmt.dsa_number = m.group(1)
            fmt.package = m.group(2)
            fmt.problem = m.group(3)
        else:
            return

        m = DATE.search(headers['Date'])
        if m:
            fmt.year = m.group(1)
        else:
            return

        return fmt
