#!/usr/bin/python

import random
import math
import argparse

DEFAULT_DICT="/usr/share/dict/words"
WORDS = 4
BAD_CH_LIST = ['\'']

class DictionaryList(object):
    def __init__(self, flags):
        self._dictList = []
        self._dictLen = 0
        self._skipBad = flags.x
        self._maxLen = flags.l
        self._badChars = BAD_CH_LIST
        self._loadDict(DEFAULT_DICT)

    def getWord(self, num):
        return self._dictList[num]

    def __len__(self):
        return self._dictLen

    def _loadDict(self, path):
        self._dictList = []
        dict_file = file(path)
        for line in dict_file:
            word = line.strip()
            if self._validateWord(word):
                self._dictList.append(word)
        self._dictLen = len(self._dictList)

    def _validateWord(self, word):
        if len(word) > self._maxLen or len(word) == 0:
            return False
        if self._skipBad and self._hasBadChar(word):
            return False
        return True

    def _hasBadChar(self, word):
        for char in word:
            if char in self._badChars:
                return True

class RandomDict(DictionaryList):
    def __init__(self, flags):
        super(RandomDict, self).__init__(flags)
        self._rng = random.SystemRandom()

    def __iter__(self):
        return self

    def next(self):
        return self.getWord(self._rng.randint(0, self._dictLen-1))

class PasswordGen(object):
    def __init__(self, flags):
        self._randSource = RandomDict(flags)
        self._wordCount = flags.w
        self._delimiter = flags.s

    def __iter__(self):
        return self

    def next(self):
        word_list = [self._randSource.next() for i in range(self._wordCount)]
        return self._delimiter.join(word_list)

    def getInfo(self):
        entropy = math.log(len(self._randSource) ** self._wordCount, 2)
        info =  "\nInfo:\n"
        info += "  Entropy: %d\n" % entropy
        info += "  Entropy per word: %d" % (entropy / self._wordCount)
        return info

def createParser():
    parser = argparse.ArgumentParser(
            description='Generate an xkcd style password.',
            epilog='http://xkcd.com/936/')
    parser.add_argument('w',
            type=int,
            default=WORDS,
            nargs='?',
            help="The number of words in the password. Defaults to 4.")
    parser.add_argument('-d',
            type=open,
            default=DEFAULT_DICT,
            help="The dictionary file. Defaults to /usr/share/dict/words.")
    parser.add_argument('-x',
            action='store_false',
            default=True,
            help="Disable excluding special characters and punctuation.")
    parser.add_argument('-i',
            action='store_true',
            default=False,
            help="Enable showing password information (entropy, etc).")
    parser.add_argument('-s',
            default='-',
            help="Delimit words with a given character/string.")
    parser.add_argument('-l',
            default=100,
            type=int,
            help="The maximum word length. Words must be at or below this length.")
    return parser

if __name__ == "__main__":
    parser = createParser()
    flags = parser.parse_args()
    pGen = PasswordGen(flags)
    print pGen.next()
    print pGen.getInfo()
    exit()

    # Parse arguments
    parser = createParser()
    args = vars( parser.parse_args() )
    word_count = args['w']
    dict_file = args['d']
    exclude_chars = args['x']
    info = args['i']
    delimit = args['s']
    max_word_len = args['l']

