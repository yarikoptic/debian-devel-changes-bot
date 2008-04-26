#!/usr/bin/env python

import os
import time
import select
import threading

FIFO = '/tmp/ddc'

class ReadThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)

        self.lock = threading.Lock()
        self.running = False
        self.quitfds = None

    def run(self):
        self.running = True
        self.quitfds = os.pipe()

        while self.running:
            fifo = os.open(FIFO, os.O_RDONLY | os.O_NONBLOCK)
            readfds, _, _ = select.select([fifo, self.quitfds[0]], [], [])

            if not self.running or self.quitfds[0] in readfds:
                os.close(fifo)
                os.close(self.quitfds[0])
                os.close(self.quitfds[1])
                break

            fileobj = os.fdopen(fifo)
            print fileobj.readlines()
            fileobj.close()

    def stop(self):
        self.lock.acquire()
        try:
            if self.running:
                self.running = False
                os.write(self.quitfds[1], '1')
        finally:
            self.lock.release()

t = ReadThread()
t.start()
try:
    time.sleep(30)
finally:
    t.stop()
