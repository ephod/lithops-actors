import logging
from typing import Optional, TypeVar, Dict, Tuple, List, Any

from actors import director
import actors.actor
from actors.actor import ActorProxy

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


class MethodHandler(object):
    _actor_proxy: 'actors.actor.ActorProxy'
    _method_name: str
    _with_future: bool

    def __init__(self, actor_proxy: 'actors.actor.ActorProxy', method_name: str):
        self._actor_proxy = actor_proxy  # TODO: make this a weak ref
        self._method_name = method_name
        self._with_future = False

    def __call__(self, *args: Tuple, **kwargs: Dict):
        raise TypeError("Actor methods cannot be called directly. Instead "
                        f"of running 'object.{self._method_name}()', try "
                        f"'object.{self._method_name}.remote()'.")

    def remote(self, *args: Tuple, **kwargs: Dict) -> Optional[str]:
        # TODO: we could let the user define the action id
        # TODO: check args for self references
        logger.debug(f"Calling method '{self._method_name}'"
                     f" on actor '{self._actor_proxy}'")

        # FIXME: checking all args for proxies is slow
        refs = False
        args: List[Any] = list(args)
        new_args: List[Any] = []
        for arg in args:
            if isinstance(arg, actors.actor.ActorProxy):
                refs = True
                arg: 'actors.actor.WeakRef' = arg._to_weak()
            new_args.append(arg)
        new_kwargs = {}
        for key, value in kwargs:
            if isinstance(value, actors.actor.ActorProxy):
                refs = True
                value: 'actors.actor.WeakRef' = value._to_weak()
            new_kwargs[key] = value
        new_action = actors.actor.Action(
            self._actor_proxy._thtr_actor_key,
            self._method_name,
            args=tuple(new_args),
            kwargs=new_kwargs,
            refs=refs)
        director.send_action(new_action)
        if self._with_future:
            return "This would be a Future"

    @property
    def future(self) -> 'actors.actor.MethodHandler':
        class WithFuture(MethodHandler):
            def __init__(s):
                super().__init__(self._actor_proxy, self._method_name)
                s._with_future = True

        return WithFuture()
