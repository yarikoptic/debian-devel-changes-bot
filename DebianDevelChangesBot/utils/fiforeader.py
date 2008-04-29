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
import fcntl
import select
import threading
import traceback

class FifoReader(object):
    __shared_state = {}

    read_lock = threading.Lock()
    stop_lock = threading.Lock()
    running = False
    quitfds = None

    def __init__(self):
        self.__dict__ = self.__shared_state

    def start(self, callback, fifo_loc):
        self.callback = callback
        self.fifo_loc = fifo_loc
        threading.Thread(target=self.run).start()

    def run(self):
        self.read_lock.acquire()
        try:
            for fileobj in self.gen_messages():
                try:
                    self.callback(fileobj)
                except Exception, exc:
                    print "Uncaught exception caught inside fiforeader"
                    traceback.print_exc()
                finally:
                    fileobj.close()
        finally:
            self.read_lock.release()

    def gen_messages(self):
        self.running = True
        self.quitfds = os.pipe()

        while self.running:
            fifo = os.open(self.fifo_loc, os.O_RDONLY | os.O_NONBLOCK)
            flags = fcntl.fcntl(fifo, fcntl.F_GETFL)
            fcntl.fcntl(fifo, fcntl.F_SETFD, flags & ~os.O_NONBLOCK)

            readfds, _, _ = select.select([fifo, self.quitfds[0]], [], [])

            # If our anonymous descriptor was written to, exit loop
            if not self.running or self.quitfds[0] in readfds:
                os.close(fifo)
                os.close(self.quitfds[0])
                os.close(self.quitfds[1])
                break

            if fifo not in readfds:
                continue

            yield os.fdopen(fifo)

    def stop(self):
        self.stop_lock.acquire()
        try:
            if self.running:
                self.running = False
                os.write(self.quitfds[1], '1')

                # Block until we have actually stopped
                self.read_lock.acquire()
                self.read_lock.release()
        finally:
            self.stop_lock.release()
