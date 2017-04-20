import string
import random


def randstr(n=8):
    """
    randstr creates a random string of numbers and upper/lowercase characters.


    >>> randstr()
    "0YH58H9E"
    >>> randstr(5)
    "0ds34"

    This code is slighty modified version of
    http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(n))
