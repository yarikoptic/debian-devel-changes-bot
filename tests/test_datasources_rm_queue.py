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
from DebianDevelChangesBot.datasources import RmQueue

class TestDatasourceTestingRmQueue(unittest.TestCase):

    def setUp(self):
        self.datasource = RmQueue()

        fixture = os.path.join(os.path.dirname(os.path.abspath(__file__)), \
            'fixtures', 'rm_queue.html')
        self.datasource.update(open(fixture))

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

    def testSize(self):
        self.assertEqual(self.datasource.get_size(), 10)

    def testTop(self):
        self.assert_(self.datasource.is_rm('libgocr'))

    def testBottom(self):
        self.assert_(self.datasource.is_rm('sablevm-classlib'))

if __name__ == "__main__":
    unittest.main()
