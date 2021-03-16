from inspect import (
    getmro,
    isfunction,
    ismethod,
    Parameter,
    signature)
from typing import Callable, List, TypeVar

_T = TypeVar("_T")


def is_function_or_method(obj: object) -> bool:
    return isfunction(obj) or ismethod(obj)


def is_class_method(f: _T) -> bool:
    """Returns whether the given method is a class method."""
    return hasattr(f, "__self__") and f.__self__ is not None


def is_static_method(cls: _T, f_name: str) -> bool:
    for cls in getmro(cls):
        if f_name in cls.__dict__:
            return isinstance(cls.__dict__[f_name], staticmethod)
    return False


def extract_signature(func: Callable, ignore_first: bool = False) -> List[Parameter]:
    """Extract the function signature from the function.

    :param func: The function whose signature should be extracted.
    :param ignore_first: True if the first argument should be ignored.
        Like in the case of a class method.
    :return: List of Parameter objects representing the function signature.
    """
    signature_parameters: List[Parameter] = list(signature(func).parameters.values())

    if ignore_first:
        if len(signature_parameters) == 0:
            raise ValueError("Methods must take a 'self' argument, but the "
                             f"method '{func.__name__}' does not have one.")
        signature_parameters = signature_parameters[1:]

    return signature_parameters
