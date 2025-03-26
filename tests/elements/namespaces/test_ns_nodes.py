
from forged.elements.namespaces.core.nodes import NamespaceNode

def test_add_child():
    root = NamespaceNode("root")
    child = root.add_child("child")
    assert child.name == "child"
    assert root.get_child("child") == child

def test_get_child():
    root = NamespaceNode("root")
    root.add_child("child")
    assert root.get_child("child").name == "child"
    assert root.get_child("nonexistent") is None

def test_remove_child():
    root = NamespaceNode("root")
    root.add_child("child")
    assert root.remove_child("child") is True
    assert root.get_child("child") is None
    assert root.remove_child("nonexistent") is False

def test_has_child():
    root = NamespaceNode("root")
    root.add_child("child")
    assert root.has_child("child") is True
    assert root.has_child("nonexistent") is False

def test_find_node_by_path():
    root = NamespaceNode("root")
    child = root.add_child("child")
    grandchild = child.add_child("grandchild")
    assert root.find_node_by_path("child.grandchild") == grandchild
    assert root.find_node_by_path("child.nonexistent") is None

def test_equality():
    node1 = NamespaceNode("node")
    node2 = NamespaceNode("node")
    assert node1 == node2
    node1.add_child("child")
    assert node1 != node2

def test_len():
    root = NamespaceNode("root")
    assert len(root) == 0
    root.add_child("child")
    assert len(root) == 1

def test_iter():
    root = NamespaceNode("root")
    child = root.add_child("child")
    assert list(iter(root)) == [child]

def test_repr():
    root = NamespaceNode("root")
    assert "NamespaceNode name=root" in repr(root)
    root.add_child("child")
    assert "child" in repr(root)

def test_dot_access_with_children():
    root = NamespaceNode("root")
    root.add_child("level1").add_child("level2")
    assert root.children.level1.children.level2.name == "level2"


def test_node_equality_with_children():
    node1 = NamespaceNode("foo")
    node2 = NamespaceNode("foo")
    node1.add_child("bar")
    node2.add_child("bar")
    assert node1 == node2
