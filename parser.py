# -*- coding: utf-8 -*-

from nltk.corpus import cmudict
#import nltk.cmudict # seems to contain more up to date dict
from nltk.tokenize import TweetTokenizer, sent_tokenize # TODO: doesn't properly handle "i.e." and "e.g." IF NOT FOLLOWED BY COMMA, so might want to make special rule ro replace such things

import re



# Resources:
# - NY Times' haiku algorithm: https://haiku.nytimes.com/about

##
## TODO
##
## LAST: (oct 7)
## - finished haiku_cut; should test and intergrate with text processing
##
## TODO
##

class Syllables(object):

    EXTRAS = {
        'spacetime': 2,
    }

    def __init__(self):
        self._dict = dict()
        syl_dict = cmudict.dict()
        for word in syl_dict.iterkeys():
            num_syls = [len(list(y for y in x if y[-1].isdigit())) for x in syl_dict[word]][0]
            self._dict[word] = num_syls
        self._dict.update(self.EXTRAS)

    def nsyls(self, word):
        return self._dict.get(word.lower())

class TextParser(object):

    def __init__(self, text):
        self._text = text
        self._sentences = None

    @property
    def sentences(self):
        if self._sentences is None:
            self._sentences = sent_tokenize(self._text)
        return self._sentences

class HaikuParser(TextParser):

    # TODO: find haikus not only in complete sentences; just have to be something that could be a complete sentence.
    # e.g. a sentence could be "P and Q", but i can use P or Q alone
    # but for that i need to find 'semantic' sentences... which is going to be really hard.
    # ALTERNATIVELY, i can just find any haiku regardless of sentence structure, and see what comes up.

    # can also chop by comma (that's what Times does) and by 'and' or 'or'.

    SYLS = Syllables()
    WORD_TK = TweetTokenizer()

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

    def _words(self, string):
        return self.WORD_TK.tokenize(string)

    def _nsyls(self, text):
        return [self._nsyl_word(word) for word in self.WORD_TK.tokenize(text)]

    def _nsyl_word(self, word):
        return self.SYLS.nsyls(word)

    def _haiku_cut(self, string):

        syls = [5, 7, 5]
        lines = ['' for _ in xrange(len(syls))]
        cur_syls = 0
        cur_line = 0

        for word in self._words(string):

            nsyls = self._nsyl_word(word)

            # advance line if needed - done here to swallow 0-syl words
            if nsyls and cur_syls == syls[cur_line]:
                if cur_line == len(lines):
                    # not a haiku (too long)
                    return
                cur_line += 1
                cur_syls = 0

            cur_syls += nsyls if nsyls else 0

            if cur_syls <= syls[cur_line]:
                lines[cur_line] = self._attach(lines[cur_line], word)
            else:
                # not a haiku (no pattern)
                return

        # check haiku is right size
        if all(lines) and cur_syls == syls[-1]: 
            # a haiku!
            return lines

    def _attach(self, string, word):
        if not string:
            return word
        if word[0].isalpha() or word[0].isdigit():
            return string + ' ' + word
        else:
            return string + word

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

