from enum import Enum
from inspect import Parameter
from typing import Optional
import unittest

from actors.util.inspect import (
    extract_signature,
    is_class_method,
    is_function_or_method,
    is_static_method)


class Text(Enum):
    FUNCTION = 'function'
    INSTANCE_METHOD = 'instance_method'
    CLASS_METHOD = 'class_method'
    STATIC_METHOD = 'static_method'


def function_stub() -> str:
    return Text.FUNCTION.value


def function_with_one_argument(first_name: str) -> str:
    return first_name


def function_with_two_arguments(first_name: str, last_name: str) -> str:
    return f"{first_name} {last_name}"


class ClassStub(object):
    name: str

    def __init__(self, name: str):
        self.name = name

    def instance_method(self) -> str:
        return self.name

    @classmethod
    def class_method(cls):
        return cls(Text.CLASS_METHOD.value)

    @staticmethod
    def static_method():
        return Text.STATIC_METHOD.value


class ChildClassStub(ClassStub):
    pass


class TestInspectMethods(unittest.TestCase):
    class_stub: Optional[ClassStub]
    name: str

    def setUp(self):
        self.function_execution = function_stub()
        self.function_reference = function_stub
        self.function_reference_with_one_argument = function_with_one_argument
        self.function_reference_with_two_arguments = function_with_two_arguments
        self.name = Text.INSTANCE_METHOD.value
        self.class_stub = ClassStub(self.name)
        self.child_class_stub = ChildClassStub(self.name)

    def tearDown(self):
        self.function_execution = None
        self.function_reference = None
        self.function_reference_with_one_argument = None
        self.function_reference_with_two_arguments = None
        self.name = ''
        self.class_stub = None
        self.child_class_stub = None

    def test_function_execution_is_not_function(self) -> None:
        self.assertFalse(is_function_or_method(self.function_execution))

    def test_function_reference_is_function(self) -> None:
        self.assertTrue(is_function_or_method(self.function_reference))

    def test_class_instance_method_execution_is_not_method(self) -> None:
        self.assertFalse(is_function_or_method(self.class_stub.class_method()))

    def test_class_instance_method_reference_is_method(self) -> None:
        self.assertTrue(is_function_or_method(self.class_stub.class_method))

    def test_class_instance_method_execution(self) -> None:
        self.assertFalse(is_class_method(self.class_stub.instance_method()))

    def test_class_instance_method_reference(self) -> None:
        self.assertTrue(is_class_method(self.class_stub.instance_method))

    def test_class_method_execution(self) -> None:
        self.assertFalse(is_class_method(self.class_stub.class_method()))

    def test_class_method_reference(self) -> None:
        self.assertTrue(is_class_method(self.class_stub.class_method))

    def test_class_static_method_execution(self) -> None:
        self.assertFalse(is_class_method(self.class_stub.static_method()))

    def test_class_static_method_reference(self) -> None:
        self.assertFalse(is_class_method(self.class_stub.static_method))

    def test_method_resolution_order_within_is_static_method(self) -> None:
        with self.assertRaises(AttributeError):
            is_static_method(self.class_stub, Text.STATIC_METHOD.value)
        with self.assertRaises(AttributeError):
            is_static_method(self.child_class_stub, Text.STATIC_METHOD.value)

        self.assertTrue(is_static_method(self.class_stub.__class__, Text.STATIC_METHOD.value))
        self.assertTrue(is_static_method(self.child_class_stub.__class__, Text.STATIC_METHOD.value))

        self.assertFalse(is_static_method(self.child_class_stub.__class__, Text.CLASS_METHOD.value))
        self.assertFalse(is_static_method(self.child_class_stub.__class__, Text.CLASS_METHOD.value))

    def test_non_existing_method_within_is_static_method(self) -> None:
        self.assertFalse(is_static_method(self.child_class_stub.__class__, Text.FUNCTION.value))
        self.assertFalse(is_static_method(self.child_class_stub.__class__, Text.FUNCTION.value))

    def test_extract_signature(self) -> None:
        with self.assertRaises(ValueError):
            extract_signature(self.function_reference, True)
        expect = []
        self.assertListEqual(extract_signature(self.function_reference_with_one_argument, True), expect)
        expect = [Parameter(name='last_name', kind=Parameter.POSITIONAL_OR_KEYWORD, annotation=str)]
        self.assertListEqual(extract_signature(self.function_reference_with_two_arguments, True), expect)


if __name__ == '__main__':
    unittest.main()
