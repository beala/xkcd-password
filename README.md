##Introduction##

This python script implements the [xkcd password spec](http://xkcd.com/936/).

##Usage##

```
% ./xkpa.py -h
usage: xkpa.py [-h] [-n] [-d D] [-x] [-i] [-s S] [-l L] [-m] [w]

Generate an xkcd style password.

positional arguments:
  w           The number of words in the password. Defaults to 4.

optional arguments:
  -h, --help  show this help message and exit
  -n          Disable printing a newline at the end of the password. Good for
              piping to the clipboard.
  -d D        The dictionary file. Defaults to ./dict.
  -x          Disable excluding special characters and punctuation.
  -i          Enable showing password information (entropy, etc).
  -s S        Delimit words with a given character/string.
  -l L        The maximum word length. Words must be at or below this length.
  -m          Enable the low memory algorithm.

http://xkcd.com/936/
```

##Examples##
**Generate a password, and put it in the clipboard (OS X)**

	./xkpa.py -n | pbcopy

**Generate a password with info**

	./xkpa.py -i
	platter-presented-neighbor-vocational

	Info:
  		Entropy: 61.291656 bits
  		Entropy per word: 15.322914 bits

**Generate a password with 5 words separated by '.'**
 
	./xkpa.py -s '.' 5
	belies.annoyingly.birthing.ventilate.icon
	
**Generate a password with words no longer than 5 characters in length**

	./xkpa.py -l 5
	cover-kings-yard-store

**Generate a password on a low memory machine with 10 words, separated by nothing, and include words with special characters**

	./xkpa.py -mxs '' 10
	owedsuffersunhealthierlatitudecurd'sprotractormilestone'snutcrackerscertifypossession's

##Dictionary File##
The dictionary file bundled with the script is from the `wamerican-small` package off Ubuntu. I strikes a nice balance between entropy and not having too many esoteric words.
 
Modify the `DEFAULT_DICT` variable at the top of the script to use a different default.

##Randomness##
This script uses the `random.SystemRandom()` method. This should provide cryptographically secure randomness.

##Low Memory Algorithm##
[This](http://blog.usrsb.in/blog/2012/01/11/picking-random-items-from-a-file/) is the low memory algorithm.

	1. Read a word from the dictionary.
	2. Give it a random value.
	3. Insert the value-word pair (as a tuple) into the priority queue.
	4. If the queue has more than n items, pop an item.
	5. Repeat until every word has been read.
