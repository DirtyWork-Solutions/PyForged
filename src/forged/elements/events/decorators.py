from forged.elements.events.registry import get_action, get_activity

def on_action(name):
    """
    Decorator to connect a function to an Action by name.
    """
    def decorator(func):
        action = get_action(name)
        if action is None:
            raise ValueError(f"Action '{name}' not found in registry.")
        action.connect(func)
        return func
    return decorator

def on_activity(name, pipe=None):
    """
    Decorator to subscribe a function to an Activity by name.
    Optionally applies a pipe (list of Rx operators).
    """
    def decorator(func):
        activity = get_activity(name)
        if activity is None:
            raise ValueError(f"Activity '{name}' not found in registry.")
        stream = activity.pipe(*pipe) if pipe else activity
        stream.subscribe(func)
        return func
    return decorator