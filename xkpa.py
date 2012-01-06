#!/usr/bin/python

import random
import re
import math
import argparse

DEFAULT_DICT="/usr/share/dict/words"
WORDS = 4
BAD_CH_LIST = ['\'']

BAD_CHARS= "|".join(BAD_CH_LIST)

def createParser():
    parser = argparse.ArgumentParser(
            description='Generate an xkcd style password.',
            epilog='http://xkcd.com/936/')
    parser.add_argument('w',
            type=int,
            default=WORDS,
            nargs='?',
            help="The number of words to generate.")
    parser.add_argument('-d',
            type=open,
            default=DEFAULT_DICT,
            help="The dictionary file.")
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
            help="Delimit words with a given character.")
    parser.add_argument('-l',
            default=100,
            type=int,
            help="The maximum word length. Words must be at or below this length.")
    return parser

def loadDict(dict_file, exclude_char, max_word_len):
    dict_list = []
    for line in dict_file:
        word = line.strip()
        if validateWord(word, max_word_len, exclude_char):
            dict_list.append(word)
    return dict_list

def validateWord(word, max_word_len, exclude_char):
    return (len(word) <= max_word_len) and not (exclude_char and re.search(BAD_CHARS, word))

def makePassword(dict_list, word_count, delimit):
    dict_len = len(dict_list)
    r = random.SystemRandom()
    pass_list = []
    for i in range(word_count):
        pass_list.append( dict_list[r.randint(0,dict_len-1)] )
    return delimit.join(pass_list)

def getPassInfo(dict_len, word_count):
    entropy = math.log(dict_len ** word_count, 2)
    return "\nInfo:\n  Entropy: %d\n  Entropy per word: %d" % (entropy, (entropy/word_count))

if __name__ == "__main__":
    # Parse arguments
    parser = createParser()
    args = vars( parser.parse_args() )
    word_count = args['w']
    dict_file = args['d']
    exclude_chars = args['x']
    info = args['i']
    delimit = args['s']
    max_word_len = args['l']

    #Read in dictionary
    dict_list = loadDict(dict_file, exclude_chars, max_word_len)

    # Select random words and create password
    print makePassword(dict_list, word_count, delimit)

    if info:
        print getPassInfo(len(dict_list), word_count)
