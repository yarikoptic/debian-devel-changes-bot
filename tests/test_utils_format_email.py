
import unittest

class TestFormatEmail(unittest.TestCase):


    def testSimple(self):
        pass

    def testDebian(self):
        val = "John Smith <jsmith@debian.org>"
        ret = "John Smith (jsmith)"

    def testDebianQuotes(self):
        val = '"John Smith" <jsmith@debian.org>'
        ret = "John Smith (jsmith)"

        val = "'John Smith' <jsmith@debian.org>"
        ret = "John Smith (jsmith)"

    def testUppercaseDebianEmail(self):
        val = 'John Smith <JSMITH@DEBIAN.ORG>'
        ret = "John Smith (jsmith)"

    def testUppercaseEmail(self):
        val = 'John Smith <JSMITH@HOST.TLD>'
        ret = "John Smith <jsmith@host.tld>"

    def testExtraSpacesOne(self):
        val = "John  Smith <jsmith@host.tld>"
        ret = "John Smith <jsmith@host.tld>"

        val = "John Smith  <jsmith@host.tld>"
        ret = "John Smith <jsmith@host.tld>"

    def testExtraSpacesTwo(self):
        val = "John Smith < jsmith@host.tld>"
        ret = "John Smith <jsmith@host.tld>"

        val = "John Smith < jsmith@host.tld>"
        ret = "John Smith <jsmith@host.tld >"
