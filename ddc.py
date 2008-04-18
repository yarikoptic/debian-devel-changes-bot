
print """
This is the first incarnation of the #debian-devel-changes bot. You
should not attempt to use it, or rely on this file's existence - it
will be removed once replacement code has been written.
"""

import sys
sys.exit(1)

# -*- coding: utf-8 -*-

# Copyright (C) 2008  Chris Lamb <chris@chris-lamb.co.uk>
#
# This file is part of uChoob.
#
# uChoob is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# uChoob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with uChoob.  If not, see <http://www.gnu.org/licenses/>.

from twisted.internet import threads

import os
import re
import email
import email.Header

import urllib2
import time
from BeautifulSoup import BeautifulSoup

import uchoob
import uchoob.logging
from uchoob.auth import Auth
from uchoob.colour import colourise

FIFO_DEVEL_CHANGES = '/var/run/debian-devel-changes'

class Ddc(object):
    command_name = "ddc"
    channels = ('#debian-devel-changes',)
    #channels = ('#lamby-test',)

    def __init__(self, irc):
        self.running = True
        self.irc = irc
        self.new_queue_entries = ([], None)
        self.rc_bugs = (-1, None)
        threads.deferToThread(self._devel_changes)
        self.messages = []

    def unload(self):
        self.running = False

    def _decode_str(self, val):
        try:
            return " ".join([x.decode('utf-8') for x, y in email.Header.decode_header(val)])
        except:
            return str(val)

    def _get_header(self, msg, header):
        val = msg[header]
        if val is None:
            return ''
        val = val.replace('\n', ' ')

        return self._decode_str(val)

    def _try_security(self, msg):
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

    def _devel_changes(self):
        while self.running:
            try:
                self.update_rc_bug_count()
            except:
                uchoob.logging.log_exception()

            f = file(FIFO_DEVEL_CHANGES, 'r')
            try:
                try:
                    msg = email.message_from_file(f)
                except:
                    continue
            finally:
                f.close()

            if not self.running:
                break

            try:
                flag = False
                for fn in (self._try_accepted, self._try_closed, self._try_submit, self._try_security):
                    ret = fn(msg)
                    if ret and self.irc:
                        if ret not in self.messages:
                            for channel in self.channels:
                                self.irc.get_from_channel(channel).say(ret)
                            self.messages.insert(0, ret)
                            self.messages = self.messages[:30]
                        flag = True
                        break
            except:
                uchoob.logging.log_exception()

            if not flag:
                print "=" * 80
                for key in ('To', 'From', 'X-Debian-PR-Message', 'X-Debian-PR-Source', 'Subject'):
                    print "%s: %s" % (key, self._get_header(msg, key))
                print
                try:
                    for line in self._get_body_text(msg).split("\n")[:25]:
                        print self._decode_str(line)
                except:
                    print "Could not print msg"
                print "-" * 80
                print "Could not match above message"
                print "=" * 80

    def _try_closed(self, msg):
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

    def _get_body_text(self, msg):
        p = msg.get_payload()
        while type(p) is list:
            p = msg.get_payload(0)

        while type(p) is not str:
            p = p.get_payload()

        return p

    def _tidy_data(self, data):
        for key in data.keys():
            data[key] = re.sub(r'\s+', ' ', data[key])
            data[key] = data[key].strip()
        return data

    def _format_email(self, email):
        email = re.sub(r'(?:<([-A-Za-z0-9]+)@debian.org>)', r'(\1)', email)
        email = re.sub(r'@(.{6}).*>', r'@\1..>', email)
        return email.replace(r'"', '')

    def _try_submit(self, msg):
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

    def _try_accepted(self, msg):
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

    @Auth(2)
    def cmd_rc_bugs(self, irc):
        try:
            self.update_rc_bug_count()
        except:
            uchoob.logging.log_exception()

    def update_rc_bug_count(self):
        cur_time = time.localtime()[:4] + ({True:1}.get(time.localtime()[4] > 30, 0),)

        if self.rc_bugs[0] == -1:
            print "Not updating on first load"
            self.rc_bugs = (-2, self.rc_bugs[1])
            return

        if cur_time == self.rc_bugs[1]:
            return

        if not self.irc.irc.connected:
            print "not updating yet"
            return

        print "Going to update RC bug count..."

        RC_BUGS_LOCATION = 'http://bts.turmzimmer.net/details.php?bydist=lenny'
        page = urllib2.urlopen(RC_BUGS_LOCATION)

        matcher = re.compile(r'.*Total shown: (?P<bugs>\d+) bug.*')

        for line in page:
            ret = matcher.match(line)
            if not ret:
                continue

            bugs = int(ret.groups('bugs')[0])
            self.rc_bugs = (self.rc_bugs[0], cur_time)

            print "Got bug count. Current count is %d, used to be %d" % (
                bugs, self.rc_bugs[0])

            if bugs == self.rc_bugs[0]:
                # Update time
                self.rc_bugs = (self.rc_bugs[0], cur_time)
                print "no change, so skipping"
                break

            # Update time and bug number
            self.rc_bugs = (bugs, cur_time)
            for channel in self.channels:
                self.irc.get_from_channel(channel).get_topic()

            self.rc_bugs = (bugs, cur_time)
            return

    def cb_topicUpdated(self, irc, current_topic):
        bugs = self.rc_bugs[0]

        if bugs < 0:
            print "Not initialised, so not updating topic"
            return

        HOOK = 'RC bug count: '
        new_topic = re.sub(HOOK + '(\d+)', HOOK + str(bugs), current_topic)

        if current_topic != new_topic:
            irc.set_topic(new_topic)

    def is_new(self, src_pkg):
        cur_time = time.localtime()[:4]

        if cur_time != self.new_queue_entries[1]:
            def get_entries():
                NEW_LOCATION = 'http://ftp-master.debian.org/new.html'
                page = urllib2.urlopen(NEW_LOCATION)
                for item in BeautifulSoup(page)('tr', {'class' : ('odd', 'even')}):
                    yield str(item.find('td').string)

            self.new_queue_entries = (set(get_entries()), cur_time)

        return src_pkg in self.new_queue_entries[0]
