
from forged.elements.namespaces.utils import (
    split_path,
    join_path,
    is_valid_identifier,
    merge_tags,
    normalize_path,
    filter_paths,
    deep_merge_dicts,
    validate_path
)

def test_split_path():
    assert split_path("a.b.c") == ["a", "b", "c"]
    assert split_path(".a.b.c.") == ["a", "b", "c"]
    assert split_path("") == []


def test_join_path():
    assert join_path(["a", "b", "c"]) == "a.b.c"
    assert join_path(("a", "b", "c")) == "a.b.c"
    assert join_path([]) == ""

def test_is_valid_identifier():
    assert is_valid_identifier("valid_name")
    assert not is_valid_identifier("invalid-name")
    assert not is_valid_identifier("123invalid")

def test_merge_tags():
    assert merge_tags({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert merge_tags({"a": 1}, {"a": 2}) == {"a": 2}
    assert merge_tags() == {}

def test_normalize_path():
    assert normalize_path("a.b.c") == "a.b.c"
    assert normalize_path(".a.b.c.") == "a.b.c"
    assert normalize_path("a..b..c") == "a.b.c"

def test_filter_paths():
    paths = ["a.b.c", "a.b.d", "b.c.d"]
    assert filter_paths(paths, "a.b") == ["a.b.c", "a.b.d"]
    assert filter_paths(paths, "b") == ["b.c.d"]
    assert filter_paths(paths, "c") == []

def test_deep_merge_dicts():
    dict1 = {"a": {"b": 1}}
    dict2 = {"a": {"c": 2}}
    assert deep_merge_dicts(dict1, dict2) == {"a": {"b": 1, "c": 2}}
    dict1 = {"a": 1}
    dict2 = {"b": 2}
    assert deep_merge_dicts(dict1, dict2) == {"a": 1, "b": 2}

def test_validate_path():
    assert validate_path("a.b.c")
    assert not validate_path("a.b.c.")
    assert not validate_path("a..b..c")
    assert not validate_path("a.b.c-")