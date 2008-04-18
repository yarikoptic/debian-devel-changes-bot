
import re

from DebianChangesBot import Datasource

class TestingRCBugs(Datasource):
    URL = 'http://bts.turmzimmer.net/details.php?bydist=lenny'
    INTERVAL = 60 * 30

    pattern = re.compile(r'.*Total shown: (?P<bug_count>\d+) bug.*')

    def parse(self, fileobj):
        for line in fileobj:
            ret = self.pattern.match(line)
            if ret:
                val = ret.group('bug_count')
                return int(val)

        raise Datasource.DataError()
