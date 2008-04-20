#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianChangesBot.mailparsers import SecurityAnnounceParser as p

class TestMailParserSecurityAnnounce(unittest.TestCase):

    def setUp(self):
        self.headers = {
            'List-Id': '<debian-security-announce.lists.debian.org>',
            'Date': 'Sat, 19 Apr 2008 19:18:38 +0100',
            'Subject': '[SECURITY] [DSA 1234-5] New pinafore packages ' \
                'fix inertial dampener problem',
        }

    def testSimple(self):
        msg = p.parse(self.headers, [])

        self.assert_(msg)
        self.assertEqual(msg.dsa_number, 1234)
        self.assertEqual(msg.dsa_revision, 5)
        self.assertEqual(msg.package, 'pinafore')
        self.assertEqual(msg.problem, 'inertial dampener problem')
        self.assertEqual(msg.year, 2008)

    def testNoDate(self):
        del self.headers['Date']
        self.failIf(p.parse(self.headers, []))

    def testNoSubject(self):
        del self.headers['Subject']
        self.failIf(p.parse(self.headers, []))

    def testNoListId(self):
        del self.headers['List-Id']
        self.failIf(p.parse(self.headers, []))

    def testWrongListId(self):
        self.headers['List-Id'] = '<debian-ponies-announce.lists.debian.org>'
        self.failIf(p.parse(self.headers, []))

if __name__ == "__main__":
    unittest.main()
