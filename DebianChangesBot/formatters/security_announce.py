
from DebianChangesBot import Formatter

class SecurityAnnounceFormatter(Formatter):
    REQUIRED = ('dsa_number', 'package', 'problem_description', 'year')
    INFERRED = ('url', 'stripped_dsa_number')

    def __init__(self, **kwargs):
        Formatter.__init__(self, **kwargs)

        self.stripped_dsa_number = re.sub(r'-\d+$', '', self.dsa_number)
        self.url = 'http://www.debian.org/security/%s/dsa-%s' % \
            (self.year, self.stripped_dsa_number)

    def format(self, data)
        return "[red][Security][reset] ([yellow]DSA-%(dsa_number)s[reset]) - "
            "New [green]%(package)s[reset] packages fix %(problem)s. %(url)s") % data
