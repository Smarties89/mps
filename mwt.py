import time
import logging

log = logging.getLogger(__name__)


class MemoizeWithTimeout(object):
    """Memoize With Timeout


    The implementation builds on Leslie Polzer code from 
    http://code.activestate.com/recipes/325905-memoize-decorator-with-timeout
    The code have been modified to support log and flushing.
    """
    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=2):
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
                log.info("cache")
                if (time.time() - v[1]) > self.timeout or kwargs.get('mwt_flush', False):
                    raise KeyError
            except KeyError:
                log.info("new")

                if 'mwt_flush' in kwargs:
                    del kwargs['mwt_flush']

                v = self.cache[key] = f(*args,**kwargs),time.time()

            return v[0]
        func.func_name = f.__name__

        return func
