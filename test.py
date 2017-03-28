import os
from os import remove
from hdcache import hdcache

from .errorrecoveryfile import ErrorRecoveryFile

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
