##Introduction##

This python script implements the [xkcd password spec](http://xkcd.com/936/).

##Install##

This package requires the `pip` Python package manager for installation. [pip installation instructions](http://www.pip-installer.org/en/latest/installing.html).

Then:

```
pip install xkpa
```

##Usage##

```
% xkpa -h
usage: xkpa.py [-h] [-n] [-d DICT_PATH] [-x] [-i] [-s SEPARATOR] [-l LENGTH]
               [-c COUNT] [-m]
               [w]

Generate an xkcd style password.

positional arguments:
  w             The number of words in the password. Defaults to 4.

optional arguments:
  -h, --help    show this help message and exit
  -n            Disable printing a newline at the end of the password. Good
                for piping to the clipboard.
  -d DICT_PATH  The dictionary file. Defaults to [PATH_TO_BUNDLED_DICT].
  -x            Disable excluding special characters and punctuation.
  -i            Enable showing password information (entropy, etc).
  -s SEPARATOR  Delimit words with a given character/string.
  -l LENGTH     The maximum word length. Words must be at or below this
                length.
  -c COUNT      Number of passwords to generate. Defaults to 1.
  -m            Enable the low memory algorithm.

http://xkcd.com/936/
```

##Examples##
**Generate a password, and put it in the clipboard (OS X)**

    xkpa -n | pbcopy

**Generate a password, copy to clipboard, and print info**

    xkpa -ni | pbcopy

    Info:
        Entropy: 61.292 bits
        Entropy per word: 15.323 bits
        At 1 million tries per second, it would take at most 89499.437 years to crack.

The password will get copied to the clipboard, but the info message will not (the info message is printed to stderr).

**Generate a password with info**

    xkpa -i
    pomegranate-outs-scapegoated-decomposed

    Info:
        Entropy: 61.292 bits
        Entropy per word: 15.323 bits
        At 1 million tries per second, it would take at most 89499.437 years to crack.

**Generate a password with 5 words separated by '.'**

    xkpa -s '.' 5
    belies.annoyingly.birthing.ventilate.icon

**Generate a password with words no longer than 5 characters in length**

    xkpa -l 5
    cover-kings-yard-store

**Generate a password on a low memory machine with 10 words, separated by nothing, and include words with special characters**

    xkpa -mxs '' 10
    owedsuffersunhealthierlatitudecurd'sprotractormilestone'snutcrackerscertifypossession's

**Generate multiple passwords**

    xkpa -c 5
    1. excite-incriminating-wronged-veto
    2. ordinariest-reverberation-remain-subsidy
    3. noisiness-faraway-countrysides-straightens
    4. hardening-bribes-children-helpings
    5. calmest-outs-audition-cleaned

This is useful if someone is looking over your shoulder. Generate 20 passwords, and pick one. Each password is numbered, because your choice should be decided before the passwords are generated (if you generate 20 passwords, decided on a number between 1 and 20 beforehand). This prevents the urge to cherry pick passwords and decrease entropy.

## Cherry Picking Passwords

If the generated passwords contain too many esoteric words, *resist the urge to cherry pick passwords with easier to remember words.* This will decrease the entropy of the password in an unpredictable way. The proper way to generate passwords with more familiar words is to use the `-l` option to limit the length of each word. Although this will also decrease entropy, it will be done in such a way that the `-i` flag will still be able to calculate the entropy of the password. When using the `-l` flag, be sure to use it in conjunction with `-i` to ensure the entropy of the password is suitable for your needs.

So, use `xkpa -i -l NUM` until you've found a setting for the entropy you want. *Then generate one password and use it.* Don't keep generating a password until you've found one you "like."

##Dictionary File##
The dictionary file bundled with the script is from the `wamerican-small` package off Ubuntu. It strikes a nice balance between entropy and not having too many esoteric words. See README\_DICT.txt for the associated licenses and credits.

Modify the `DEFAULT_DICT` variable at the top of the script to use a different default.

##Randomness##
This script uses the `random.SystemRandom()` method. This should provide cryptographically secure randomness.

##License##
The `xkpa.py` script is released under the MIT license:

```
Copyright (c) 2012 Alex Beal

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

The dictionary file (`dict.txt`) is distributed under the license of its original authors located in the README\_DICT.txt file.
