#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianChangesBot import Datasource
from DebianChangesBot.datasources import NewQueue

class TestDatasourceTestingRCBugs(unittest.TestCase):

    def setUp(self):
        self.fixture = os.path.join(os.path.dirname(os.path.abspath(__file__)), \
            'fixtures', 'new_queue.html')

        self.datasource = NewQueue()

    def parse(self):
        fileobj = open(self.fixture)
        return self.datasource.parse(fileobj)

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

    def testType(self):
        val = self.parse()
        iter(val)

    def testElemTypes(self):
        val = self.parse()
        for package in val:
            self.assertEqual(type(package), str)

    def testLength(self):
        val = self.parse()
        self.assertEqual(len(val), 110)


if __name__ == "__main__":
    unittest.main()
