import pytest
from forged.elements.namespaces.core.namespace import Namespace
from forged.elements.namespaces.core.items import Entry

def test_register_and_resolve():
    ns = Namespace("root")
    ns.register("a.b.c", "value")
    print(ns.to_dict())
    assert ns.resolve("a.b.c") == "value"

def test_register_with_metadata():
    ns = Namespace("root")
    metadata = {"key": "value"}
    ns.register("a.b.c", "value", metadata=metadata)
    entry = ns.root.get_child("a").get_child("b").get_child("c").entry
    assert entry.value == "value"
    assert entry.metadata == metadata

def test_unregister():
    ns = Namespace("root")
    ns.register("a.b.c", "value")
    ns.unregister("a.b.c")
    with pytest.raises(KeyError):
        ns.resolve("a.b.c")

def test_list():
    ns = Namespace("root")
    ns.register("a.b.c", "value")
    ns.register("a.b.d", "value")
    paths = ns.list("a.b")
    assert "a.b.c" in paths
    assert "a.b.d" in paths

def test_to_dict():
    ns = Namespace("root")
    ns.register("a.b.c", "value")
    ns_dict = ns.to_dict()
    assert ns_dict == {
        "root": {
            "a": {
                "b": {
                    "c": {
                        "__entry__": {
                            "name": "value",
                            "tags": {}
                        }
                    }
                }
            }
        }
    }

def test_from_dict():
    ns = Namespace("root")
    ns_data = {
        "root": {
            "a": {
                "b": {
                    "c": {
                        "__entry__": {
                            "name": "value",
                            "tags": {}
                        }
                    }
                }
            }
        }
    }
    ns.from_dict(ns_data)
    assert ns.resolve("a.b.c") == "value"


def test_lazy_loading():
    ns = Namespace("root")
    ns.resolver.bind_lazy("a.b.c", lambda: "lazy_value")
    assert ns.resolve("a.b.c") == "lazy_value"

def test_contains():
    ns = Namespace("root")
    ns.register("a.b.c", "value")
    assert "a.b.c" in ns
    assert "a.b.d" not in ns

def test_len():
    ns = Namespace("root")
    ns.register("a.b.c", "value")
    ns.register("a.b.d", "value")
    assert len(ns) == 2

from forged.elements.namespaces.aliasing import Aliaser

def test_add_alias():
    aliaser = Aliaser()
    aliaser.add("alias1", "target1")
    assert aliaser.get("alias1") == "target1"

def test_remove_alias():
    aliaser = Aliaser()
    aliaser.add("alias1", "target1")
    aliaser.remove("alias1")
    assert aliaser.get("alias1") == "alias1"

def test_resolve_path():
    aliaser = Aliaser()
    aliaser.add("alias1", "target1")
    assert aliaser.resolve_path("alias1") == "target1"
    assert aliaser.resolve_path("alias1.subpath") == "target1.subpath"
    assert aliaser.resolve_path("nonexistent") == "nonexistent"

def test_all_aliases():
    aliaser = Aliaser()
    aliaser.add("alias1", "target1")
    aliaser.add("alias2", "target2")
    assert aliaser.all() == {"alias1": "target1", "alias2": "target2"}
