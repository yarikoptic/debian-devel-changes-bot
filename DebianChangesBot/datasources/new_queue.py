# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup

from DebianChangesBot import Datasource

class NewQueue(Datasource):
    URL = 'http://ftp-master.debian.org/new.html'
    INTERVAL = 60 * 30

    def parse(self, fileobj):
        soup = BeautifulSoup(fileobj)
        cells = [row.find('td') for row in soup('tr', {'class': ('odd', 'even')})]
        packages = [str(c.string) for c in cells]

        return packages
