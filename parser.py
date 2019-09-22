# -*- coding: utf-8 -*-

from nltk.corpus import cmudict
from nltk.tokenize import sent_tokenize # TODO: doesn't properly handle "i.e." and "e.g." IF NOT FOLLOWED BY COMMA, so might want to make special rule ro replace such things

import re



# Resources:
# - NY Times' haiku algorithm: https://haiku.nytimes.com/about

class TextParser(object):

    def __init__(self, text):
        self._text = text
        self._sentences = None

    @property
    def sentences(self):
        if self._sentences is None:
            self.sentences = sent_tokenize(self._text)
        return self._sentences

class HaikuParser(TextParser):

    # TODO: find haikus not only in complete sentences; just have to be something that could be a complete sentence.
    # e.g. a sentence could be "P and Q", but i can use P or Q alone
    # but for that i need to find 'semantic' sentences... which is going to be really hard.
    # ALTERNATIVELY, i can just find any haiku regardless of sentence structure, and see what comes up.

    # can also chop by comma (that's what Times does) and by 'and' or 'or'.

    def __init__(self, *arg, **kw):
        super(HaikuParser, self).__init__(*arg, **kw)

    @property
    def parse_haikus(self):
        if self._haikus is None:
            self._haikus = self._parse_haikus()
        return self._haikus

    def _text_units(self):
        # TODO: break down even more: commas, "and"s, etc.
        for sent in self.sentences:
            yield sent

    def _nsyl(self, text):
        pass

    def _nsyl_word(self, word):
        pass

    def _haiku_cut(self, string):
        pass

    def _parse_haikus(self):
        haikus = []
        candidate = ''
        for unit in self._text_units():
            candidate += unit
            num_syls = self._nsyl(candidate)
            if num_syls < 17:
                continue
            if num_syls == 17:
                haiku = self._haiku_cut(candidate)
                if haiku: haikus.append(candidate)
            candidate = ''

