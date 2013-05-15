"""
FS in-process Redis implementation (incomplete)

"""

import sys
import os
from os.path import join as joinpath, dirname
from os.path import exists
import base64
py3 = sys.version_info >= (3,0)

import shutil

class FSRedis:
    def __init__(self, datadir, quote=base64.standard_b64encode,
                 unquote=base64.standard_b64decode):
        if hasattr(os, "fsencode"):
            datadir = os.fsencode(datadir)
        self.datadir = datadir
        self._quote = quote
        self._unquote = unquote

    def _getpath(self, *keys):
        if py3:
            k = []
            for key in keys:
                if isinstance(key, str):
                    key = key.encode("utf8")
                k.append(self._quote(key))
        else:
            k = [self._quote(x) for x in keys]
        return joinpath(self.datadir, *k)

    def flushdb(self):
        shutil.rmtree(self.datadir)
        os.mkdir(self.datadir)

    def _readpath(self, *keys):
        p = self._getpath(*keys)
        try:
            with open(p, "rb") as f:
                return f.read()
        except (IOError, OSError):
            return None

    # key value

    def get(self, key):
        return self._readpath(key)

    def set(self, key, val):
        p = self._getpath(key)
        with open(p, "wb") as f:
            f.write(val)

    def exists(self, key):
        return exists(self._getpath(key))

    # hashsets
    def hexists(self, key, field):
        p = self._getpath(key, field)
        return exists(p)

    def hget(self, key, field):
        return self._readpath(key, field)

    def hset(self, key, field, val):
        p = self._getpath(key, field)
        return self._hset(p, val)

    def _hset(self, p, val):
        dir = dirname(p)
        if not exists(dir):
            os.mkdir(dir)
        with open(p, "wb") as f:
            f.write(val)
        return True

    def hsetnx(self, key, field, val):
        p = self._getpath(key, field)
        if exists(p):
            return False
        return self._hset(p, val)

    def hdel(self, key, field):
        p = self._getpath(key, field)
        try:
            os.remove(p)
        except OSError:
            return False
        return True

    def hkeys(self, key):
        p = self._getpath(key)
        try:
            keys = os.listdir(p)
        except (IOError, OSError):
            return []
        return [self._unquote(x) for x in keys]

    def hgetall(self, key):
        p = self._getpath(key)
        try:
            keys = os.listdir(p)
        except (IOError, OSError):
            return []
        d = {}
        for subfile in keys:
            subpath = joinpath(p, subfile)
            with open(subpath, "rb") as f:
                d[self._unquote(subfile)] = f.read()
        return d

    def hmset(self, key, mapping):
        for name, val in mapping.items():
            self.hset(key, name, val)
        return True

    # sets
    def smembers(self, key):
        p = self._getpath(key)
        if not exists(p):
            return set()
        return [self._unquote(x) for x in os.listdir(p)]

    def sadd(self, key, field):
        p = self._getpath(key, field)
        if exists(p):
            return False
        subdir = dirname(p)
        if not exists(subdir):
            os.mkdir(subdir)
        open(p, "wb").close()
        return True

    def srem(self, key, field):
        p = self._getpath(key, field)
        if not exists(p):
            return False
        os.remove(p)
        return True

    def sismember(self, key, field):
        p = self._getpath(key, field)
        return exists(p)
