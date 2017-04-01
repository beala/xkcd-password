#!/usr/bin/python -O
 
from __future__ import print_function
import random
import math
import argparse
import os
import sys
from pkg_resources import resource_filename

PY2 = sys.version_info < (3,)
if PY2:
    range = xrange

# The dictionary bundled with the script. It must be in the same
# dir as the script.
DEFAULT_DICT =  resource_filename(__name__, 'dict.txt')
# Uncomment to use the system dictionary as the default.
#DEFAULT_DICT="/usr/share/dict/words"
WORDS = 4
BAD_CH_LIST = ['\'']
VERSION_NUMBER="0.1.4"

class WordValidator(object):
    """Validates words from the dictionary file, when the file is loaded
       into memory.
    """
    def __init__(self, flags):
        self._badChars = set(BAD_CH_LIST)
        self._maxLen = flags.l
        self._skipBad = flags.x

    def isValidWord(self, word):
        """Returns True if the word is valid. False otherwise.
        """
        if len(word) > self._maxLen or len(word) == 0:
            return False
        if self._skipBad and self._hasBadChar(word):
            return False
        return True

    def _hasBadChar(self, word):
        """Return true if word has a 'bad' char.
        """
        for char in reversed(word):
            if char in self._badChars:
                return True

class WordList(object):
    """List-like object that returns words from a dictionary file.
    """
    def __init__(self, flags):
        self._wordValidator = WordValidator(flags)
        self._loadDict(flags.d)

    def __getitem__(self, key):
        return self._dictList[key]

    def __len__(self):
        return len(self._dictList)

    def _loadDict(self, path):
        """Load every word from dict_file that passes the isValidWord test.
        """
        self._dictList = []
        with open(path) as dict_file:
            for line in dict_file:
                word = line.strip()
                if self._wordValidator.isValidWord(word):
                    self._dictList.append(word)

class RandomWord(object):
    """Iterator that returns on random word per iteration.
    """
    def __init__(self, flags):
        self._dictObj = WordList(flags)
        self._rng = random.SystemRandom()

    def __iter__(self):
        return self

    def __len__(self):
        return len(self._dictObj)

    def next(self):
        return self._rng.choice(self._dictObj)

    __next__ = next

class PasswordGen(object):
    """Iterator that returns one password per iteration.
    """
    def __init__(self, flags):
        self._randSource = RandomWord(flags)
        self._wordCount = flags.w
        self._delimiter = flags.s

    def __iter__(self):
        return self

    def next(self):
        rand_source_iter = iter(self._randSource)
        word_list = [rand_source_iter.next() for i in range(self._wordCount)]
        return self._delimiter.join(word_list)

    __next__ = next

    def getInfo(self):
        entropy, entr_per_word = self.calcEntropy()
        info =  "\nInfo:\n"
        info += "  Entropy: %0.3f bits\n" % entropy
        info += "  Entropy per word: %0.3f bits\n" % entr_per_word
        info += "  Possible combinations given settings: %s\n" % self.readableNum(self.calcPos())
        for triespersec in [1e3, 70e3, 75e6, 350e9]:
            info += self.makeYrsToCrackMsg(triespersec)
        return info

    def calcEntropy(self):
        entropy = math.log(self.calcPos(), 2)
        return entropy, entropy/self._wordCount

    def calcYrsToCrack(self, triesPerSec):
        try:
            return (self.calcPos()/(60*60*24*365.25*triesPerSec))/2
        except OverflowError:
            # If float calculation overflows, estimate using long.
            return (self.calcPos()/(60*60*24*365*int(triesPerSec)))/2

    def makeYrsToCrackMsg(self, triesPerSec):
        try:
            return "  Average time to crack at %s tries per second: %s years\n" % (self.readableNum(triesPerSec), self.readableNum(self.calcYrsToCrack(triesPerSec)))
        except TypeError:
            # If float conversion overflows, use long.
            return "  Average time to crack at %s tries per second: %s years\n" % (self.readableNum(triesPerSec), self.calcYrsToCrack(triesPerSec))

    def calcPos(self):
        return len(self._randSource) ** self._wordCount

    def readableNum(self, num, postfix=""):
        num_words = { 1000000000000: 'trillion ',
                      1000000000   : 'billion ',
                      1000000      : 'million ',
                      1000         : 'thousand ', }
        for div, word in num_words.items():
            if num/div >= 1:
                return self.readableNum(num/div, word + postfix)
        return "{:,.1f} {:s}".format(num, postfix).rstrip()


class Enumerator(object):
    """Accepts an iterator and prepends 1., 2., 3., etc to the beginning
       of each item returned from the generator.
    """
    def __init__(self, gen):
        self.gen = gen
        self.count = 0

    def __iter__(self):
        return self

    def next(self):
        self.count += 1
        return "%d. %s" % (self.count, self.gen.next())


def createParser():
    """Create the parser for the command line flagsi
    """
    # Default values for command line flags.
    flag_defaults = {
        'w': WORDS,
        'n':False,
        'd':DEFAULT_DICT,
        'x':True,
        'i':False,
        's':'-',
        'l':100,
        'c':1,
        'v':False,
        }
    parser = argparse.ArgumentParser(
            description='Generate an xkcd style password.',
            epilog='http://xkcd.com/936/')
    parser.add_argument('w',
            type=int,
            default=flag_defaults['w'],
            nargs='?',
            help="The number of words in the password. Defaults to 4.")
    parser.add_argument('-n',
            action='store_true',
            default=flag_defaults['n'],
            help="Disable printing a newline at the end of the password.\
                  Good for piping to the clipboard.")
    parser.add_argument('-d',
            default=flag_defaults['d'],
            metavar="DICT_PATH",
            help="The dictionary file. Defaults to %s." % DEFAULT_DICT)
    parser.add_argument('-x',
            action='store_false',
            default=flag_defaults['x'],
            help="Disable excluding special characters and punctuation.")
    parser.add_argument('-i',
            action='store_true',
            default=flag_defaults['i'],
            help="Enable showing password information (entropy, etc).")
    parser.add_argument('-s',
            default=flag_defaults['s'],
            metavar="SEPARATOR",
            help="Delimit words with a given character/string.")
    parser.add_argument('-l',
            default=flag_defaults['l'],
            type=int,
            metavar="LENGTH",
            help="The maximum word length. Words must be at or below this length.")
    parser.add_argument('-c',
            default=flag_defaults['c'],
            type=int,
            metavar="COUNT",
            help="Number of passwords to generate. Defaults to 1.")
    parser.add_argument('-v',
            action='store_true',
            default=flag_defaults['v'],
            help="Display version information.")
    return parser

def main():
    parser = createParser()
    flags = parser.parse_args()

    if flags.l < 1:
        sys.stderr.write("ERROR: Maxmimum word length is less than 1.\n")
        return
    if flags.c < 1:
        sys.stderr.write("ERROR: Password count is less than 1.\n")
        return

    if flags.v:
        print("Version: " + VERSION_NUMBER)
        return

    pGen = iter(PasswordGen(flags))
    # Print the password without adding a \n or space.
    password_count = int(flags.c)
    if password_count == 1:
        sys.stdout.write(pGen.next())
    elif password_count > 1:
        pGenEnumerate = iter(Enumerator(pGen))
        for i in range(password_count):
            sys.stdout.write(pGenEnumerate.next() + ("\n" if i != flags.c - 1 else ""))
    # Print newline if newline not disabled.
    if not flags.n:
        print("")

    # Make sure the password gets printed before info.
    sys.stdout.flush()
    if flags.i:
        sys.stderr.write(pGen.getInfo())

if __name__ == "__main__":
    main()
