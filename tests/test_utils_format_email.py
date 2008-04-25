#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianChangesBot import Message

class TestFormatEmail(unittest.TestCase):

    def setUp(self):
        self.message = Message()

    def testSimple(self):
        pass

    def testDebian(self):
        val = "John Smith <jsmith@debian.org>"
        ret = "John Smith (jsmith)"
        self.assertEqual(self.message.format_email_address(val), ret)

    def testDebianQuotes(self):
        val = '"John Smith" <jsmith@debian.org>'
        ret = "John Smith (jsmith)"
        self.assertEqual(self.message.format_email_address(val), ret)

        val = "'John Smith' <jsmith@debian.org>"
        ret = "John Smith (jsmith)"
        self.assertEqual(self.message.format_email_address(val), ret)

    def testNonNormalDebianEmail(self):
        val = 'John Smith <jsmith@merkel.debian.org>'
        ret = 'John Smith (jsmith)'
        self.assertEqual(self.message.format_email_address(val), ret)

        val = 'John Smith <jsmith@master.debian.org>'
        ret = 'John Smith (jsmith)'
        self.assertEqual(self.message.format_email_address(val), ret)

    def testUppercaseDebianEmail(self):
        val = 'John Smith <JSMITH@DEBIAN.ORG>'
        ret = "John Smith (jsmith)"
        self.assertEqual(self.message.format_email_address(val), ret)

    def testUppercaseEmail(self):
        val = 'John Smith <JSMITH@HOST.TLD>'
        ret = "John Smith <jsmith@host.tld>"
        self.assertEqual(self.message.format_email_address(val), ret)

    def testExtraSpacesOne(self):
        val = "John  Smith <jsmith@host.tld>"
        ret = "John Smith <jsmith@host.tld>"
        self.assertEqual(self.message.format_email_address(val), ret)

        val = "John Smith  <jsmith@host.tld>"
        ret = "John Smith <jsmith@host.tld>"
        self.assertEqual(self.message.format_email_address(val), ret)

    def testExtraSpacesTwo(self):
        val = "John Smith < jsmith@host.tld>"
        ret = "John Smith <jsmith@host.tld>"
        self.assertEqual(self.message.format_email_address(val), ret)

        val = "John Smith < jsmith@host.tld>"
        ret = "John Smith <jsmith@host.tld >"
        self.assertEqual(self.message.format_email_address(val), ret)

    def testDontRepeatName(self):
        val = "John Smith (jsmith) <jsmith@debian.org>"
        ret = "John Smith (jsmith)"
        self.assertEqual(self.message.format_email_address(val), ret)

        val = "John Smith (JSMITH) <jsmith@debian.org>"
        ret = "John Smith (jsmith)"
        self.assertEqual(self.message.format_email_address(val), ret)

if __name__ == "__main__":
    unittest.main()
