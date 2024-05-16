#!/usr/bin/env python3

"""import the uuid, redis and typing module"""
import redis
import uuid
from typing import Union, Callable


class Cache():
    def __init__(self):
        """ tore an instance of the Redis client as a
        private variable named _redis (using redis.Redis())
        and flush the instance using flushdb"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key using uuid, store the
        input data in Redis using the random key and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, None]:
        """Retrieve data from Redis using the specified key.
        If fn is provided, use it to convert the data back to the desired format."""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve data from Redis as a string."""
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve data from Redis as an integer."""
        return self.get(key, int)
