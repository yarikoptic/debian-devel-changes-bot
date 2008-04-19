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
    def format_email_address(self, email):
        email = re.sub(r'(?:<([-A-Za-z0-9]+)@debian.org>)', r'(\1)', email)
        email = re.sub(r'@(.{6}).*>', r'@\1..>', email)
        return email.replace(r'"', '')
