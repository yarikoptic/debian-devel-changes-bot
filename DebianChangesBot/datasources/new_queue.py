# -*- coding: utf-8 -*-

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
