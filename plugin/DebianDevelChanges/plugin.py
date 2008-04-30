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

from supybot.commands import wrap
from supybot import ircdb, log, schedule

from DebianDevelChangesBot.mailparsers import get_message
from DebianDevelChangesBot.datasources import get_datasources
from DebianDevelChangesBot.utils import parse_mail, FifoReader, colourise

class DebianDevelChanges(supybot.callbacks.Plugin):
    threaded = True

    def __init__(self, irc):
        self.__parent = super(DebianDevelChanges, self)
        self.__parent.__init__(irc)
        self.irc = irc

        fr = FifoReader()
        fifo_loc = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))), 'bin', 'debian-devel-changes.fifo')
        fr.start(self._email_callback, fifo_loc)

        for callback, interval, name in get_datasources():
            try:
                schedule.removePeriodicEvent(name)
            except KeyError:
                pass
            schedule.addPeriodicEvent(callback, interval, name, now=False)
            schedule.addEvent(callback, interval, time.time() + 1)

    def die(self):
        FifoReader().stop()
        for callback, interval, name in get_datasources():
            schedule.removePeriodicEvent(name)

    def _email_callback(self, fileobj):
        try:
            email = parse_mail(fileobj)
            msg = get_message(email)

            if msg:
                txt = colourise(msg.format().encode('utf-8'))
                for channel in self.irc.state.channels:
                    ircmsg = supybot.ircmsgs.privmsg(channel, txt)
                    self.irc.queueMsg(ircmsg)
        except:
           log.exception('Uncaught exception')

    # Commands

    def rc(self, irc, msg, args):
        from DebianDevelChangesBot.datasources import TestingRCBugs

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
    update = wrap(update)

Class = DebianDevelChanges
