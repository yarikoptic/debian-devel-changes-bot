# -*- coding: utf-8 -*-

from DebianChangesBot import MailParser
from DebianChangesBot.messages import BugClosedMessage

import re

SUBJECT = re.compile(r'^Bug#(\d+): marked as done \((.+)\)$')

class BugClosedParser(MailParser):

    def parse(self, headers, body):
        msg = BugClosedMessage()

        m = SUBJECT.match(headers['Subject'])
        if m:
            msg.bug_number = m.group(1)
            msg.title = m.group(2)
        else:
            return

        try:
            msg.by = headers['To']

            # Let source package name override binary package
            msg.package = headers['X-Debian-PR-Package']
            msg.package = headers['X-Debian-PR-Source']
        except KeyError:
            return

        # Strip package name prefix from title
        if msg.title.lower().startswith('%s: ' % msg.package.lower()):
            msg.title = data.title[len(msg.package) + 2:]

        # If bug was closed via 123456-done@bugs.debian.org, To: is wrong.
        if '-done@bugs.debian.org' in data.by:
            msg.by = headers['From']

        return msg
