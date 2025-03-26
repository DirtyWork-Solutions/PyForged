import pytest
from forged.elements.namespaces.core.items import Entry

def test_entry_initialization():
    entry = Entry(value="test_value", name="test_name", tags={"tag1": "value1"}, metadata={"meta1": "value1"})
    assert entry.value == "test_value"
    assert entry.name == "test_name"
    assert entry.tags == {"tag1": "value1"}
    assert entry.get_metadata("meta1") == "value1"

def test_entry_default_name():
    entry = Entry(value="test_value")
    assert entry.name == "test_value"

def test_entry_freeze_unfreeze():
    entry = Entry(value="test_value")
    entry.freeze()
    assert entry.is_frozen() is True
    entry.unfreeze()
    assert entry.is_frozen() is False

def test_entry_update_metadata():
    entry = Entry(value="test_value")
    assert entry.get_metadata("meta1") is None
    entry.metadata["meta1"] = "value1"
    assert entry.get_metadata("meta1") == "value1"


def test_entry_equality():
    entry1 = Entry(value="test_value", name="test_name")
    entry2 = Entry(value="test_value", name="test_name")
    entry3 = Entry(value="different_value", name="test_name")
    assert entry1 == entry2
    assert entry1 != entry3

def test_entry_hash():
    entry1 = Entry(value="test_value", name="test_name")
    entry2 = Entry(value="test_value", name="test_name")
    assert hash(entry1) == hash(entry2)

def test_entry_str_repr():
    entry = Entry(value="test_value", name="test_name", tags={"tag1": "value1"})
    assert str(entry) == "NamespaceItem(name=test_name, value=test_value)"
    assert repr(entry) == "<NamespaceItem name=test_name frozen=False tags={'tag1': 'value1'}>"