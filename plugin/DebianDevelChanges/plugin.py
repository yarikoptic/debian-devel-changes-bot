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

from DebianDevelChangesBot.mailparsers import get_message
from DebianDevelChangesBot.utils import parse_mail, FifoReader, colourise

class DebianDevelChanges(supybot.callbacks.Plugin):
    def __init__(self, irc):
        self.__parent = super(DebianDevelChanges, self)
        self.__parent.__init__(irc)
        self.irc = irc

        fr = FifoReader()
        fifo_loc = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))), 'bin', 'debian-devel-changes.fifo')
        fr.start(self.cb_email, fifo_loc)

    def die(self):
        FifoReader().stop()

    def cb_email(self, fileobj):
        try:
            email = parse_mail(fileobj)
            msg = get_message(email)

            if msg:
                txt = colourise(msg.format().encode('utf-8'))
                for channel in self.irc.state.channels:
                    ircmsg = supybot.ircmsgs.privmsg(channel, txt)
                    self.irc.queueMsg(ircmsg)
        except:
           supybot.log.exception('Uncaught exception')

Class = DebianDevelChanges
