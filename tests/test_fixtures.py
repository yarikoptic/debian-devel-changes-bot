#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianChangesBot.messages import *
from DebianChangesBot.mailparsers import *
from DebianChangesBot.utils import parse_mail

from glob import glob

class TestFixtures(unittest.TestCase):

    def _test_dir(self, dir, parser, expected_type, test=lambda x: bool(x)):
        dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
            'fixtures', dir, '*')

        for filename in glob(dir):
            try:
                headers, body = parse_mail(file(filename))
                msg = parser.parse(headers, body)
            except Exception:
                print "Exception when parsing %s" % filename
                raise

            if type(msg) != expected_type:
                print
                print filename, "did not match"
            self.assertEqual(type(msg), expected_type)

            if not test(msg):
                print
                print filename, "did not pass test"
            self.assert_(test(msg))

    def testAcceptedUpload(self):
        self._test_dir('accepted_upload', AcceptedUploadParser, AcceptedUploadMessage)

    def testBugClosed(self):
        self._test_dir('bug_closed', BugClosedParser, BugClosedMessage)

    def testBugSubmitted(self):
        self._test_dir('bug_submitted', BugSubmittedParser, BugSubmittedMessage)

    def testSecurityAnnounce(self):
        self._test_dir('security_announce', SecurityAnnounceParser, SecurityAnnounceMessage)

    def testNoMatch(self):
        for parser in AcceptedUploadParser, BugClosedParser, BugSubmittedParser, SecurityAnnounceParser:
            self._test_dir('non_messages', parser, type(None), test=lambda x: not bool(x))

if __name__ == "__main__":
    unittest.main()
