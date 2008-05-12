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

import re
import thread
import urllib2

import socket
socket.setdefaulttimeout(10)

from DebianDevelChangesBot import Datasource

class TestingRCBugs(Datasource):
    __shared_state = {}

    URL = 'http://bts.turmzimmer.net/details.php?bydist=lenny'
    BUG_COUNT = re.compile(r'.*Total shown: (?P<bug_count>\d+) bug.*')
    INTERVAL = 60 * 10

    lock = thread.allocate_lock()
    num_bugs = None

    def __init__(self):
        self.__dict__ = self.__shared_state

    def update(self, fileobj=None):
        if fileobj is None:
            fileobj = urllib2.urlopen(self.URL)

        for line in fileobj:
            ret = self.BUG_COUNT.match(line)
            if ret:
                self.lock.acquire()
                try:
                    self.num_bugs = int(ret.group('bug_count'))
                    return
                finally:
                    self.lock.release()

        # No bug count line found
        raise Datasource.DataError()

    def get_num_bugs(self):
        self.lock.acquire()
        try:
            return self.num_bugs
        finally:
            self.lock.release()
