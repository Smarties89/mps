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
        Decorator function that permantly cache function calls in a file 

        Example

	>>> @hdcache("cachedresult.db")
	>>> def docomputation(x, y):
	>>>    print("Doing hard computation for {} + {}".format(x, y))
	>>>    return str(x+y)

	>>> docomputation(2, 3, cachekey="2 plus 3")
	"Doing hard computation for 2 + 5"
	"5"
	>>> docomputation(2, 3, cachekey="2 plus 3")
	"5"

	The second docomputation does not call the actual function but retrieves
        the result from the file "cachedresult.db"
        Moreover, next time the program is called the result will also be cached
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
