# -*- coding: utf-8 -*-

from DebianChangesBot import Message

import re


class SecurityAnnounceMessage(Message):
    FIELDS = ('dsa_number', 'dsa_revision', 'package', 'problem', 'year')

    def format(self):
        msg = "[red][Security][reset] ([yellow]DSA-%d-%d[reset]) - " % \
            (self.dsa_number, self.dsa_revision)

        msg += "New [green]%s[reset] packages fix %s. http://www.debian.org/security/%s/dsa-%d" % \
            (self.package, self.problem, self.year, self.dsa_number)

        return msg
