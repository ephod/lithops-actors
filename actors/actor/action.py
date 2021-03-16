import logging
import uuid
from typing import TypeVar, Dict, Optional, Tuple, List, Union, Any

import actors.actor

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


class Action(object):
    """Create a new representation of an action.

    If no *action_id* is given, a new one is generated.
    """
    actor_key: str
    method_name: str
    action_id: str
    args: Union[tuple, list, None, List[Any]]
    kwargs: Union[dict, None, Dict[Any, Any]]
    refs: bool

    def __init__(
        self,
        actor_key: str,
        method_name: str,
        action_id: Optional[str] = None,
        args: Optional[Union[Tuple, List]] = None,
        kwargs: Optional[Dict] = None,
        refs: bool = False):
        self.args = args or []
        self.kwargs = kwargs or {}
        self.action_id = action_id or uuid.uuid4().hex
        self.actor_key = actor_key
        self.method_name = method_name
        self.refs = refs

    def call(self, instance):
        if self.refs:
            args = list(self.args)
            new_args = []
            for arg in args:
                if isinstance(arg, actors.actor.WeakRef):
                    arg = actors.actor.ActorProxy._from_weak(arg)
                new_args.append(arg)
            self.args = tuple(new_args)
            new_kwargs = {}
            for key, value in self.kwargs:
                if isinstance(value, actors.actor.WeakRef):
                    value = actors.actor.ActorProxy._from_weak(value)
                new_kwargs[key] = value
            self.kwargs = new_kwargs
        """Run this action on the *instance*"""
        method = getattr(instance, self.method_name)
        return method(*self.args, **self.kwargs)

    def __repr__(self) -> str:
        return f"Action({self.actor_key}, {self.method_name}, {self.action_id})"
