import pytest
from forged.namespacing.core.namespace import Namespace
from forged.namespacing.core.symbol import Symbol
from forged.namespacing.registry.composable import CompositeNamespace

@pytest.fixture
def namespace():
    return Namespace()

def test_register_and_resolve(namespace):
    namespace.register("test.path", "value")
    assert namespace.resolve("test.path") == "value"

def test_unregister(namespace):
    namespace.register("test.path", "value")
    namespace.unregister("test.path")
    with pytest.raises(KeyError):
        namespace.resolve("test.path")

def test_composite_namespace():
    ns1 = Namespace("ns1")
    ns2 = Namespace("ns2")
    composite = CompositeNamespace(ns1, ns2)

    ns1.register("shared.path", "value1")
    ns2.register("shared.path", "value2")

    assert composite.resolve("shared.path") == "value1"
    assert composite.resolve_all("shared.path") == ["value1", "value2"]

def test_symbol_metadata():
    symbol = Symbol(value="test_value", name="test_symbol")
    symbol.attach_metadata("key", "value")
    assert symbol.get_metadata("key") == "value"