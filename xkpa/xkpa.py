#!/usr/bin/python -O

import random
import math
import argparse
import os
import sys
from pkg_resources import resource_filename

# The dictionary bundled with the script. It must be in the same
# dir as the script.
DEFAULT_DICT =  resource_filename(__name__, 'dict.txt')
# Uncomment to use the system dictionary as the default.
#DEFAULT_DICT="/usr/share/dict/words"
WORDS = 4
BAD_CH_LIST = ['\'']
VERSION_NUMBER="0.1.2"

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

class Dictionary(object):
    def __init__(self, flags):
        self._dictLen = 0
        self._wordValidator = WordValidator(flags)
        self.dict_path = flags.d

    def _openDict(self):
        try:
            dict_file = open(self.dict_path)
        except IOError as e:
            error_msg =  "There was a problem opening the dictionary file '%s': " % self.dict_path
            error_msg += str(e.args[1]) + "\n"
            sys.stderr.write(error_msg)
            exit(1)
        return dict_file

class DictionaryList(Dictionary):
    """List-like object that returns words from a dictionary file.
    """
    def __init__(self, flags):
        super(DictionaryList, self).__init__(flags)
        self._loadDict(flags.d)

    def __getitem__(self, key):
        return self._dictList[key]

    def __len__(self):
        return self._dictLen

    def _loadDict(self, path):
        """Load every word from dict_file that passes the isValidWord test.
        """
        self._dictList = []
        dict_file = self._openDict()
        for line in dict_file:
            word = line.strip()
            if self._wordValidator.isValidWord(word):
                self._dictList.append(word)
        self._dictLen = len(self._dictList)
        dict_file.close()

class RandomDict(object):
    """Iterator that returns on random word per iteration.
    """
    def __init__(self, flags):
        self._dictObj = DictionaryList(flags)
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
    """Iterator that returns one password per iteration.
    """
    def __init__(self, flags):
        self._randSource = RandomDict(flags)
        self._wordCount = flags.w
        self._delimiter = flags.s

    def __iter__(self):
        return self

    def next(self):
        rand_source_iter = iter(self._randSource)
        word_list = [rand_source_iter.next() for i in range(self._wordCount)]
        return self._delimiter.join(word_list)

    def getInfo(self):
        entropy, entr_per_word = self.calcEntropy()
        yrs_to_crack_msg = "  At %s tries per second, it would take on average %0.3f years to crack.\n"
        info =  "\nInfo:\n"
        info += "  Entropy: %0.3f bits\n" % entropy
        info += "  Entropy per word: %0.3f bits\n" % entr_per_word
        info += self.makeYrsToCrackMsg("70 thousand", 70e3)
        info += self.makeYrsToCrackMsg("70 million", 70e6)
        info += self.makeYrsToCrackMsg("300 billion", 300e9)
        return info

    def calcEntropy(self):
        entropy = math.log(self.calcPos(), 2)
        return entropy, entropy/self._wordCount

    def calcYrsToCrack(self, triesPerSec):
        return (self.calcPos()/(60.*60*24*365.25*triesPerSec))/2.

    def makeYrsToCrackMsg(self, english, triesPerSec):
        return "  Average time to crack at %s tries per second: %0.6f years\n" % (english, self.calcYrsToCrack(triesPerSec))


    def calcPos(self):
        return len(self._randSource) ** self._wordCount


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

    if flags.v:
        print "Version: " + VERSION_NUMBER
        return

    pGen = iter(PasswordGen(flags))
    # Print the password without adding a \n or space.
    password_count = int(flags.c)
    if password_count == 1:
        sys.stdout.write(pGen.next())
    elif password_count > 1:
        pGenEnumerate = iter(Enumerator(pGen))
        for i in xrange(password_count):
            sys.stdout.write(pGenEnumerate.next() + ("\n" if i != flags.c - 1 else ""))
    else:
        sys.stderr.write("ERROR: Password count is less than 1.")
    # Print newline if newline not disabled.
    if not flags.n:
        print ""

    # Make sure the password gets printed before info.
    sys.stdout.flush()
    if flags.i:
        sys.stderr.write(pGen.getInfo())

if __name__ == "__main__":
    main()
