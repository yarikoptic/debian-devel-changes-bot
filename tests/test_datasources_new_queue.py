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

from DebianDevelChangesBot import Datasource
from DebianDevelChangesBot.datasources import NewQueue

class TestDatasourceTestingNewQueue(unittest.TestCase):

    def setUp(self):
        self.fixture = os.path.join(os.path.dirname(os.path.abspath(__file__)), \
            'fixtures', 'new_queue.html')

        self.datasource = NewQueue()

    def is_new(self, package, version):
        fileobj = open(self.fixture)
        self.datasource.update(fileobj)
        return self.datasource.is_new(package, version)

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

    def testTop(self):
        self.assert_(self.is_new('ganeti-instance-debian-etch', '0.4-1'))

    def testBottom(self):
        self.assert_(self.is_new('sugar-chat-activity', '37~git-2'))

    def testMultipleVersions(self):
        self.assert_(self.is_new('cpushare', '0.47-1'))
        self.assert_(self.is_new('cpushare', '0.47-2'))

    def testInvalidVersion(self):
        self.failIf(self.is_new('cpushare', '0.47-3'))

    def testNotInQueue(self):
        self.failIf(self.is_new('package-not-in-new-queue', 'version-foo'))

    def testByhand(self):
        self.assert_(self.is_new('loadlin', '1.6c.really1.6c-1.2'))

    def testExperimental(self):
        self.assert_(self.is_new('tagua', '1.0~alpha2-2'))

if __name__ == "__main__":
    unittest.main()
