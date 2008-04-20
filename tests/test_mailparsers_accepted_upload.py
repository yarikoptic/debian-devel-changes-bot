#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianChangesBot.mailparsers import AcceptedUploadParser as p

class TestMailParserAcceptedUpload(unittest.TestCase):

    def setUp(self):
        self.body = [
            '-----BEGIN PGP SIGNED MESSAGE-----',
            'Hash: SHA1',
            '',
            'Format: 1.7',
            'Date: Thu, 03 Apr 2008 11:45:26 +0100',
            'Source: haskell-irc',
            'Binary: libghc6-irc-dev libghc6-irc-doc',
            'Architecture: source i386 all',
            'Version: 0.4.2-1',
            'Distribution: unstable',
            'Urgency: low',
            'Maintainer: Chris Lamb <chris@chris-lamb.co.uk>',
            'Changed-By: Chris Lamb <chris@chris-lamb.co.uk>',
            'Description: ',
            ' libghc6-irc-dev - GHC 6 libraries for the Haskell IRC library',
            ' libghc6-irc-doc - GHC 6 libraries for the Haskell IRC library (documentation)',
            'Changes: ',
            # etc.
        ]

    def testSimple(self):
        msg = p.parse({}, self.body)

        self.assert_(msg)
        self.assertEqual(msg.package, 'haskell-irc')
        self.assertEqual(msg.version, '0.4.2-1')
        self.assertEqual(msg.distribution, 'unstable')
        self.assertEqual(msg.urgency, 'low')
        self.assertEqual(msg.by, 'Chris Lamb <chris@chris-lamb.co.uk>')
        self.assertEqual(msg.closes, None)

    def testCloses(self):
        self.body.append('Closes: 123456 456123')
        msg = p.parse({}, self.body)

        self.assert_(msg)
        self.assertEqual(msg.closes, [123456, 456123])


if __name__ == "__main__":
    unittest.main()
