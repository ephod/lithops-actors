import logging
from typing import TypeVar, Dict, Any

from actors import director
import actors.actor

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


class ActorProxy(object):
    """An actor proxy or handle.

    Fields are prefixed with _thtr_ to hide them and to avoid collisions.
    """
    _thtr_actor_key: str
    _thtr_method_signatures: Dict[str, Any]
    _thtr_class_name: str
    _thtr_class_id: str

    def __init__(self, actor_key: str, methods_signs: Dict[str, Any], class_name: str, class_id: str):
        self._thtr_actor_key = actor_key
        self._thtr_method_signatures = methods_signs
        self._thtr_class_name = class_name
        self._thtr_class_id = class_id

        for method_name in self._thtr_method_signatures.keys():
            # TODO: Python function descriptors to load/import classes when
            #  needed. When recreating proxies or sending them elsewhere.
            # function_descriptor = PythonFunctionDescriptor(
            #     module_name, method_name, class_name)
            # self._function_descriptor[
            #     method_name] = function_descriptor
            method = actors.actor.MethodHandler(self, method_name)
            setattr(self, method_name, method)

        setattr(self, 'pls_stop', self.__stop)

    def __stop(self) -> None:
        director.send_stop(self._thtr_actor_key)

    def _to_weak(self) -> 'actors.actor.WeakRef':
        return actors.actor.WeakRef(
            self._thtr_actor_key,
            self._thtr_method_signatures,
            self._thtr_class_name,
            self._thtr_class_id)

    @staticmethod
    def _from_weak(weak: 'actors.actor.WeakRef') -> 'actors.actor.ActorProxy':
        return ActorProxy(
            weak._thtr_actor_key,
            weak._thtr_method_signatures,
            weak._thtr_class_name,
            weak._thtr_class_id)

    def __eq__(self, other) -> bool:
        if isinstance(other, ActorProxy):
            return self._thtr_actor_key == other._thtr_actor_key
        return False

    # Make tab completion work.
    def __dir__(self):
        return self._thtr_method_signatures.keys()

    def __repr__(self) -> str:
        return (f"Actor("
                f"{self._thtr_class_name}, "
                f"{self._actor_key})")

    @property
    def _actor_key(self) -> str:
        return self._thtr_actor_key
