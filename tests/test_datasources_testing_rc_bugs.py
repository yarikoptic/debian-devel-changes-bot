#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianChangesBot import Datasource
from DebianChangesBot.datasources import TestingRCBugs

class TestDatasourceTestingRCBugs(unittest.TestCase):

    def setUp(self):
        self.fixture = os.path.join(os.path.dirname(os.path.abspath(__file__)), \
            'fixtures', 'testing_rc_bugs.html')

        self.datasource = TestingRCBugs()

    def testURL(self):
        """
        Check we have a sane URL.
        """
        self.assert_(len(self.datasource.URL) > 5)
        self.assert_(self.datasource.URL.startswith('http'))
        self.assert_('dist' in self.datasource.URL)

    def testInterval(self):
        """
        Check we have a sane update interval.
        """
        self.assert_(self.datasource.INTERVAL > 60)

    def testParse(self):
        fileobj = open(self.fixture)
        self.datasource.update(fileobj)
        val = self.datasource.get_num_bugs()

        self.assert_(type(val) is int)
        self.assertEqual(val, 538)

    def testParseEmpty(self):
        fileobj = open('/dev/null')
        self.assertRaises(Datasource.DataError, self.datasource.update, fileobj)

if __name__ == "__main__":
    unittest.main()
