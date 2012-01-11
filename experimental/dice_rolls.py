#!/usr/bin/python
import random
import operator

# This script rolls a bunch of dice, and then records which ones have the
# highest values. This is run for multiple trials. Ties are broken
# randomly. This experiment seems to indicate that each die has an equal
# chance of being in the top 3 (or 4 or 5, etc).

DICE = 10
RANGE = 1000
HIGHEST = 5
TRIALS = 100000
r = random.SystemRandom()

class die(object):
    def __init__(self, id, range):
        self.value = 0
        self._range = range
        self.id = id
        self.count = 0

    def roll(self):
        r.randint(1, self._range)

    def __cmp__(self, other):
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        else:
            return -1 if r.randint(0,1) == 0 else 1

    def __repr__(self):
        return "(id: %d, count: %d)" % (self.id, self.count)

dice_list = [ die(id, RANGE) for id in range(DICE) ]
for trial in range(TRIALS):
    for die in range(DICE):
        dice_list[die].roll()
    dice_list.sort()
    for die in range(HIGHEST):
        dice_list[die].count += 1
    dice_list = sorted(dice_list, key=lambda die:die.id)

print sorted(dice_list, key=lambda die : die.id)
