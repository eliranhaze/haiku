# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from nltk.corpus import cmudict
#import nltk.cmudict # seems to contain more up to date dict
from nltk.tokenize import TweetTokenizer, sent_tokenize # TODO: doesn't properly handle "i.e." and "e.g." IF NOT FOLLOWED BY COMMA, so might want to make special rule ro replace such things

import re



# Resources:
# - NY Times' haiku algorithm: https://haiku.nytimes.com/about
# - Parsing tools and poetry algorithms: http://ryanheuser.org/tools and http://ryanheuser.org/sonnet-from-numbers

##
## TODO
##
## LOG: 
## - dec 11 i should write something that automatically finds and downloads texts and mines them
## - nov 24 also handle sentences that come after ':', e.g. in plato!
## - nov 24 added text processing; next: add more tests; smart haiku filtering
## - nov 21 handled missing and hyphen words; there's more to handle there; should do processing as well
## - nov 21 tested lewis 1, works well; should: add missing words and handle hyphen words
## - nov 20 intergrated unit tests; some fixes; should add more tests and integrate text processing
## - nov 12 fixed haiku_cut + parsing; should integrate into unit tests and text processing
## - oct 7 finished haiku_cut; should test and intergrate with text processing
##
## TODO
##

class Syllables(object):

    EXTRAS = {
        'actualized': 4,
        'analyse': 3,
        'ascription': 3,
        'ascriptions': 3,
        'behaviour': 3,
        'bivalence': 2,
        'causally': 3,
        'centerless': 3,
        'colour': 2,
        'conditionals': 4,
        'conjunct': 2,
        'conjuncts': 2,
        'connectedness': 4, # TODO: handle suffixes intelligently
        'connexion': 3,
        'contextualism': 6,
        'contextualist': 5,
        'credences': 3,
        'declarative': 4,
        'declaratives': 4,
        'demonstratives': 4,
        'denotation': 4,
        'dewdrop': 2,
        'dicto': 2,
        'disjunct': 2,
        'disjuncts': 2,
        'disjunctive': 3,
        'encodes': 2,
        'entailment': 3,
        'epistemic': 4,
        'epistemically': 5,
        'epistemological': 7,
        'evidential': 4,
        'extensional': 4,
        'extensionality': 6,
        'factive': 2,
        'factuals': 3,
        'favour': 2,
        'felicitous': 4,
        'fulfil': 2,
        'fulfilment': 3,
        'gavagai': 3,
        'grue': 1,
        'indeterminacy': 6,
        'indexical': 4,
        'indexicals': 4,
        'indexicality': 6,
        'inductive': 3,
        'intensional': 4,
        'intimating': 4,
        'iteration': 4,
        'kk': 2,
        'logics': 2,
        'meme': 1,
        'memes': 1,
        'metaphysically': 5,
        'neuron': 2,
        'nihilist': 3,
        'ponens': 2,
        'pragmatics': 3,
        'premiss': 2,
        'premisses': 3,
        'presupposed': 3,
        'presupposing': 4,
        'presuppositions': 5, # TODO: handle plurals intelligently
        'priori': 3,
        'propositional': 5,
        'qualia': 2,
        'quantifier': 4,
        'quantifiers': 4,
        'quus': 1,
        'recursive': 3,
        'reductio': 4,
        'reductionist': 4,
        'reductive': 3,
        'referent': 3,
        'referents': 3,
        'referential': 4,
        'sceptic': 2,
        'sceptical': 3,
        'sceptics': 2, # TODO: maybe there's a british english corpus as well? if so just combine the two
        'scepticism': 4,
        'semantical': 4,
        'semantically': 4,
        'signboard': 2,
        'simpliciter': 4,
        'solipsism': 4,
        'spacetime': 2,
        "sparrow's": 2,
        'subjectively': 4,
        'subsume': 2,
        'subsumes': 2,
        'synonymy': 4,
        'syntactic': 3,
        'theoretic': 3,
        'throbs': 1,
        'tollens': 2,
        'toothache': 2,
        'tractatus': 3,
        'trivially': 4,
        'unicorns': 3,
        'universals': 4,
        'vacuously': 4,
        'wherefore': 2,
        'whereof': 2,
        'whitecaps': 2,
        'wrongness': 2,
        u'ϕ': 1,
        u'ψ': 1,
        u'τ': 1,
    }

    NAMES = { # TODO: add handling for possessives
        'almog': 2,
        'argle': 2,
        'avicenna': 4,
        'bargle': 2,
        'bentham': 2,
        'carnap': 2,
        'chomsky': 2,
        'dummett': 2,
        'foucault': 2,
        'frege': 2,
        "frege's": 2,
        'fregean': 3,
        'geach': 1,
        'godel': 2,
        "godel's": 2,
        'gricean': 3,
        'heidegger': 3,
        'hesperus': 3,
        "hume's": 1,
        'humean': 3,
        'husserl': 2,
        "kant's": 1,
        'kripke': 2,
        "kripke's": 2,
        "leibniz's": 3,
        "locke's": 1,
        'nozick': 2,
        'ockham': 2,
        'parfit': 2,
        "quine's": 1,
        'russellian': 4,
        'soames': 1,
        'sorites': 4,
        'strawson': 2,
        'tarski': 2,
        'wittgenstein': 3,
        "wittgenstein's": 3,
    }

    PREFIXES = {
        'im': 1,
        'in': 1,
        'un': 1,
        'sub': 1,
        'non': 1,
        'dis': 1,
        'self': 1,
        'world': 1,
        'counter': 2,
        'under': 2,
        'over': 2,
        'anti': 2,
        'meta': 2,
        'contra': 2,
        'super': 2,
        'truth': 1,
    }

    def __init__(self):
        self._dict = dict()
        syl_dict = cmudict.dict()
        for word in syl_dict.iterkeys():
            num_syls = [len(list(y for y in x if y[-1].isdigit())) for x in syl_dict[word]][0]
            self._dict[word] = num_syls
        self._dict.update(self.EXTRAS)
        self._dict.update(self.NAMES)

    def nsyls(self, word):
        word = word.lower()
        n = self._dict.get(word)
        return n if n else self._calc_missing(word)

    def _calc_missing(self, word):
        if '-' in word:
            part_syls = [self.nsyls(part) for part in word.split('-')]
            if all(part_syls):
                return sum(part_syls)
        for pref, pref_syl in self.PREFIXES.iteritems():
            if word.startswith(pref):
                n = self.nsyls(word[len(pref):])
                if n:
                    return pref_syl + n

