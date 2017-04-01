## Introduction

This python script implements the [xkcd password spec](http://xkcd.com/936/).

## Install

This package requires the `pip` Python package manager for installation. [pip installation instructions](http://www.pip-installer.org/en/latest/installing.html).

Then:

```
pip install xkpa
```

## Usage

```
% xkpa -h
usage: xkpa.py [-h] [-n] [-d DICT_PATH] [-x] [-i] [-s SEPARATOR] [-l LENGTH]
               [-c COUNT] [-v]
               [w]

Generate an xkcd style password.

positional arguments:
  w             The number of words in the password. Defaults to 4.

optional arguments:
  -h, --help    show this help message and exit
  -n            Disable printing a newline at the end of the password. Good
                for piping to the clipboard.
  -d DICT_PATH  The dictionary file. Defaults to [PATH].
  -x            Disable excluding special characters and punctuation.
  -i            Enable showing password information (entropy, etc).
  -s SEPARATOR  Delimit words with a given character/string.
  -l LENGTH     The maximum word length. Words must be at or below this
                length.
  -c COUNT      Number of passwords to generate. Defaults to 1.
  -v            Display version information.

http://xkcd.com/936/
```

## Examples
**Generate a password, and put it in the clipboard (OS X)**

    xkpa -n | pbcopy

**Generate a password, copy to clipboard, and print info**

    xkpa -ni | pbcopy
    Info:
      Entropy: 61.292 bits
      Entropy per word: 15.323 bits
      Possible combinations given settings: 2.0 million trillion
      Average time to crack at 1.0 thousand tries per second: 44.7 million years
      Average time to crack at 70.0 thousand tries per second: 629.8 thousand years
      Average time to crack at 75.0 million tries per second: 580.8 years
      Average time to crack at 350.0 billion tries per second: 0.1 years

The password will get copied to the clipboard, but the info message will not (the info message is printed to stderr).

**Generate a password with info**

    xkpa -i
    wincing-peaceful-transplanted-nitrated
    
    Info:
      Entropy: 61.292 bits
      Entropy per word: 15.323 bits
      Possible combinations given settings: 2.0 million trillion
      Average time to crack at 1.0 thousand tries per second: 44.7 million years
      Average time to crack at 70.0 thousand tries per second: 629.8 thousand years
      Average time to crack at 75.0 million tries per second: 580.8 years
      Average time to crack at 350.0 billion tries per second: 0.1 years

**Generate a password with 5 words separated by '.'**

    xkpa -s '.' 5
    belies.annoyingly.birthing.ventilate.icon

**Generate a password with words no longer than 5 characters in length**

    xkpa -l 5
    cover-kings-yard-store

**Generate multiple passwords**

    xkpa -c 5
    1. excite-incriminating-wronged-veto
    2. ordinariest-reverberation-remain-subsidy
    3. noisiness-faraway-country-sides-straightens
    4. hardening-bribes-children-helpings
    5. calmes-touts-audition-cleaned

This is useful if someone is looking over your shoulder. By generating multiple passwords, someone looking over your shoulder will not know which is your real password. Each password is numbered, because your choice should be decided *before the passwords are generated* (if you generate 20 passwords, decided on a number between 1 and 20 beforehand). This prevents the urge to cherry pick passwords and decrease entropy.

## Cherry Picking Passwords

If the generated passwords contain too many esoteric words, *resist the urge to cherry pick passwords with easier to remember words.* This will decrease the entropy of the password in an unpredictable way. The proper way to generate passwords with more familiar words is to use the `-l` option to limit the length of each word. Although this will also decrease entropy, it will be done in such a way that the `-i` flag will still be able to calculate the entropy of the password. When using the `-l` flag, be sure to use it in conjunction with `-i` to ensure the entropy of the password is suitable for your needs.

So, use `xkpa -i -l NUM` until you've found a setting with the desired entropy. *Then generate one password and use it.* Don't keep generating a password until you've found one you "like."

Do not use the `-c` flag to generate several passwords at once, and cherry pick. This option is meant for use in public places where someone may be looking over your shoulder. The proper way to use this option is to think of a number between 1 and 100, and then generate 100 passwords with `xkpa -c 100`. Then choose the password which corresponds to the number you've already picked. This way, you're not cherry picking, and if someone glances over your shoulder, they won't know which of the 100 passwords is your real password.

## Entropy

How much entropy you need really depends on what you're trying to protect against. State of the art password crackers can crack Windows password files at a rate of [300+ billion attempts per second](http://passwords12.at.ifi.uio.no/Jeremi_Gosney_Password_Cracking_HPC_Passwords12.pdf) [PDF] and this rate will only increase in the future. On the other hand, brute forcing a remote sever will take place at a much lower rate, and secure servers should have throttling mechanisms in place making this sort of attack obsolete. So, if you're worried that someone will try to reverse your hashed password, and you think your passwords are being hashed with a weak algorithm (e.g., MD5 or NTLM), then aim for high entropy. If you're generating a password for a remote server, and that server has throttling mechanisms in place, or your passwords are being hashed with a more secure algorithm (e.g., bcrypt), a lower entropy may be acceptable.

The information on time-to-crack given by the `-i` flag was specifically chosen because these values represent the current state of the art. Weak hashes, like NTLM and MD5 can be attempted at 350 billion and 180 billion tries per second, respectively. bcrypt, a more secure hash, slows this same attack down to 70 thousand attempts per second (75 million/sec for md5crypt). Attacks against remote servers probably happen somewhere within an order of magnitude of 1,000 attempts per second against a poorly secured server, and would be immediately throttled against a secure server. [CloudCracker](https://www.cloudcracker.com/) boasts a rate of 300,000,000 words in 20 minute, or 41,000 words per second.

## Config File

There is no config file. Set default arguments by adding an alias to your `~/.bashrc`:

    alias pgen="xkpa -nil 5 5"

## Dictionary File
The dictionary file bundled with the script is from the `wamerican-small` package off Ubuntu. It strikes a nice balance between entropy and not having too many esoteric words. See README\_DICT.txt for the associated licenses and credits.

Modify the `DEFAULT_DICT` variable at the top of the script to use a different default.

## Randomness
This uses Python's [`random.SystemRandom`](https://docs.python.org/3/library/random.html#random.SystemRandom) as a source of entropy. This provides cryptographically secure randomness.

## License
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
