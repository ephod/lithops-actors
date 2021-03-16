from typing import List, Dict

import actors.actor


class WeakRef(object):
    _thtr_actor_key: str
    _thtr_method_signatures: Dict[str, List]
    _thtr_class_name: str
    _thtr_class_id: str

    def __init__(self, actor_key: str, methods_signs: Dict[str, List], class_name: str, class_id: str):
        self._thtr_actor_key = actor_key
        self._thtr_method_signatures = methods_signs
        self._thtr_class_name = class_name
        self._thtr_class_id = class_id

    def build_proxy(self) -> 'actors.actor.ActorProxy':
        return actors.actor.ActorProxy._from_weak(self)
