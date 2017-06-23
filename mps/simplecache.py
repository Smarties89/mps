#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from time import time


class SimpleCache:
    def __init__(self, timeout, storage=None):
        if storage is None:
            storage = {}

        self._cache = storage
        self._timeout = timeout

    def _generate_key(self, args):
        key = u""
        for arg in args:
            key += str(arg)
        return key

    def get(self, *args):
        key = self._generate_key(args)
        cache = self._cache.get(key, None)
        # Not in cache
        if cache is None:
            return None

        # Not valid anymore after timeout
        if cache['created'] + self._timeout < time():
            return None

        return cache['data']

    def save(self, data, *args):
        key = self._generate_key(args)
        self._cache[key] = {'data': data, 'created': time()}
