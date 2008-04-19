
from DebianChangesBot import MailParser
from DebianChangesBot.formatters import BugClosedFormatter

import re

SUBJECT = re.compile(r'^Bug#(\d+): marked as done \((.+)\)$')

class BugClosedParser(MailParser):

    def parse(self, headers, body):
        fmt = BugClosedFormatter()

        m = SUBJECT.match(headers['Subject'])
        if m:
            fmt.bug_number = m.group(1)
            fmt.title = m.group(2)
        else:
            return

        try:
            fmt.by = headers['To']

            # Let source package name override binary package
            fmt.package = headers['X-Debian-PR-Package']
            fmt.package = headers['X-Debian-PR-Source']
        except KeyError:
            return

        # Strip package name prefix from title
        if fmt.title.lower().startswith('%s: ' % fmt.package.lower()):
            fmt.title = data.title[len(fmt.package) + 2:]

        # If bug was closed via 123456-done@bugs.debian.org, To: is wrong.
        if '-done@bugs.debian.org' in data.by:
            fmt.by = headers['From']

        return fmt
