#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianChangesBot.mailparsers import BugSubmittedParser as p

class TestMailParserBugSubmitted(unittest.TestCase):

    def setUp(self):
        self.headers = {
            'Subject': 'Bug#123456: Bug title',
            'From': 'Submitter Name <name@host.tld>',
        }

        self.body = [
            "Package: package-name",
            "Version: version-here",
            "",
            "Description"
        ]

    def testSimple(self):
        msg = p.parse(self.headers, self.body)

        self.assert_(msg)
        self.assertEqual(msg.package, 'package-name')
        self.assertEqual(msg.version, 'version-here')
        self.assertEqual(msg.by, 'Submitter Name <name@host.tld>')

    def testVersionWithSpaces(self):
        self.body[1] = "Version: version with spaces"
        msg = p.parse(self.headers, self.body)

        self.failIf(msg.version)

if __name__ == "__main__":
    unittest.main()
