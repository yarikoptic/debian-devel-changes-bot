# -*- coding: utf-8 -*-

from DebianChangesBot import Message
from DebianChangesBot.datasources import NewQueue

class UploadAcceptedMessage(Message):
    FIELDS = ('package', 'version', 'distribution', 'urgency', 'by')
    OPTIONAL = ('closes',)

    def format(self):
        msg = "[green]%s[reset] "

        if NewQueue().is_new(self.package):
            msg += "[red](NEW)[reset] "

        msg += "[yellow]%s[reset]) uploaded " % self.version

        if self.distribution != 'unstable':
            msg += "to [blue]%s[reset] "

        if self.urgency != 'low':
            msg += "with urgency [red]%s[reset]" % self.urgency

        msg += "by [cyan]%s[reset]" % self.format_email_address(self.by)

        if self.closes and '-backports' not in self.distribution:
            bug_list = ', '.join(["[b]#%s[/b]" % x for x in self.closes.split(' ')])
            msg += " (Closes: %s)" % bug_list

        msg += ". http://packages.qa.debian.org/%s" % self.package

        return msg
