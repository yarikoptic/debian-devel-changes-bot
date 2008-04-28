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

import thread
import urllib2
from BeautifulSoup import BeautifulSoup

from DebianChangesBot import Datasource

class NewQueue(Datasource):
    __shared_state = {}

    URL = 'http://ftp-master.debian.org/new.html'
    INTERVAL = 60 * 30

    packages = []
    lock = thread.allocate_lock()

    def __init__(self):
        self.__dict__ = self.__shared_state

    def update(self, fileobj=None):
        if fileobj is None:
            fileobj = urllib2.urlopen(self.URL)

        soup = BeautifulSoup(fileobj)
        cells = [row.find('td') for row in soup('tr', {'class': ('odd', 'even')})]
        packages = [str(c.string) for c in cells]

        if len(packages) == 0:
            raise Datasource.DataError()

        self.lock.acquire()
        try:
            self.packages = packages
        finally:
            self.lock.release()

    def is_new(self, package):
        self.lock.acquire()
        try:
            return package in self.packages
        finally:
            self.lock.release()
