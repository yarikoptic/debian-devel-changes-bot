
from DebianChangesBot import MailParser

class BugSubmitted(MailParser):

    def parse(self, msg):
        # Required fields are specified by None
        data = {
            'Source' : None,
            'Version' : None,
            'Distribution' : None,
            'Urgency' : None,
            'Changed-By' : None,
            'Closes' : '',
        }

        for line in self._get_body_text(msg).split("\n"):
            for key in data.keys():
                if not data[key] and line.startswith("%s: " % key):
                    data[key] = self._decode_str(line.strip()[len(key) + 2:])

        if filter(lambda x: x is None, data.itervalues()):
            # We did not see all the required fields, return
            return False

        # Reformat some fields
        if data['Closes']:
            data['Closes'] = ', '.join(["[b]#%s[/b]" % bug for bug in data['Closes'].split(' ')])
        data['Changed-By'] = self._format_email(data['Changed-By'])

        def reformat(key, match, new):
            if data[key].lower() == match.lower():
                data[key] = ''
            else:
                data[key] = new % data[key]

        data = self._tidy_data(data)

        if data['Distribution'].find('-backports') >= 0:
            data['Closes'] = ''

        reformat('Distribution', 'unstable', " to [blue]%s[reset]")
        reformat('Urgency', 'low', _(" with urgency [red]%s[reset]"))
        reformat('Closes', '', _(" (Closes: %s)"))

        data['NEW'] = ''
        if self.is_new(data['Source']):
            data['NEW'] = _(" [red](NEW)[reset]")

        for k, v in data.iteritems():
            try:
                data[k] = str(v.decode('ascii'))
            except: pass
        return colourise(_("[green]%(Source)s[reset]%(NEW)s ([yellow]%(Version)s[reset]) uploaded%(Distribution)s%(Urgency)s by [cyan]%(Changed-By)s[reset]%(Closes)s. http://packages.qa.debian.org/%(Source)s") % data)
