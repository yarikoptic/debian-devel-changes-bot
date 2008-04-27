# -*- coding: utf-8 -*-

from DebianChangesBot import MailParser
from DebianChangesBot.utils import tidy_bug_title
from DebianChangesBot.messages import BugSubmittedMessage

import re

SUBJECT = re.compile(r'^Bug#(\d+): (.+)$')

BTS = re.compile(r'^# Automatically generated email from bts')
FOLLOWUP_FOR = re.compile(r'(?i)^Followup-For:? .+')
PACKAGE = re.compile(r'(?i)^Package:? ([^\s]{1,40})$')
VERSION = re.compile(r'(?i)^Version:? ([^\s]{1,20})$')
SEVERITY = re.compile(r'(?i)^Severity:? (critical|grave|serious|important|normal|minor|wishlist)$')

class BugSubmittedParser(MailParser):

    @staticmethod
    def parse(headers, body):
        if headers.get('List-Id', '') != '<debian-bugs-dist.lists.debian.org>':
            return

        msg = BugSubmittedMessage()

        m = SUBJECT.match(headers['Subject'])
        if m:
            msg.bug_number = int(m.group(1))
            msg.title = m.group(2)
        else:
            return

        msg.by = headers['From']

        mapping = {
            PACKAGE: 'package',
            VERSION: 'version',
            SEVERITY: 'severity',
        }

        for line in body[:10]:
            if BTS.match(line) or FOLLOWUP_FOR.match(line):
                return

            for command in ('thanks', 'kthxbye'):
                if line.startswith(command):
                    return

            for command in ('retitle', 'reassign'):
                if line.startswith('%s %d' % (command, msg.bug_number)):
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

        if type(msg.version) is str and msg.version.find('GnuPG') != -1:
            msg.version = None

        if not msg.package:
            return

        msg.title = tidy_bug_title(msg.title, msg.package)

        return msg
