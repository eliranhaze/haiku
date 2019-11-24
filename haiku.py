# -*- coding: utf-8 -*-
""" give text, print haiku found """

import pyphen
import re
import sys

from nltk.corpus import cmudict

###
## TODO: handle "doesn't" #syls
###

print 'initializing...'
SYL_DICT = cmudict.dict()
WORD_PATTERN = re.compile('\w+')
WORDPUNCT_PATTERN = re.compile('\S+')
# TODO: I should check for common key errors (ie words in in the dict) and add them manually. eg 'spacetime' is not there but can be added simply as space+time
# (should keep a log/db of commonly missing words
# TODO: convert numbers to words
# TODO: find a way to skip page numbers / titles / etc in pdf texts

def get_words(sentence):
    return WORD_PATTERN.findall(sentence)

def get_words_with_punct(sentence):
    return WORDPUNCT_PATTERN.findall(sentence)

def normalize_punctuation(sentence):
    """ left-trim punctuation marks, to attach them to previous word """
    # TODO: what does this do exactly? when is it needed?
    return re.sub('\s+(\W+)', r'\1', sentence)

def strip_word(word):
    """ strip word of any non-word stuff """
    # the purpose of this is to remove punctuation and stuff (brackets, apostrophes, quotes, etc) so as to get
    # the word itself for evaluation. the problem is that this also removes apostrophes from possessives and contractions, which (maybe use TextBlob, for this and/or for sentences)
    # should remain. TODO: fix (maybe use TextBlob, for this and/or for sentences) (maybe use TextBlob, for this and/or for sentences)
    # --- Probably just keep apostrophes (with regex) but strip them from start/end of word
    words = get_words(word)
    if words:
        return words[0]

MISS = []
p = pyphen.Pyphen(lang='en')
def sylbackup(w):
    # this returns wrong results sometimes. either find a way to eliminate wrong results or do as suggested above: find common cmu errors
    MISS.append(w)
    return len(p.inserted(w).split('-'))

def nsyl(word):
    word = strip_word(word) # TODO: this is what causes loss of contractions!!!! they are in the dict!!! possessives too!
    if word:
      try:
          # TODO: this could be made a lot faster by building a simple dict in advance
        return [len(list(y for y in x if y[-1].isdigit())) for x in SYL_DICT[word.lower()]][0]
      except:
          raise
        #return sylbackup(word)
    return 0

def nsyl_sent(sent):
    return sum(nsyl(w) for w in get_words(sent))

def first_n_syls(words, n):
    cur_syls = 0
    result = []
    for w in words:
        result.append(w)
        cur_syls += nsyl(w)
        if cur_syls == n:
            return result
        if cur_syls > n:
            return

def first_n_syls2(words, n):
    cur_syls = 0
    result = []
    for w in words:
        result.append(w)
        cur_syls += nsyl(w)
        if cur_syls > n:
            break
    return cur_syls

def haiku_cut(sent):
    sent = normalize_punctuation(sent)
    words = get_words_with_punct(sent)
    line1 = first_n_syls(words, 5)
    if not line1:
        return
    line2 = first_n_syls(words[len(line1):], 7)
    if not line2:
        return
    line3 = first_n_syls(words[len(line1+line2):], 5)
    if not line3:
        return
    return line1, line2, line3

def extract_haikus(text):

    #print 'extracting haikus from text len=%d' % len(text)
    #sentences = text.split('.')
    sentences = split_into_sentences(text)
    #print 'found %d sentences' % len(sentences)


    # OLD bit
    #haiku_cands = []
    #for i, s in enumerate(sentences):
    #    try:
    #        words = get_words(s)
    #        ww = first_n_syls(words, 17)
    #        if ww and ww == words:
    #            haiku_cands.append(s)
    #    except: # TODO: proper handling?
    #        pass
    #    if (i+1) % 500 == 0:
    #        print 'processed: %d' % (i+1)

    haiku_cands = []
    prev = '' # for short sentences that may attach to next sentence to form a haiku # TODO: less hackey
    prev_n = 0
    keep_prev = False
    for i, s in enumerate(sentences):
        try:
            #print 'checking: %s' % s
            words = get_words(s)
            syls = first_n_syls2(words, 17)
            #print '%d syls' % syls
            if syls == 17:
                haiku_cands.append(s)
                #print 'added: %s' % s
                prev = ''
                prev_n = 0
            elif 0 < syls < 17:
                prev += ' ' + s 
                prev_n += syls
                keep_prev = True
                if prev_n == 17:
                    haiku_cands.append(prev)
                    #print 'added: %s' % prev
            if not keep_prev:
                    prev = ''
                    prev_n = 0
        except: # TODO: proper handling?
        #    prev = ''
         #   prev_n = 0
         #print 'error'
         pass
        if (i+1) % 500 == 0:
            print 'processed: %d' % (i+1)

    #print 'found %d candidates' % len(haiku_cands)
    haikus = []
    for cand in haiku_cands:
        cut = haiku_cut(cand)
        if cut:
            haikus.append(cut)

    #print 'found %d haikus' % len(haikus)
    return haikus

def format_haiku(haiku):
    lines = tuple(' '.join(h) for h in haiku)
    pad = '*' * 34
    formatted = '%s\n  %s\n%s' % lines
    return '%s\n%s' % (pad, formatted)

# the following from:
# https://stackoverflow.com/questions/4576077/python-split-text-on-sentences
# (also, missing handling decimals, more cases, etc; see comments there)
# BUT: better just use nltk.tokenize.sent_tokenize

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co|viz)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def main():
    input_file = sys.argv[1]
    text = open(input_file).read()
    haikus = extract_haikus(text)
    print 'haikus (%d):' % len(haikus)
    for h in haikus:
        print format_haiku(h)

if __name__ == '__main__':
    main()
