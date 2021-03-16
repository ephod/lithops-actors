import inspect
from typing import TypeVar

import actors.actor
from actors.util.inspect import (
    extract_signature,
    is_function_or_method,
    is_class_method,
    is_static_method,
)

_T = TypeVar("_T")


class RoleClassMethodMetadata(object):
    """Metadata of methods in a Role class."""
    _cache = {}

    def __init__(self):
        class_name = type(self).__name__
        raise TypeError(f"{class_name} can not be constructed directly, "
                        f"instead of running '{class_name}()', "
                        f"try '{class_name}.create()'")

    @classmethod
    def clear_cache(cls):
        cls._cache.clear()

    @classmethod
    def create(
        cls: 'actors.actor.RoleClassMethodMetadata',
        modified_class: _T,
        actor_creation_function_descriptor: 'actors.actor.RoleDescriptor') -> 'actors.actor.RoleClassMethodMetadata':
        # Try to create an instance from cache.
        cached_meta = cls._cache.get(actor_creation_function_descriptor)
        if cached_meta is not None:
            return cached_meta

        # Create an instance without __init__ called.
        self = cls.__new__(cls)

        actor_methods = inspect.getmembers(modified_class, is_function_or_method)
        self.methods = dict(actor_methods)
        self.signatures = {}
        for method_name, method in actor_methods:
            # Whether or not this method requires binding of its first
            # argument. For class and static methods, we do not want to bind
            # the first argument, but we do for instance methods
            is_bound = (is_class_method(method) or is_static_method(modified_class, method_name))

            self.signatures[method_name] = extract_signature(method, ignore_first=not is_bound)

        cls._cache[actor_creation_function_descriptor] = self
        return self
