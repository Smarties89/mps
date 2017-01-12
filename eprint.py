from __future__ import print_function
import sys

# Credits go to MarcH from http://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python#14981125

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
