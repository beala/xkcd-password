#!/usr/bin/python

import random
import math
import argparse
import os
import sys

# The dictionary bundled with the script. It must be in the same
# dir as the script.
DEFAULT_DICT= os.path.dirname(sys.argv[0]) + "/dict"
# Uncomment to use the system dictionary as the default.
#DEFAULT_DICT="/usr/share/dict/words"
WORDS = 4
BAD_CH_LIST = ['\'']

class Dictionary(object):
    def __init__(self, flags):
        self._dictLen = 0
        self._skipBad = flags.x
        self._maxLen = flags.l
        self._badChars = BAD_CH_LIST
        self._loadDict(flags.d)

    def __len__(self):
        return self._dictLen

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

class DictionarySplitline(Dictionary):
    def __init__(self, flags):
        super(DictionarySplitline, self).__init__(flags)

    def __getitem__(self, key):
        return self._dictList[key]

    def _loadDict(self, path):
        self._dictList = []
        dict_file = file(path)
        # Load the dictionary into memory.
        self._dictList = dict_file.read().splitlines()
        # Convert the dictList to a dictionary for quick searching
        dict_dict = dict(enumerate(self._dictList))
        for key, word in dict_dict.items():
            # Remove invalid words
            if not self._validateWord(word):
                del dict_dict[key]
        # Copy the words back into the dictList
        self._dictList = dict_dict.values()
        self._dictLen = len(self._dictList)

class DictionaryList(Dictionary):
    def __init__(self, flags):
        super(DictionaryList, self).__init__(flags)

    def __getitem__(self, key):
        return self._dictList[key]

    def _loadDict(self, path):
        self._dictList = []
        dict_file = file(path)
        for line in dict_file:
            word = line.strip()
            if self._validateWord(word):
                self._dictList.append(word)
        self._dictLen = len(self._dictList)

class RandomDict(object):
    def __init__(self, flags):
        #self._dictObj = DictionaryList(flags)
        self._dictObj = DictionarySplitline(flags)
        self._rng = random.SystemRandom()

    def __iter__(self):
        return self

    def __len__(self):
        return len(self._dictObj)

    def next(self):
        return self._dictObj[self._rng.randint(0, len(self) - 1)]

    def __getattr__(self, attr):
        return getattr(self._dictObj, attr)

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
            default=DEFAULT_DICT,
            help="The dictionary file. Defaults to %s." % DEFAULT_DICT)
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
    if flags.i:
        print pGen.getInfo()
