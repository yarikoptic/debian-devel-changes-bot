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

import socket
socket.setdefaulttimeout(10)

from DebianDevelChangesBot import Datasource

class NewQueue(Datasource):
    _shared_state = {}

    URL = 'http://ftp-master.debian.org/new.html'
    INTERVAL = 60 * 30

    packages = {}
    lock = thread.allocate_lock()

    def __init__(self):
        self.__dict__ = self._shared_state

    def update(self, fileobj=None):
        self.lock.acquire()
        try:
            if fileobj is None:
                fileobj = urllib2.urlopen(self.URL)

            soup = BeautifulSoup(fileobj)

            packages = {}
            for row in soup('tr', {'class': ('odd', 'even')}):
                package = row.td.string
                versions = [v.string for v in row.contents[3].findAll('a')]
                packages[package] = versions

            self.packages = packages
        finally:
            self.lock.release()

    def is_new(self, package, version):
        self.lock.acquire()
        try:
            versions = self.packages.get(package, [])
            return version in versions
        finally:
            self.lock.release()

    def get_size(self):
        self.lock.acquire()
        try:
            size = len(self.packages)
            if size > 0:
                return size
            return None
        finally:
            self.lock.release()
