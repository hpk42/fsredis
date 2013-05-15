fsredis
=======

fsredis is a Python module offering limited parts of the Python
redis API, and persisting to the filesystem.

To get started::

    >>> from fsredis import FSRedis
    >>> redis = FSRedis(datadir)
    >>> redis.set("hello", "world")
    >>> redis.get("hello")
    world

For now, use completion to find out which operations are supported.
Works for me.
