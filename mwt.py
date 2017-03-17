import time


class MWT(object):
    """Memoize With Timeout
    The implementation is taken from Leslie Polzer at
    http://code.activestate.com/recipes/325905-memoize-decorator-with-timeout
    and slighty modified to support log.
    """
    _caches = {}
    _timeouts = {}

    def __init__(self, log, timeout=2):
        self.log = log
        self.timeout = timeout

    def collect(self):
        """Clear cache of results which have timed out"""
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                if (time.time() - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            self._caches[func] = cache

    def __call__(self, f):
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            kw = sorted(kwargs.items())
            key = (args, tuple(kw))
            try:
                v = self.cache[key]
                self.log.info("cache")
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                self.log.info("new")
                v = self.cache[key] = f(*args,**kwargs),time.time()
            return v[0]
        func.func_name = f.__name__

        return func
