#!/usr/bin/python -O

import random
import heapq

DICT_PATH = "/usr/share/dict/words"
WORD_COUNT = 4

d_file = open(DICT_PATH)
wordq = []
for line in d_file:
    word = line.strip()
    rand_val = random.random()
    heapq.heappush(wordq, (rand_val, word) )
    if len(wordq) > WORD_COUNT:
        heapq.heappop(wordq)

print wordq

