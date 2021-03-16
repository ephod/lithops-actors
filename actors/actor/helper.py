import logging
from typing import Optional, TypeVar

import actors.actor
from actors.util.inspect import is_function_or_method

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


def enrich_class(cls: _T) -> _T:
    # check if cls is already an enriched class.
    if hasattr(cls, '__thtr_actor_class__'):
        return cls

    # Modify the class to have an additional method that will be used
    # stop the actor.
    class Class(cls):
        __thtr_actor_class__ = cls  # The original actor class

        def __thtr_stop_actor__(self):
            pass  # TODO: is it necessary here?

    Class.__module__ = cls.__module__
    Class.__name__ = cls.__name__

    if not is_function_or_method(getattr(Class, '__init__', None)):
        # Add __init__ if it does not exist.
        # Assign an __init__ function will avoid many checks later on.
        def __init__(self):
            pass

        Class.__init__ = __init__

    return Class


def make_role_class(cls: _T, class_id: Optional[str]) -> 'actors.actor.RoleClass':
    if class_id is None:
        class_id = 'lithops:' + cls.__name__
    Enriched = enrich_class(cls)
    return actors.actor.RoleClass._thtr_from_enriched_class(Enriched, class_id)
