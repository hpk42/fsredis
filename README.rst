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

There is some support for:

- key/val: get/set/del
- hashsets: hget/hset/hgetall/hexists/hmset
- sets: sadd/smembers/srem

