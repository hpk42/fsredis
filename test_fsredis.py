
import pytest

from fsredis import FSRedis
from redis import StrictRedis

@pytest.fixture(scope="class", params=["fs", "real"])
def redis(request):
    if request.param == "fs":
        tmpdir = request.config._tmpdirhandler.mktemp("fsredis")
        return FSRedis(str(tmpdir))
    else:
        return StrictRedis()

@pytest.fixture(autouse=True)
def cleanredis(redis):
    redis.flushdb()

@pytest.fixture(params=[b"key1", b"key1/sub"])
def key(request):
    return request.param

class TestKeyVal:
    def test_getsetdel(self, redis, key):
        assert redis.get(key) is None
        redis.set(key, b"world")
        assert redis.get(key) == b"world"
        assert redis.exists(key)
        assert redis.delete(key)
        assert not redis.delete(key)
        assert not redis.exists(key)

    def test_multidelete(self, redis):
        redis.set(b"key1", b"val1")
        redis.set(b"key2", b"val2")
        redis.set(b"key3", b"val3")
        assert redis.delete(b"key1", b"key2")
        assert redis.delete(b"key2", b"key3")

    def test_exists(self, redis, key):
        assert not redis.exists(key)


class TestSet:
    def test_basics(self, redis, key):
        assert not redis.smembers(key)
        assert redis.sadd(key, "hello")
        assert not redis.sadd(key, "hello")
        assert redis.sismember(key, "hello")
        assert redis.smembers(key) == set([b"hello"])
        assert not redis.sismember(key, "other")
        assert redis.srem(key, "hello")
        assert not redis.srem(key, "hello")


class TestHashSet:
    def test_getsetdel(self, redis, key):
        field = b"field1/some"
        assert not redis.hexists(key, field)
        assert redis.hget(key, field) is None
        redis.hset(key, field, b"world")
        assert redis.hexists(key, field)
        assert redis.hget(key, field) == b"world"
        assert redis.hdel(key, field)
        assert not redis.hdel(key, field)
        assert redis.hget(key, field) is None

    def test_hsetnx(self, redis, key):
        assert redis.hsetnx(key, b"field1", b"val")
        assert not redis.hsetnx(key, b"field1", b"val2")
        assert redis.hget(key, b"field1") == b"val"

    def test_hkeys_getall(self, redis):
        redis.hset(b"key10", b"field1", b"val1")
        redis.hset(b"key10", b"field2", b"val2")
        assert set(redis.hkeys(b"key10")) == set([b"field1", b"field2"])
        assert redis.hgetall(b"key10") == {
                b"field1": b"val1",b"field2":b"val2"}

    def test_hgetall_empty(self, redis):
        assert redis.hgetall(b"key11") == {}

    def test_hmset(self, redis):
        redis.hset(b"key", b"field0", b"val0")
        assert redis.hmset(b"key", {b"field1": b"val1", b"field2": b"val2"})
        d = redis.hgetall(b"key")
        assert d == {b"field0":b"val0", b"field1": b"val1", b"field2": b"val2"}

