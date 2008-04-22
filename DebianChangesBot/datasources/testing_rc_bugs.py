# -*- coding: utf-8 -*-

import re
import thread

from DebianChangesBot import Datasource

class TestingRCBugs(Datasource):
    __shared_state = {}

    URL = 'http://bts.turmzimmer.net/details.php?bydist=lenny'
    BUG_COUNT = re.compile(r'.*Total shown: (?P<bug_count>\d+) bug.*')
    INTERVAL = 60 * 30

    lock = thread.allocate_lock()
    num_bugs = None

    def __init__(self):
        self.__dict__ = self.__shared_state

    def update(self, fileobj):
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
