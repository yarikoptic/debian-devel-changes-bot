# -*- coding: utf-8 -*-

from DebianChangesBot import MailParser
from DebianChangesBot.utils import tidy_bug_title
from DebianChangesBot.messages import BugClosedMessage

import re

SUBJECT = re.compile(r'^Bug#(\d+): marked as done \((.+)\)$')

class BugClosedParser(MailParser):

    @staticmethod
    def parse(headers, body):
        if headers.get('List-Id', '') != '<debian-bugs-closed.lists.debian.org>':
            return

        msg = BugClosedMessage()

        m = SUBJECT.match(headers['Subject'])
        if m:
            msg.bug_number = int(m.group(1))
            msg.title = m.group(2)
        else:
            return

        msg.by = headers['To']

        # Let binary package name override binary package
        msg.package = headers.get('X-Debian-PR-Source', None)
        msg.package = headers['X-Debian-PR-Package']

        msg.title = tidy_bug_title(msg.title, msg.package)

        return msg
