#!/usr/bin/env python
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

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianDevelChangesBot.mailparsers import BugClosedParser as p

class TestMailParserBugClosed(unittest.TestCase):
    def setUp(self):
        self.headers = {
            'List-Id': '<debian-bugs-closed.lists.debian.org>',
        }

        self.body = []

    def testDone(self):
        self.headers.update({
            'Subject': 'Bug#479099: marked as done (please add random mode)',
            'From': u'Adeodato Simó <dato@net.com.org.es>',
            'To': 'Felipe Sateler <fsateler@gmail.com>, 479099-done@bugs.debian.org',
            'X-Debian-PR-Source': 'minirok-source-package',
            'X-Debian-PR-Package': 'minirok',
        })

        msg = p.parse(self.headers, self.body)
        self.assert_(msg)
        self.assertEqual(msg.bug_number, 479099)
        self.assertEqual(msg.package, 'minirok')
        self.assertEqual(msg.by, u'Adeodato Simó <dato@net.com...>')
        self.assertEqual(msg.title, 'please add random mode')

if __name__ == "__main__":
    unittest.main()
