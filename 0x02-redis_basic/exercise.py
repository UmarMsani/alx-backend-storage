#!/usr/bin/env python3
""" redis caching client modules.
"""
import redis
from uuid import uuid4
from functools import wraps
from typing import Any, Callable, Optional, Union


def count_calls(method: Callable) -> Callable:
    """ decorator track the call count of Cache class methods
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """ wrap called method and increments its call count Redis before executions.
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ decorators to track arguments of Cache class method..
    """
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """raps the called method and tracks it passed args by storing them in Redis...
        """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """Redis for how many times a function was called and display:
            - how many times it was called
            - Function arguments and output for each calls..
    """
    client = redis.Redis()
    calls = client.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


class Cache:
    """ cach class for Redis....
    """
    def __init__(self) -> None:
        """initialize  new cache objects.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes,  int,  float]) -> str:
        """ Store a data in Redis with a randomly generated keys...
        """
        key = str(uuid4())
        client = self._redis
        client.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """ gets value of a key from Redis and converts it ...
            the result byted into the correct data type..
        """
        client = self._redis
        value = client.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_str(self, data: bytes) -> str:
        """ Converting bytes to a string..
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """ Converting bytes to integers..
        """
        return int(data)

