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
import supybot

from DebianDevelChangesBot.utils import parse_mail, FifoReader

class DebianDevelChanges(supybot.callbacks.Plugin):
    def __init__(self, irc):
        self.__parent = super(DebianDevelChanges, self)
        self.__parent.__init__(irc)
        self.irc = irc

        fr = FifoReader()
        fifo_loc = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))), 'bin', 'debian-devel-changes.fifo')
        fr.start(self.email_callback, fifo_loc)

    def email_callback(self, fileobj):
        text = repr(parse_mail(fileobj))[:300]
        for channel in self.irc.state.channels:
            self.irc.queueMsg(supybot.ircmsgs.privmsg(channel, text.encode('utf-8')))

    def die(self):
        FifoReader().stop()

Class = DebianDevelChanges
