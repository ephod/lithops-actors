import logging
import uuid
from typing import List, TypeVar, Tuple, Dict, Any

from actors import director
import actors.actor

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


class RoleClass(object):
    """An actor role class.

    This class replaces decorated role classes and can be
    used to obtain proxies to actors of that role.
    """
    __thtr_metadata__: 'actors.actor.RoleClassMetadata'

    def __init__(self, name, bases: List, attr):
        """Prevents users from directly inheriting from a RoleClass.
        This will be called when a class is defined with a RoleClass object
        as one of its base classes. To intentionally construct a RoleClass,
        use the '_thtr_from_enriched_class' class method.
        Raises:
            TypeError: Always.
        """
        for base in bases:
            if isinstance(base, RoleClass):
                raise TypeError(
                    f"Attempted to define subclass '{name}' of actor "
                    f"class '{base.__thtr_metadata__.class_name}'. "
                    "Inheriting from actor classes is "
                    "not currently supported.")

        # This shouldn't be reached because one of the base classes must be
        # an actor class if this was meant to be subclassed.
        assert False, "RoleClass.__init__ should not be called."

    def __call__(self, *args: Tuple, **kwargs: Dict):
        """Prevents users from directly instantiating an ActorClass.
        This will be called instead of __init__ when 'ActorClass()' is executed
        because an is an object rather than a metaobject. To properly
        instantiated a remote actor, use 'ActorClass.remote()'.
        Raises:
            Exception: Always.
        """
        raise TypeError("Actors cannot be instantiated. "
                        "Obtain references to them instead. "
                        f"Instead of '{self.__thtr_metadata__.class_name}()', "
                        f"use '{self.__thtr_metadata__.class_name}"
                        f".with_key(key)'.")

    @classmethod
    def _thtr_from_enriched_class(cls, enriched_class: _T, class_id: str) -> 'actors.actor.RoleClass':
        for attribute in [
            'with_key',
            # "_remote",
            '_thtr_from_modified_class',
        ]:
            if hasattr(enriched_class, attribute):
                logger.warning("Creating an actor from class "
                               f"{enriched_class.__name__} overwrites "
                               f"attribute {attribute} of that class")

        # The role class we are constructing inherits from the
        # original class so it retains all class properties.
        class DerivedRoleClass(cls, enriched_class):
            pass

        name = f"RoleClass({enriched_class.__name__})"
        DerivedRoleClass.__module__ = enriched_class.__module__
        DerivedRoleClass.__name__ = name
        DerivedRoleClass.__qualname__ = name
        # Construct the base object.
        self = DerivedRoleClass.__new__(DerivedRoleClass)
        # Role creation function descriptor.
        actor_creation_function_descriptor = actors.actor.RoleDescriptor.from_class(
            enriched_class.__thtr_actor_class__)

        self.__thtr_metadata__ = actors.actor.RoleClassMetadata(
            enriched_class, actor_creation_function_descriptor, class_id)

        return self

    def remote(self, *args: Tuple, **kwargs: Dict) -> 'actors.actor.ActorProxy':
        meta = self.__thtr_metadata__
        actor_key = meta.class_id + ':' + str(uuid.uuid4())

        proxy = actors.actor.ActorProxy(
            actor_key,
            meta.method_meta.signatures,
            meta.class_name,
            meta.class_id)
        weak_ref = proxy._to_weak()

        director.new_actor(meta, weak_ref, args, kwargs)

        return proxy

    def for_key(self, actor_key: str) -> 'actors.actor.ActorProxy':
        meta = self.__thtr_metadata__

        return actors.actor.ActorProxy(
            actor_key,
            meta.method_meta.signatures,
            meta.class_name,
            meta.class_id)
