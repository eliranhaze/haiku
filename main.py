# -*- coding: utf-8 -*-

from parser import HaikuParser

import io
import os
import sys

class HaikuProcessor(object):

    def __init__(self, files):
        self._files = files
        self._missing = {}

    def process(self):
        self._extract_haikus()
        self._print_missing()

    def _extract_haikus(self):
        for f in self._files:
            print '-' * 40
            print 'extracting haikus: %s' % f
            text = io.open(f, encoding='utf-8').read()
            hp = HaikuParser(text)
            haikus = hp.haikus
            print 'haikus (%d):' % len(haikus)
            for h in haikus:
                print self._format_haiku(h)
            print '-' * 40
            self._missing.update(hp._missing)

    def _print_missing(self):
        if self._missing:
            print 'missing words (%d):' % sum(self._missing.itervalues())
            print sorted(self._missing.items(), key = lambda x: -x[1])

    def _format_haiku(self, haiku):
        lines = tuple(' '.join(h) for h in haiku)
        pad = '*' * 34
        formatted = '%s\n  %s\n%s' % lines
        return '%s\n%s' % (pad, formatted)

def get_files(path):
    files = []
    if os.path.isdir(path):
        for f in os.listdir(path):
            filepath = os.path.join(path, f)
            if os.path.isfile(filepath):
                files.append(filepath)
    else:
        files.append(path)
    return files

def main():
    path = sys.argv[1]
    HaikuProcessor(get_files(path)).process()

if __name__ == '__main__':
    main()
