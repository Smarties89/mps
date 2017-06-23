from time import sleep

from simplecache import SimpleCache

def test_simple_cache():
    cache = SimpleCache(0.1)

    assert cache.get("hamster") == None
    cache.save("yumyum", "hamster")
    assert cache.get("hamster") == "yumyum"
    sleep(0.1)
    assert cache.get("hamster") == None
