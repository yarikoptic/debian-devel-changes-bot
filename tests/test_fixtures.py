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
    count = 0

def add_tests(testdir, parser, expected_type, test=lambda x: bool(x)):
    testdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'fixtures', testdir, '*')

    for filename in glob(testdir):
        def testFunc(self, filename=filename):
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

        TestFixtures.count += 1
        setattr(TestFixtures, 'test%d' % TestFixtures.count, testFunc)

add_tests('accepted_upload', AcceptedUploadParser, AcceptedUploadMessage)
add_tests('bug_closed', BugClosedParser, BugClosedMessage)
add_tests('bug_submitted', BugSubmittedParser, BugSubmittedMessage)
add_tests('bug_submitted', BugSubmittedParser, BugSubmittedMessage)
add_tests('security_announce', SecurityAnnounceParser, SecurityAnnounceMessage)

for parser in AcceptedUploadParser, BugClosedParser, BugSubmittedParser, SecurityAnnounceParser:
    add_tests('non_messages', parser, type(None), test=lambda x: not bool(x))

if __name__ == "__main__":
    unittest.main()
