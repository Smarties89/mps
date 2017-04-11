import logging
import os
from os import remove
from time import sleep

from .hdcache import hdcache
from .errorrecoveryfile import ErrorRecoveryFile
from .mwt import MemoizeWithTimeout

_changed = False

@hdcache("cachedresult")
def docomputation(x, y): 
    global _changed
    _changed = True
    return str(x+y)


def test_cacheresult_with_cachekey():
    global _changed
    try:
        remove("cachedresult")
    except:
        pass
    _changed = False 
    assert docomputation(2, 3, cachekey="2 plus 3") == "5"
    assert _changed == True
    _changed = False
    assert docomputation(2, 3, cachekey="2 plus 3") == "5"
    assert _changed == False 


def test_cacheresult_without_cachekey():
    global _changed
    try:
        remove("cachedresult")
    except:
        pass
    _changed = False 
    assert docomputation(2, 3) == "5"
    assert _changed == True
    _changed = False
    assert docomputation(2, 3) == "5"
    assert _changed == False 


def test_errorrecovery():
    er = ErrorRecoveryFile('/tmp', {})
    assert er.dataid is not None
    assert 'inprogress_' in er.current
    assert er.current.startswith('/tmp/')
    assert os.path.exists(er.current) == True
    oldpath = er.current

    er.status = 'dropped'
    assert 'dropped_' in er.current
    assert os.path.exists(er.current) == True
    assert oldpath != er.current

    er.remove()
    assert er.current is None
    assert os.path.exists(oldpath) == False
    # Should not give an exception.
    er.remove()


memoized_i = 0
@MemoizeWithTimeout(logging.getLogger(), 0.1)
def memoized_function():
    global memoized_i
    memoized_i += 1
    return memoized_i


def test_mwt_normal_use():
    global memoized_i
    memoized_i = 0
    assert memoized_function() == 1
    assert memoized_i == 1
    assert memoized_function() == 1
    assert memoized_i == 1

    sleep(0.15)

    assert memoized_i == 1
    assert memoized_function() == 2
    assert memoized_i == 2
    assert memoized_function() == 2
    assert memoized_i == 2


def test_mwt_with_flush():
    global memoized_i
    memoized_i = 0
    assert memoized_function(mwt_flush=True) == 1
    assert memoized_i == 1
    assert memoized_function(mwt_flush=True) == 2
    assert memoized_i == 2
    assert memoized_function(mwt_flush=True) == 3
    assert memoized_i == 3
