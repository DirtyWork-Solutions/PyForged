import asyncio
import pytest
from forged.events.dispatcher import send, async_send, threaded_send, get_receivers, get_all_receivers, connections
from forged.events.filters import EventFilter, EventFilterManager
from forged.events.middleware import MiddlewareManager

@pytest.fixture
def event_filter_manager():
    return EventFilterManager()

@pytest.fixture
def middleware_manager():
    return MiddlewareManager()

def test_event_filter(event_filter_manager):
    def condition(signal, sender, **kwargs):
        return signal == "test_signal"

    event_filter = EventFilter(condition)
    event_filter_manager.add_filter(event_filter)
    assert event_filter_manager.apply_filters("test_signal", "sender")
    assert not event_filter_manager.apply_filters("other_signal", "sender")

def test_middleware(middleware_manager):
    def middleware(signal, sender, **kwargs):
        return signal + "_modified", sender, kwargs

    middleware_manager.add_middleware(middleware)
    signal, sender, kwargs = middleware_manager.process("test_signal", "sender")
    assert signal == "test_signal_modified"

def test_send():
    def receiver(signal, sender, *args, **kwargs):
        return "Received"

    connections[id(None)] = {"Test message": [receiver]}
    # Debug: Check registered receivers before sending
    print("Registered receivers before send:", list(get_all_receivers(None, "Test message")))
    responses = asyncio.run(send("Test message", None))
    print("Responses:", responses)
    assert len(responses) > 0


def test_threaded_send():
    def receiver(signal, sender, *args, **kwargs):
        return "Received"

    connections[id(None)] = {"Test message": [receiver]}
    print("Registered receivers before threaded send:", list(get_all_receivers(None, "Test message")))
    print("Connections:", connections)
    responses = threaded_send("Test message", None)
    print("Responses:", responses)
    if not responses:
        print("No responses received. Check if threaded_send is correctly implemented and receivers are properly registered.")
    assert len(responses) > 0

def test_get_receivers():

    def receiver(signal, sender, *args, **kwargs):
        return "Received"

    connections[id(None)] = {"Test message": [receiver]}
    # Debug: Check registered receivers
    receivers = get_receivers(None, "Test message")
    print("Receivers:", receivers)
    assert len(receivers) > 0

def test_get_all_receivers():
    def receiver(signal, sender, *args, **kwargs):
        return "Received"

    connections[id(None)] = {"Test message": [receiver]}
    # Debug: Check registered receivers
    receivers = list(get_all_receivers(None, "Test message"))
    print("All Receivers:", receivers)
    assert len(receivers) > 0

@pytest.mark.asyncio
async def test_async_send():
    responses = await async_send("Test message", None)
    assert len(responses) > 0

from forged.events.library import add_to_library, get_from_library, update_library_event, remove_from_library, list_library_events

@pytest.fixture
def setup_library():
    # Setup code to initialize the library
    add_to_library('event1', 'value1', {'description': 'This is event 1'})
    yield
    # Teardown code to clean up the library
    remove_from_library('event1')

def test_add_to_library(setup_library):
    assert get_from_library('event1') == 'value1'

def test_get_from_library(setup_library):
    assert get_from_library('event1') == 'value1'
    assert get_from_library('non_existent_event') is None

def test_update_library_event(setup_library):
    update_library_event('event1', 'new_value1', {'description': 'Updated event 1'})
    assert get_from_library('event1') == 'new_value1'

def test_remove_from_library(setup_library):
    remove_from_library('event1')
    assert get_from_library('event1') is None

def test_list_library_events(setup_library):
    events = list_library_events()
    assert 'event1' in events
    assert 'non_existent_event' not in events