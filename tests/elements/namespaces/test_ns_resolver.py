import pytest
from forged.elements.namespaces.core.resolver import Resolver
from forged.elements.namespaces.core.nodes import NamespaceNode
from forged.elements.namespaces.core.items import Entry

def test_handle_conflict_replace():
    resolver = Resolver()
    resolver.conflict_mode = "replace"
    node = NamespaceNode("test")
    node.entry = Entry(value="original")
    resolver.handle_conflict(node, "new_value", "test.path")
    assert node.entry.value == "new_value"

def test_handle_conflict_chain():
    resolver = Resolver()
    resolver.conflict_mode = "chain"
    node = NamespaceNode("test")
    node.entry = Entry(value=lambda x: x + 1)
    resolver.handle_conflict(node, lambda x: x * 2, "test.path")
    assert callable(node.entry.value)
    assert node.entry.value(2) == 4

def test_handle_conflict_soft():
    resolver = Resolver()
    resolver.conflict_mode = "soft"
    node = NamespaceNode("test")
    node.entry = Entry(value="original")
    resolver.handle_conflict(node, "new_value", "test.path")
    assert node.entry.value == "original"

def test_handle_conflict_strict():
    resolver = Resolver()
    resolver.conflict_mode = "strict"
    node = NamespaceNode("test")
    node.entry = Entry(value="original")
    with pytest.raises(ValueError):
        resolver.handle_conflict(node, "new_value", "test.path")

def test_bind_lazy():
    resolver = Resolver()
    resolver.bind_lazy("test.path", lambda: "lazy_value")
    assert resolver.has_lazy("test.path")

def test_load_lazy():
    resolver = Resolver()
    resolver.bind_lazy("test.path", lambda: "lazy_value")
    entry = resolver.load_lazy("test.path")
    assert entry.value == "lazy_value"

def test_match_pattern():
    resolver = Resolver()
    root = NamespaceNode("")  # unnamed root
    parent = root.add_child("root")
    child = parent.add_child("child")
    child.entry = Entry(value="child_value")

    print("DEBUG: parent.children =", list(parent.children.keys()))
    print("DEBUG: root.children =", list(root.children.keys()))

    print("DEBUG: child is", parent.get_child("child"))
    print("DEBUG: parent.children['child'] =", parent.children["child"])

    results = resolver.match_pattern(root, "root.child")

    print("DEBUG: match results =", results)

    print("child is:", child)
    print("parent.children['child'] is:", parent.children["child"])
    print("parent.get_child('child') is:", parent.get_child("child"))
    print("child.entry:", child.entry)

    print("DEBUG: parent id:", id(parent))
    print("DEBUG: child id:", id(child))

    assert len(results) == 1