#!/usr/bin/python -O

import random

DICT_PATH = "/usr/share/dict/words"
WORDS = 4
RANGE = 5000

def trim(d):
    word_list = d.items()
    word_list.sort()
    word_count = 0
    entry = 0
    while word_count < WORDS and entry < len(word_list):
        word_count += len( word_list[entry][1] )
        entry += 1
    remove = len(word_list) - entry
    if remove > 0:
        for e in range(0, remove):
            word_list.pop()
    return dict(word_list)

def grab(d, words):
    word_list = d.items()
    word_list.sort()
    print word_list
    count = 0
    selected_words = []
    while count < words:
        if len( word_list[0][1] ) == 0:
            del word_list[0]
        selected = word_list[0][1][r.randint(0, len(word_list[0][1])-1)]
        word_list[0][1].remove(selected)
        count += 1
        selected_words.append(selected)
    return selected_words

r = random.SystemRandom()
dict_file = file(DICT_PATH)
word_dict = {}
for line in dict_file:
    word = line.strip()
    word_value = r.randint(0, RANGE)
    if word_value in word_dict:
        word_dict[word_value].append(word)
    else:
        word_dict[word_value] = [word]
    word_dict = trim(word_dict)

print grab(word_dict, WORDS)
