
from DebianChangesBot import MailParser

class SecurityAnnounce(MailParser):

    def parse(self, msg):
        if self._get_header(msg, 'List-Id') != '<debian-security-announce.lists.debian.org>':
            return False

        data = {
            'dsa_number' : None,
            'package' : None,
            'problem' : None,
            'year' : None,
            'url' : None,
        }

        m = re.match(r'^\[SECURITY\] \[DSA ([-\d]+)\] New (.*?) packages fix (.*)$', self._get_header(msg, 'Subject'))
        if m:
            data['dsa_number'] = m.group(1)
            data['package'] = m.group(2)
            data['problem'] = m.group(3)
        else:
            return False

        m = re.match(r'.*(20\d\d)', self._get_header(msg, 'Date'))
        if m:
            data['year'] = m.group(1)
        else:
            return False

        data['url'] = "http://www.debian.org/security/%s/dsa-%s" % (data['year'], re.sub(r'-\d+$', '', data['dsa_number']))
        data = self._tidy_data(data)

        for k, v in data.iteritems(): data[k] = str(v.decode('ascii'))
        return colourise(_("[red][Security][reset] ([yellow]DSA-%(dsa_number)s[reset]) - New [green]%(package)s[reset] packages fix %(problem)s. %(url)s") % data)
