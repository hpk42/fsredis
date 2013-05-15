fsredis
=======

fsredis is a Python module offering limited parts of the Python
redis API, and persisting to the filesystem.

To get started::

    pip install fsredis

and then on the interactive python prompt::

    >>> from fsredis import FSRedis
    >>> redis = FSRedis(datadir)
    >>> redis.set("hello", "world")
    >>> redis.get("hello")
    world

hopefully you have completion and can check for more operations :)

There is some support for:

- key/val: get/set/del
- hashsets: hget/hset/hgetall/hexists/hmset
- sets: sadd/smembers/srem

These operations are tested both with the original Redis
API and the FSRedis api on Python26, python26 and Python33.

I welcome pull requests to fix things or add operations
if they are tested.


copyright: Holger Krekel 2013, License: MIT

