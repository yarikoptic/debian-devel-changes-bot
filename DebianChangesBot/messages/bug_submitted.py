# -*- coding: utf-8 -*-

from DebianChangesBot import Message

class BugSubmittedMessage(Message):
    FIELDS = ('bug_number', 'package', 'by', 'title')
    OPTIONAL = ('severity', 'version')

    def format(self):
        msg = "Opened [b]#%d[/b] " % self.bug_number

        if self.severity in ('critical', 'grave', 'serious'):
            msg += "([red]%s[reset]) " % self.severity

        msg += "in [green]%s[reset] " % self.package

        if self.version not in ('n/a'):
            msg += "([yellow]%s[reset]) " % self.version

        msg += "by [cyan]%s[reset] " % self.format_email_address(self.by)
        msg += "«%s». http://bugs.debian.org/%d" % \
            (self.by, self.title, self.bug_number)

        return msg
