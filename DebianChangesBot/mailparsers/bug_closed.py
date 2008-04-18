
from DebianChangesBot import MailParser

class BugClosed(MailParser):

    def parse(self, msg):
        data = {
            'bug_number' : None,
            'title' : None,
            'package' : None,
            'by' : '',
        }

        m = re.match(r'^Bug#(\d+): marked as done \((.+)\)$', self._get_header(msg, 'Subject'))
        if m:
            data['bug_number'] = m.group(1)
            data['title'] = m.group(2)
        else:
            return False

        for header, key in (('X-Debian-PR-Package', 'package'), ('X-Debian-PR-Source', 'package'), ('To', 'by')):
            try:
                if len(msg[header]) > 0:
                    data[key] = self._get_header(msg, header)
            except TypeError:
                pass

        if filter(lambda x: x is None, data.itervalues()):
            print data
            return False

        if data['title'].startswith("%s: " % (data['package'])):
            data['title'] = data['title'][len(data['package']) + 2:]

        # Bug was closed via 123456-done@bugs.debian.org, so To: is wrong.
        if 'bugs.debian.org' in data['by']:
            data['by'] = self._get_header(msg, 'From')

        data['by'] = self._format_email(data['by'])
        data = self._tidy_data(data)

        for k, v in data.iteritems():
            try:
                data[k] = str(v.decode('ascii'))
            except: pass
        return colourise(_("Closed [b]#%(bug_number)s[/b] in [green]%(package)s[reset] by [cyan]%(by)s[reset] «%(title)s». http://bugs.debian.org/%(bug_number)s") % data)
