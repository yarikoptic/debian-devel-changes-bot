# -*- coding: utf-8 -*-
#
#   Debian Changes Bot
#   Copyright (C) 2008 Chris Lamb <chris@chris-lamb.co.uk>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import time
import supybot
import threading

from supybot.commands import wrap
from supybot import ircdb, log, schedule

from btsutils.debbugs import BugExceptions

from DebianDevelChangesBot.mailparsers import get_message
from DebianDevelChangesBot.datasources import get_datasources, TestingRCBugs, \
    NewQueue
from DebianDevelChangesBot.utils import parse_mail, FifoReader, colourise, \
    rewrite_topic, madison, bug_synopsis

class DebianDevelChanges(supybot.callbacks.Plugin):
    threaded = True

    def __init__(self, irc):
        self.__parent = super(DebianDevelChanges, self)
        self.__parent.__init__(irc)
        self.irc = irc
        self.topic_lock = threading.Lock()

        fr = FifoReader()
        fifo_loc = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))), 'bin', 'debian-devel-changes.fifo')
        fr.start(self._email_callback, fifo_loc)

        self.queued_topics = {}

        # Schedule datasource updates
        for callback, interval, name in get_datasources():
            try:
                schedule.removePeriodicEvent(name)
            except KeyError:
                pass

            def wrapper(callback=callback):
                callback()
                self._topic_callback()

            schedule.addPeriodicEvent(wrapper, interval, name, now=False)
            schedule.addEvent(wrapper, time.time() + 1)

    def die(self):
        FifoReader().stop()
        for callback, interval, name in get_datasources():
            schedule.removePeriodicEvent(name)

    def _email_callback(self, fileobj):
        try:
            email = parse_mail(fileobj)
            msg = get_message(email)

            if msg:
                txt = colourise(msg.for_irc())
                for channel in self.irc.state.channels:
                    if self.registryValue('show_changes', channel):
                        ircmsg = supybot.ircmsgs.privmsg(channel, txt)
                        self.irc.queueMsg(ircmsg)

        except:
           log.exception('Uncaught exception')

    def _topic_callback(self):
        self.topic_lock.acquire()

        sections = {
            TestingRCBugs().get_num_bugs: 'RC bug count:',
            NewQueue().get_size: 'NEW queue:',
        }

        try:
            values = {}
            for callback, prefix in sections.iteritems():
                values[callback] = callback()

            for channel in self.irc.state.channels:
                new_topic = topic = self.irc.state.getTopic(channel)

                for callback, prefix in sections.iteritems():
                    if values[callback]:
                        new_topic = rewrite_topic(new_topic, prefix, values[callback])

                if topic != new_topic:
                    log.info("Queueing change of topic to '%s'" % new_topic)
                    self.queued_topics[channel] = new_topic

                    event_name = '%s_topic'
                    try:
                        schedule.removeEvent(event_name)
                    except KeyError:
                        pass
                    schedule.addEvent(lambda: self._update_topic(channel),
                        time.time() + 60, event_name)
        finally:
            self.topic_lock.release()

    def _update_topic(self, channel):
        self.topic_lock.acquire()
        try:
            new_topic = self.queued_topics[channel]
            log.info("Changing topic to '%s'" % new_topic)
            self.irc.queueMsg(supybot.ircmsgs.topic(channel, new_topic))
        finally:
            self.topic_lock.release()

    def rc(self, irc, msg, args):
        num_bugs = TestingRCBugs().get_num_bugs()
        if type(num_bugs) is int:
            irc.reply("There are %d release-critical bugs in the testing distribution. " \
                "See http://bts.turmzimmer.net/details.php?bydist=lenny" % num_bugs)
        else:
            irc.reply("No data at this time.")
    rc = wrap(rc)

    def update(self, irc, msg, args):
        if not ircdb.checkCapability(msg.prefix, 'owner'):
            irc.reply("You are not authorised to run this command.")
            return

        for callback, interval, name in get_datasources():
            callback()
            irc.reply("Updated %s." % name)
        self._topic_callback()
    update = wrap(update)

    def madison(self, irc, msg, args, package):
        lines = madison(package)
        if not lines:
            irc.reply('Did not get a response -- is "%s" a valid package?' % package)
            return

        field_styles = ('package', 'version', 'distribution', 'section')
        for line in lines:
            out = []
            fields = line.strip().split('|', len(field_styles))
            for style, data in zip(field_styles, fields):
                out.append('[%s]%s' % (style, data))
            irc.reply(colourise('[reset]|'.join(out)))
    madison = wrap(madison, ['text'])

    def bug(self, irc, msg, args, bug_string):
        try:
            msg = bug_synopsis(bug_string)
            if msg:
                irc.reply(colourise(msg.for_irc()))
        except BugExceptions.InvalidBugIdError, e:
            irc.reply(e)
        except ValueError:
            irc.reply('Could not parse bug number')

    bug = wrap(bug, ['text'])

Class = DebianDevelChanges
