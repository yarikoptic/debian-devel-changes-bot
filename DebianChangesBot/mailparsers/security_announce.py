
from DebianChangesBot import MailParser

class SecurityAnnounce(MailParser):

    def parse(self, msg):
        if self._get_header(msg, 'List-Id') != '<debian-security-announce.lists.debian.org>':
            return None

        fmt = SecurityAnnounceFormatter()

        m = re.match(r'^\[SECURITY\] \[DSA ([-\d]+)\] New (.*?) packages fix (.*)$', self._get_header(msg, 'Subject'))
        if m:
            fmt.dsa_number = m.group(1)
            fmt.package = m.group(2)
            fmt.problem = m.group(3)

        m = re.match(r'.*(20\d\d)', self._get_header(msg, 'Date'))
        if m:
            fmt.year = m.group(1)

        return fmt
