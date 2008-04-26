#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianChangesBot.utils import tidy_bug_title

class TestFormatEmail(unittest.TestCase):
    def _test(self, title, package, ret):
        self.assertEqual(tidy_bug_title(title, package), ret)

    def testMatch(self):
        self._test("[a]: b", "a", "b")

    def testNoMatch(self):
        self._test("[a]: b", "c", "[a]: b")

    def testNoBraceMatch(self):
        self._test("a: b", "a", "b")

    def testNoBraceNoMatch(self):
        self._test("a: b", "c", "a: b")

    def testNoColonMatch(self):
        self._test("[a] b", "a", "b")

    def testNoColonNoMatch(self):
        self._test("[a] b", "c", "[a] b")

if __name__ == "__main__":
    unittest.main()
