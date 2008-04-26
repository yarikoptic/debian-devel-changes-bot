# -*- coding: utf-8 -*-

import urllib2

class Datasource(object):
    class DataError(Exception): pass

    def update(self):
        fileobj = urllib2.urlopen(self.URL)
        return self.parse(fileobj)

class MailParser(object):
    pass

class Message(object):
    def __init__(self):
        if hasattr(self, 'FIELDS'):
            for field in self.FIELDS:
                setattr(self, field, None)
        if hasattr(self, 'OPTIONAL'):
            for field in self.OPTIONAL:
                setattr(self, field, None)

    def __nonzero__(self):
        if hasattr(self, 'FIELDS'):
            for field in self.FIELDS:
                if getattr(self, field) is None:
                    return False
        return True
