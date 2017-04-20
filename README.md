# mps
My Python Snippets

My Python Snippets is a collection of nice to have and missing batteries for Python.
The snippes are organised as a library, but is separated into individual files that can be included in projects together.

Documentation is on this one page. 


# Table of Contents

 * [randstr](#randstr) - get a random string of numbers/characters
 * [hdcache](#hdcache) - hdcache makes it easy to use the harddrive as a cache for function results
 * [Contributors](#Contributors)



# randstr
randstr creates a random string of numbers and upper/lowercase characters.

```
>>> import mps
>>> mps.randstr()
'N5KZRC06'
>>> mps.randstr(nsize=100)
'5QRDHYESVHMNL68E0IPYEIP3TXBUU86V26PSIEZ4AWE1FAX3G2WCSJ38NAIHB9DM3ZCCI102AI6TAOC967XM3UW6ZH5X9S8OQR23'
>>> 
```

# hdcache
hdcache makes it easy to use the harddrive as a cache for function results. An example below shows how to do it, and the result of calling the script twice is below that.

```#!/bin/python
from mps import hdcache

@hdcache("cachedresult")
def docomputation(x, y): 
    print("Doing hard computation for {} + {}".format(x, y)) 
    return str(x+y)

result = docomputation(2, 3, cachekey="2 plus 3")
print("Result is {}".format(result))
```
This saves the docompuation on the cacheid of *2+3* in the file "cachedresult". The cachekey should be a unique string of the computation.

```
user@hostname:~$ python testhdcache.py 
Doing hard computation for 2 + 3
Result is 5
user@hostname:~$ python testhdcache.py 
Result is 5
user@hostname:~$ 
```


Contributors
==========

* smarties89
