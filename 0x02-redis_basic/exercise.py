#!/usr/bin/env python3

"""import the uuid, redis and typing module"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Any


def count_calls(method: Callable) -> Callable:
    """Tracks the number of calls made to a method in a Cache class."""

    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Invokes the given method after incrementing its call counter."""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return invoker


def call_history(method: Callable) -> Callable:
    """Tracks the call details of a method in a Cache class."""

    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Returns the method's output after storing its inputs and output."""
        in_key = "{}:inputs".format(method.__qualname__)
        out_key = "{}:outputs".format(method.__qualname__)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output

    return invoker


def replay(fn: Callable) -> None:
    """Displays the call history of a Cache class' method."""
    if fn is None or not hasattr(fn, "__self__"):
        return

    redis_store = getattr(fn.__self__, "_redis", None)

    if not isinstance(redis_store, redis.Redis):
        return

    fxn_name = fn.__qualname__
    in_key = "{}:inputs".format(fxn_name)
    out_key = "{}:outputs".format(fxn_name)
    fxn_call_count = 0

    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))

    print("{} was called {} times:".format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)

    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print("{}(*{}) -> {}".format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache():
    """Class that handles caches"""
    def __init__(self):
        """ tore an instance of the Redis client as a
        private variable named _redis (using redis.Redis())
        and flush the instance using flushdb"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key using uuid, store the
        input data in Redis using the random key and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str,
                                                          bytes, int, None]:
        """Retrieve data from Redis using the specified key.
        If fn is provided, use it to convert the data back
        to the desired format."""

        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve data from Redis as a string."""
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve data from Redis as an integer."""
        return self.get(key, lambda x: int(x))
