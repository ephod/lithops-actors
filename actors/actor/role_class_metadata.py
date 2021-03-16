from typing import Optional, TypeVar, Any, Union, Callable

import actors.actor

_T = TypeVar("_T")


class RoleClassMetadata(object):
    """Metadata for a role class.
    Attributes:
        enriched_class: The original class that was replaced.
        role_creation_function_descriptor: The function descriptor for
            the actor creation task.
        class_id: The ID of this actor class.
        class_name: The name of this class.
        method_meta: The actor method metadata.
    """
    enriched_class: _T
    actor_creation_function_descriptor: 'actors.actor.RoleDescriptor'
    class_id: str
    proxy_crafter: Callable[[Any], 'actors.actor.ActorProxy']
    method_meta: Union[Optional['actors.actor.RoleClassMethodMetadata'], Any]
    class_name: str

    def __init__(
        self,
        enriched_class: _T,
        role_creation_function_descriptor: 'actors.actor.RoleDescriptor',
        class_id: str):
        self.enriched_class = enriched_class
        self.actor_creation_function_descriptor = \
            role_creation_function_descriptor
        self.class_name = role_creation_function_descriptor.class_name
        self.class_id = class_id
        self.method_meta = actors.actor.RoleClassMethodMetadata.create(
            enriched_class, role_creation_function_descriptor)
        self.proxy_crafter = lambda actor_key: actors.actor.ActorProxy(
            actor_key,
            self.method_meta.signatures,
            self.class_name,
            self.class_id
        )
