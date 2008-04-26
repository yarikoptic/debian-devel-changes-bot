# -*- coding: utf-8 -*-

def tidy_bug_title(title, package):
    """
    Strips various package name prefixes from a bug title.

    For example:

      "emacs: Not as good as vim"  =>  "Not as good as vim"
      "[emacs] Not as good as vim"  =>  "Not as good as vim"

    """

    for prefix in ('%s: ', '[%s]: ', '[%s] '):
        if title.lower().startswith(prefix % package.lower()):
            title = title[len(package) + len(prefix) - 2:]

    return title
