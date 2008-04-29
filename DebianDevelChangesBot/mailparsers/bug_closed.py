# -*- coding: utf-8 -*-
#
#   Debian Changes Bot
#   Copyright (C) 2008 Chris Lamb <chris@chris-lamb.co.uk>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from DebianDevelChangesBot import MailParser
from DebianDevelChangesBot.utils import tidy_bug_title
from DebianDevelChangesBot.messages import BugClosedMessage

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
