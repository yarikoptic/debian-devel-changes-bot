import urllib2

class Datasource(object):
    class DataError(Exception): pass

    def update(self):
        fileobj = urllib2.urlopen(self.URL)
        return self.parse(fileobj)

import datasources
