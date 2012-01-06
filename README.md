###Introduction###

This python script implements the [xkcd password spec](http://xkcd.com/936/).

###Usage###

```
% ./xkpa.py -h
usage: xkpa.py [-h] [-d D] [-x] [-i] [-s S] [-l L] [w]

Generate an xkcd style password.

positional arguments:
  w           The number of words in the password. Defaults to 4.

optional arguments:
  -h, --help  show this help message and exit
  -d D        The dictionary file. Defaults to /usr/share/dict/words.
  -x          Disable excluding special characters and punctuation.
  -i          Enable showing password information (entropy, etc).
  -s S        Delimit words with a given character/string.
  -l L        The maximum word length. Words must be at or below this length.

http://xkcd.com/936/
```

###Dictionary File###
The dictionary file bundled with the script is from the `wamerican-small` package off Ubuntu. I strikes a nice balance between entropy and not having too many esoteric words.
 
Modify the `DEFAULT_DICT` variable at the top of the script to use a different default.

###Randomness###
This script uses the `random.SystemRandom()` method. This should provide cryptographically secure randomness.
