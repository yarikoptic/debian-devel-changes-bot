
from DebianChangesBot import MailParser

class BugSubmitted(MailParser):

    def parse(self, msg):
        data = {
            'Package' : None,
            'Version' : '',
            'Severity' : '',
        }

        for idx, line in enumerate(self._get_body_text(msg).split("\n")):
            if line.lower().startswith('followup-for: ') and idx < 8:
                return False
            for key in data.keys():
                if not data[key] and idx < 8:
                    if line.lower().startswith("%s: " % key.lower()):
                        data[key] = self._decode_str(line.strip()[len(key) + 2:])
                    elif line.lower().startswith("%s " % key.lower()):
                        data[key] = self._decode_str(line.strip()[len(key) + 1:])

        m = re.match(r'^Bug#(\d+): (.*)$', self._get_header(msg, 'Subject'))
        if m:
            data['bug_number'] = m.group(1)
            data['title'] = m.group(2)
        else:
            return False

        if filter(lambda x: x is None, data.itervalues()):
            # We did not see all the required fields, return
            return False

        if ' ' in data['Package']:
            return False

        data = self._tidy_data(data)

        data['by'] = self._format_email(self._get_header(msg, 'From'))

        def reformat(key, match, new):
            if type(match) is tuple:
                if data[key].lower() in match:
                    data[key] = ''
                else:
                    data[key] = new % data[key]
            elif data[key].lower() == match.lower():
                data[key] = ''
            else:
                data[key] = new % data[key]

        if data['Version'].find('GnuPG') != -1:
            data['Version'] = ''

        reformat('Version', ('', 'n/a'), " ([yellow]%s[reset])")

        if data['Severity'].lower() in ('critical', 'grave', 'serious'):
            data['Severity'] = " ([red]%s[reset])" % data['Severity']
        else:
            reformat('Severity', ('normal', ''), " (%s)")

        if data['title'].lower().startswith("%s: " % data['Package'].lower()):
            data['title'] = data['title'][len(data['Package']) + 2:]

        for k, v in data.iteritems():
            try:
                data[k] = str(v.decode('ascii'))
            except: pass
        return colourise(_("Opened [b]#%(bug_number)s[/b]%(Severity)s in [green]%(Package)s[reset]%(Version)s by [cyan]%(by)s[reset] «%(title)s». http://bugs.debian.org/%(bug_number)s") % data)
