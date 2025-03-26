import pytest
from forged.elements.namespaces.core.namespace import Namespace
from forged.elements.namespaces.composite import CompositeNamespace

def test_composite_resolve():
    base = Namespace("base")
    plugins = Namespace("plugins")
    local = Namespace("local")

    base.register("foo", 123)
    plugins.register("bar", 456)
    local.register("baz", 789)

    composite = CompositeNamespace(base, plugins, local)

    assert composite.resolve("foo") == 123
    assert composite.resolve("bar") == 456
    assert composite.resolve("baz") == 789

def test_composite_contains():
    base = Namespace("base")
    plugins = Namespace("plugins")
    local = Namespace("local")

    base.register("foo", 123)
    plugins.register("bar", 456)
    local.register("baz", 789)

    composite = CompositeNamespace(base, plugins, local)

    assert "foo" in composite
    assert "bar" in composite
    assert "baz" in composite
    assert "nonexistent" not in composite

def test_composite_list():
    base = Namespace("base")
    plugins = Namespace("plugins")
    local = Namespace("local")

    base.register("foo", 123)
    plugins.register("bar", 456)
    local.register("baz", 789)

    composite = CompositeNamespace(base, plugins, local)

    paths = composite.list()
    assert "foo" in paths
    assert "bar" in paths
    assert "baz" in paths

def test_composite_setitem():
    base = Namespace("base")
    plugins = Namespace("plugins")
    local = Namespace("local")

    composite = CompositeNamespace(base, plugins, local)
    composite.set_write_target(local)
    composite["new_item"] = 999

    # Add logging to check if the item is in the local namespace
    print(f"Items in local namespace: {local.list()}")

    assert local.resolve("new_item") == 999

def test_composite_unregister():
    base = Namespace("base")
    plugins = Namespace("plugins")
    local = Namespace("local")

    base.register("foo", 123)
    plugins.register("bar", 456)
    local.register("baz", 789)

    composite = CompositeNamespace(base, plugins, local)
    composite.unregister("foo")

    with pytest.raises(KeyError):
        base.resolve("foo")

def test_composite_add_namespace():
    base = Namespace("base")
    plugins = Namespace("plugins")
    local = Namespace("local")
    extra = Namespace("extra")

    composite = CompositeNamespace(base, plugins, local)
    composite.add_namespace(extra)

    extra.register("extra_item", 111)
    assert composite.resolve("extra_item") == 111

def test_composite_set_write_target():
    base = Namespace("base")
    plugins = Namespace("plugins")
    local = Namespace("local")

    composite = CompositeNamespace(base, plugins, local)
    composite.set_write_target(plugins)
    composite["new_item"] = 999

    assert plugins.resolve("new_item") == 999