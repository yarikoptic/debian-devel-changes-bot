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

from DebianDevelChanges import Datasource
from DebianDevelChanges.datasources import NewQueue

class TestDatasourceTestingRCBugs(unittest.TestCase):

    def setUp(self):
        self.fixture = os.path.join(os.path.dirname(os.path.abspath(__file__)), \
            'fixtures', 'new_queue.html')

        self.datasource = NewQueue()

    def is_new(self, package):
        fileobj = open(self.fixture)
        self.datasource.update(fileobj)
        return self.datasource.is_new(package)

    def testURL(self):
        """
        Check we have a sane URL.
        """
        self.assert_(len(self.datasource.URL) > 5)
        self.assert_(self.datasource.URL.startswith('http'))

    def testInterval(self):
        """
        Check we have a sane update interval.
        """
        self.assert_(self.datasource.INTERVAL > 60)

    def testParseEmpty(self):
        fileobj = open('/dev/null')
        self.assertRaises(Datasource.DataError, self.datasource.update, fileobj)

    def testTop(self):
        self.assert_(self.is_new('ganeti-instance-debian-etch'))

    def testBottom(self):
        self.assert_(self.is_new('sugar-chat-activity'))

    def testMultipleVersions(self):
        self.assert_(self.is_new('cpushare'))

    def testNotInQueue(self):
        self.failIf(self.is_new('package-not-in-new-queue'))

    def testByhand(self):
        self.assert_(self.is_new('loadlin'))

    def testExperimental(self):
        self.assert_(self.is_new('tagua'))

if __name__ == "__main__":
    unittest.main()
