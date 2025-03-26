import pytest
from forged.elements.events import Action, Activity
from forged.elements.events.core.context import scoped_context
from forged.elements.events.registry import get_action, get_activity, list_actions, list_activities


def test_action_emit_and_connect():
    action = Action("test_event")

    result = {}

    def handler(value):
        result["value"] = value

    action.connect(handler)
    action.emit(value=42)

    assert result["value"] == 42


def test_action_context_cleanup():
    action = Action("context_event")
    result = {}

    def handler(value):
        result["value"] = value

    with scoped_context() as ctx:
        action.connect(handler, ctx=ctx)
        action.emit(value=100)
        assert result["value"] == 100

    result.clear()
    action.emit(value=200)
    assert "value" not in result  # handler should be disconnected


def test_activity_subscribe_and_emit():
    action = Action("stream_event")
    activity = Activity(action)

    captured = []

    def subscriber(data):
        captured.append(data)

    with scoped_context() as ctx:
        activity.subscribe(subscriber, ctx=ctx)
        action.emit(1, key="a")
        action.emit(2, key="b")

        assert captured == [((1,), {"key": "a"}), ((2,), {"key": "b"})]

    captured.clear()
    action.emit(3, key="c")
    assert not captured  # subscription cleaned up


def test_registry_tracking():
    name = "registry_test"
    action = Action(name)
    activity = Activity(action)

    assert get_action(name) is action
    assert get_activity(name) is activity
    assert name in list_actions()
    assert name in list_activities()
