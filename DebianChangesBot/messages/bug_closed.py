# -*- coding: utf-8 -*-

from DebianChangesBot import Message

class BugClosedMessage(Message):
    FIELDS = ('bug_number', 'package', 'by', 'title')

    def format(self, data):
        return "Closed [b]#%d[/b] in [green]%s[reset] by [cyan]%s[reset] " \
            "«%s». http://bugs.debian.org/%d" % \
            (self.bug_number, self.package, self.by, self.bug_number)
