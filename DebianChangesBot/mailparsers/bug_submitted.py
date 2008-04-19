
from DebianChangesBot import MailParser
from DebianChangesBot.formatters import BugSubmittedFormatter

import re

SUBJECT = re.compile(r'^Bug#(\d+): (.+)$')

FOLLOWUP_FOR = re.compile(r'(?i)^Followup-For:? .+')
PACKAGE = re.compile(r'(?i)^Package:? ([^\s]{1,40})$')
VERSION = re.compile(r'(?i)^Version:? (.{1,50})$')
SEVERITY = re.compile(r'(?i)^Severity:? (critical|grave|serious|important|normal|minor|wishlist)$')

class BugSubmittedParser(MailParser):

    def parse(self, headers, body):
        fmt = BugSubmittedFormatter()

        m = SUBJECT.match(header['Subject'])
        if m:
            fmt.bug_number = m.group(1)
            fmt.title = m.group(2)
        else:
            return

        fmt.by = headers['From']

        # Strip package name prefix from title
        if fmt.title.lower().startswith('%s: ' % fmt.package.lower()):
            fmt.title = data.title[len(fmt.package) + 2:]

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
                    setattr(fmt, target, val)
                    del mapping[pattern]
                    break

            if len(mapping.keys()) == 0:
                break

        if fmt.version.find('GnuPG') != -1:
            fmt.version = None

        return fmt
