#!/bin/python
import os
import shelve


def _getcachekey(args, kwargs):
    cachekey = kwargs.get('cachekey', None)
    if cachekey is not None:
        del kwargs['cachekey']
        return cachekey

    return str(args) + str(kwargs)



def hdcache(directory):
    """
        Decorator function that permantly cache function calls on the
        harddrive.
    """
    def decs(func):
        def checkexists(*args, **kwargs):
            cache = shelve.open(directory)
            cachekey =  _getcachekey(args, kwargs)

            if cachekey not in cache:
                cache[cachekey] = func(*args, **kwargs)

            result = cache[cachekey]
            cache.close()
            return result

        return checkexists
    return decs
