#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianChangesBot.mailparsers import BugClosedParser as p

class TestMailParserBugClosed(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
