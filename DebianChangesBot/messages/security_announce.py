# -*- coding: utf-8 -*-

from DebianChangesBot import Message

import re

PATTERN_DSA = re.compile(r'-\d+$')

class SecurityAnnounceMessage(Message):
    FIELDS = ('dsa_number', 'package', 'problem', 'year')

    def format(self):
        url = 'http://www.debian.org/security/%s/dsa-%s' % \
            (self.year, PATTERN_DSA.sub('', self.dsa_number))

        return "[red][Security][reset] ([yellow]DSA-%d[reset]) - " \
            "New [green]%s[reset] packages fix %s. %(url)s" % \
            (self.dsa_number, self.package, self.problem, url)