class NoSylError(ValueError):
    def __init__(self, message, word, *args):
        self.message = message
        self.word = word
        super(NoSylError, self).__init__(message, word, *args)

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
        self._haikus = None
        self._missing = {}
        super(HaikuParser, self).__init__(*arg, **kw)

    @property
    def haikus(self):
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
        syls = []
        for word in self.WORD_TK.tokenize(text):
            if word[0].isalpha():
                syl = self._nsyl_word(word)
                if not syl:
                    raise NoSylError('no syl for word', word)
                syls.append(syl)
        return syls

    def _nsyl_word(self, word):
        return self.SYLS.nsyls(word)

    def _haiku_cut(self, string):

        syls = [5, 7, 5]
        lines = [[] for _ in xrange(len(syls))] # each line is a list of words
        cur_syls = 0
        cur_line = 0

        for word in string.split():

            nsyls = sum(self._nsyl_word(w) for w in self._words(word) if w[0].isalpha())

            # advance line if needed - done here to swallow 0-syl words
            if nsyls and cur_syls == syls[cur_line]:
                if cur_line == len(lines):
                    # not a haiku (too long)
                    return
                cur_line += 1
                cur_syls = 0

            cur_syls += nsyls if nsyls else 0

            if cur_syls <= syls[cur_line]:
                # within haiku format; add word to current line
                lines[cur_line].append(word)
            else:
                # not a haiku (no pattern)
                return

        # check haiku is right size
        if all(lines) and cur_syls == syls[-1]: 
            # a haiku!
            return lines

    def _clean_text(self):
        self._text = self._text.replace(u"’", "'")
        self._text = self._text.replace(u"ﬁ", "fi")
        self._text = self._text.replace(u"ﬂ", "fl")

    def _parse_haikus(self):

        self._clean_text()

        haikus = []
        candidate = ''
        num_syls = 0
        #print 'parsing haiku: %s' % self._text
        for unit in self._text_units():
            candidate += ' ' + unit
            try:
                unit_syls = sum(n for n in self._nsyls(unit))
            except NoSylError as e:
                #print e
                self._missing[e.word] = self._missing.get(e.word, 0) + 1
                num_syls = 0
                candidate = ''
                continue
            num_syls += unit_syls
            #print 'unit = %s (syl count: %s)' % (unit, num_syls)
            if num_syls > 17 and unit_syls <= 17:
                num_syls = unit_syls
                candidate = unit
            if num_syls < 17:
                continue
            if num_syls == 17:
                haiku = self._haiku_cut(candidate)
                if haiku:
                    haikus.append(haiku)
            num_syls = 0
            candidate = ''

        return haikus

