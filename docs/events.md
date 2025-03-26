# Events System

## Quick Start

```python
from eventual import Action, Activity
from eventual.core.context import scoped_context

# Create an action
user_logged_in = Action("user_logged_in")

# Create a reactive activity from that action
activity = Activity(user_logged_in)

# React to the stream
with scoped_context() as ctx:
    activity.subscribe(lambda event: print("Activity got:", event), ctx=ctx)

    # Emit an event
    user_logged_in.emit(username="alice")
```
Expected Output
```
Activity got: ((), {'username': 'alice'})
```

- - - 
## Core Concepts

### 🟢 ``Action``

Represents a named event or signal. Use it to **emit** events and connect **handlers** to respond to them.

```python
action = Action("my_event")

def on_event(data):
    print("Got:", data)

action.connect(on_event)
action.emit(data="Hello!")
```

- - -
### 🔵 ``Activity``
Represents a **reactive stream** of events originating from an **Action**. Backed by *RxPy* (or any stream backend).


- - -
### 🔌 Backends
You can configure different backends for Action and Activity.

```python
from eventual.config import set_backend

set_backend(action="pydispatcher", activity="rxpy")
```

Supported backends:

- **Actions**: "pydispatcher"
- **Activities**: "rxpy"

Custom backends can be added by extending the interfaces in ``types.py``.

- - -
### 🧼 Context Management
Every ``.connect()`` or ``.subscribe()`` can be optionally tied to a Context, which handles **auto-cleanup**.

```python
from eventual.core.context import scoped_context

with scoped_context() as ctx:
    action.connect(handler, ctx=ctx)
    activity.subscribe(callback, ctx=ctx)

# When the context exits, connections and subscriptions are cleaned up.
```

- - -
### 📚 Registry & Introspection
Track and retrieve actions or activities by name:

```python
from eventual.registry import get_action, get_activity, list_actions

list_actions()        # ['my_event']
get_action("my_event")  # → Action instance
```

- - - 
### 