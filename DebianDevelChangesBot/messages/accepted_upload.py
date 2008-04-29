# -*- coding: utf-8 -*-
#
#   Debian Changes Bot
#   Copyright (C) 2008 Chris Lamb <chris@chris-lamb.co.uk>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from DebianDevelChangesBot import Message
from DebianDevelChangesBot.datasources import NewQueue

class AcceptedUploadMessage(Message):
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
