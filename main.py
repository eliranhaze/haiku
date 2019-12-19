# -*- coding: utf-8 -*-

from parser import HaikuParser
from brains import predict, data

import io
import os
import sys

class HaikuProcessor(object):

    HAIKU_PRINT_FORMAT = True # print 3 haiku lines; otherwise print 1 line

    TEXT_SCORE_CUTOFF = 0.59 # haikus below this score are filtered
    DIGIT_CUTOFF = 5 # haikus with more digits are filtered

    SKIP_WORDS = [ # haikus with these words are filtered
        'Routledge',
        'Clarendon',
        'Oxford:',
        'Blackwell',
    ]

    def __init__(self, files):
        self._files = files
        self._missing = {}
        self._skipped = 0
        self._found = 0
        self._predictor = predict.Prediction(source=data.IS_TEXT)

    def process(self):
        self._extract_haikus()
        self._print_missing()
        print 'found: %d haikus' % self._found
        print 'skipped: %d haikus' % self._skipped

    def _extract_haikus(self):
        for f in self._files:
            text = io.open(f, encoding='utf-8').read()
            hp = HaikuParser(text)
            haikus = self._filter_haikus(hp.haikus)
            if haikus:
                self._print_haikus(f, haikus)
                self._found += len(haikus)
            self._missing.update(hp._missing)

    def _filter_haikus(self, haikus):
        """ note: returns a list of pairs of haikus with scores """
        filtered = []
        for h in haikus:
            skip, score = self._should_skip(h)
            if not skip:
                filtered.append((h, score))
        return filtered

    def _get_score(self, haiku_text):
        return self._predictor.predict(haiku_text)[1]

    def _print_haikus(self, title, haikus):
        print '%s haikus (%d):' % (title, len(haikus))
        for h, score in haikus:
            print '%s [%.2f]' % (self._format_haiku(h), score)
        print '-' * 40

    def _format_haiku(self, haiku):
        if self.HAIKU_PRINT_FORMAT:
            lines = tuple(' '.join(h) for h in haiku)
            pad = '*' * 34
            formatted = '%s\n  %s\n%s' % lines
            return '%s\n%s' % (pad, formatted)
        return '\t"%s %s %s",' % lines

    def _print_missing(self):
        limit = 25
        if self._missing:
            print 'missing words (%d):' % sum(self._missing.itervalues())
            if len(self._missing) > limit:
                print '(top %d)' % limit
            sorted_missing = sorted(self._missing.items(), key = lambda x: -x[1])[:limit]
            for word, count in sorted_missing:
                print '%s %d' % (word, count)

    def _should_skip(self, haiku):
        text = ' '.join([' '.join(line) for line in haiku])
        if any(w in text for w in self.SKIP_WORDS) or sum(1 for c in text if c.isdigit()) > self.DIGIT_CUTOFF:
            score = 0 # skip score calc
        else:
            score = self._get_score(text)
        if score < self.TEXT_SCORE_CUTOFF:
            return True, score
        return False, score

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
