# -*- coding: utf-8 -*-

from DebianChangesBot import MailParser
from DebianChangesBot.messages import BugSubmittedMessage

import re

SUBJECT = re.compile(r'^Bug#(\d+): (.+)$')

FOLLOWUP_FOR = re.compile(r'(?i)^Followup-For:? .+')
PACKAGE = re.compile(r'(?i)^Package:? ([^\s]{1,40})$')
VERSION = re.compile(r'(?i)^Version:? (.{1,50})$')
SEVERITY = re.compile(r'(?i)^Severity:? (critical|grave|serious|important|normal|minor|wishlist)$')

class BugSubmittedParser(MailParser):

    @staticmethod
    def parse(headers, body):
        msg = BugSubmittedMessage()

        m = SUBJECT.match(header['Subject'])
        if m:
            msg.bug_number = m.group(1)
            msg.title = m.group(2)
        else:
            return

        msg.by = headers['From']

        # Strip package name prefix from title
        if msg.title.lower().startswith('%s: ' % msg.package.lower()):
            msg.title = data.title[len(msg.package) + 2:]

        mapping = {
            PACKAGE: 'package',
            VERSION: 'version',
            SEVERITY: 'severity',
        }

        for line in body[:10]:
            if FOLLOWUP_FOR.match(line):
                return

            for pattern, target in mapping.iteritems():
                m = pattern.match(line)
                if m:
                    val = m.group(1).lower()
                    setattr(msg, target, val)
                    del mapping[pattern]
                    break

            if len(mapping.keys()) == 0:
                break

        if msg.version.find('GnuPG') != -1:
            msg.version = None

        return msg
