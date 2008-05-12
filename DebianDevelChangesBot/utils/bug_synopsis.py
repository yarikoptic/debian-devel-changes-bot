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

import re

from btsutils.debbugs import soap as debbugs

from DebianDevelChangesBot.utils import tidy_bug_title
from DebianDevelChangesBot.messages import BugSynopsis

BUG_NUMBER_PATTERN = re.compile(r'\d{2,7}')

def bug_synopsis(bug_string):
    m = BUG_NUMBER_PATTERN.search(bug_string)
    try:
        bug_number = int(m.group(0))
    except:
        raise ValueError

    bts = debbugs()
    entry = bts.get(bug_number)

    msg = BugSynopsis()

    msg.bug_number = bug_number
    msg.status = entry.status
    msg.package = entry.package
    msg.severity = entry.severity

    msg.title = tidy_bug_title.tidy_bug_title(entry.summary, entry.package)

    return msg
