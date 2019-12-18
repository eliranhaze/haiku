# -*- coding: utf-8 -*-

from parser import HaikuParser
from brains import predict, data

import io
import os
import sys

class HaikuProcessor(object):

    TEXT_CUTOFF_SCORE = 0.59

    def __init__(self, files):
        self._files = files
        self._missing = {}
        self._skipped = 0
        self._predictor = predict.Prediction(source=data.IS_TEXT)

    def process(self):
        self._extract_haikus()
        self._print_missing()
        print 'skipped: %d haikus' % self._skipped

    def _extract_haikus(self):
        for f in self._files:
            text = io.open(f, encoding='utf-8').read()
            hp = HaikuParser(text)
            haikus = filter(self._should_keep, hp.haikus)
            if haikus:
                self._print_haikus(f, haikus)
            self._missing.update(hp._missing)

    def _get_score(self, haiku_text):
        return self._predictor.predict(haiku_text)[1]

    def _print_haikus(self, title, haikus):
        print '%s haikus (%d):' % (title, len(haikus))
        for h in haikus:
            text = ' '.join([' '.join(line) for line in h])
            score = self._get_score(text)
            if score < self.TEXT_CUTOFF_SCORE: # TODO: move to should_skip
                self._skipped += 1
                continue
            print '%s [%.2f]' % (self._format_haiku(h), score)
            text = ' '.join([' '.join(line) for line in h])
        print '-' * 40

    def _print_missing(self):
        limit = 25
        if self._missing:
            print 'missing words (%d):' % sum(self._missing.itervalues())
            if len(self._missing) > limit:
                print '(top %d)' % limit
            sorted_missing = sorted(self._missing.items(), key = lambda x: -x[1])[:limit]
            for word, count in sorted_missing:
                print '%s %d' % (word, count)

    def _format_haiku(self, haiku):
        lines = tuple(' '.join(h) for h in haiku)
        pad = '*' * 34
        formatted = '%s\n  %s\n%s' % lines
        return '%s\n%s' % (pad, formatted)
        #return '\t"%s %s %s",' % lines

    def _should_keep(self, haiku):
        return not self._should_skip(haiku)

    def _should_skip(self, haiku):
        skip_words = [
            'Routledge',
            'Clarendon',
            'Oxford:',
            'Blackwell',
        ]
        digits = 0
        for h in haiku:
            for s in skip_words:
                if s in h:
                    self._skipped += 1
                    return True
            for word in h:
                for char in word:
                    if char.isdigit():
                        digits += 1
                if digits > 5:
                    self._skipped += 1
                    return True
        return False

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
