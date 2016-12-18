from os import remove
from hdcache import hdcache

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
