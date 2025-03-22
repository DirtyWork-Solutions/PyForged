# from bedrocked.reporting.reported import logger
import logging as logger

from forged.namespacing import Namespace
from forged.namespacing.core.resolver import Resolver

# A basic registry for hooks: {hook_name: [(priority, hook, enabled, dependencies), ...]}
_hook_registry = {}

def register_hook(name: str, hook, priority: int = 10, enabled: bool = True, dependencies: list = None, tags: list = None):
    """
    Registers a hook under a given name.
    - `dependencies` is a list of hook names that must run before this hook.
    """
    dependencies = dependencies or []
    tags = tags or []
    _hook_registry.setdefault(name, []).append((priority, hook, enabled, dependencies))
    # Sort hooks by priority.
    _hook_registry[name].sort(key=lambda tup: tup[0])

def unregister_hook(name: str, hook):
    if name in _hook_registry:
        logger.info(f"Hook found: {name}")
        _hook_registry[name] = [entry for entry in _hook_registry[name] if entry[1] != hook]
        logger.info(f"{name} was unregistered.")
    else:
        logger.error("Hook '{name}' was not found in the registry. Couldn't unregister the hook.")

def get_registered_hooks(name: str):
    return [entry for entry in _hook_registry.get(name, []) if entry[2]]  # Only enabled hooks


# - - - - - -- - - - - -
# Assuming Namespace and Symbol classes are already defined

# Create a namespace instance
hook_namespace = Namespace(name="hooks")

# Register a hook
def my_hook(*args, **kwargs):
    print("Hook executed with args:", args, "and kwargs:", kwargs)

hook_namespace.register("my_namespace.my_hook", my_hook)

# Resolve and execute the hook
resolved_hook = hook_namespace.resolve("my_namespace.my_hook")
resolved_hook("arg1", key="value")
# Assuming Resolver class is already defined

# Create a resolver instance
resolver = Resolver()

# Define a lazy loader function
def lazy_loader():
    def lazy_hook(*args, **kwargs):
        print("Lazy hook executed with args:", args, "and kwargs:", kwargs)
    return lazy_hook

# Bind the lazy loader to a path
resolver.bind_lazy("my_namespace.lazy_hook", lazy_loader)

# Load and execute the hook lazily
lazy_hook_symbol = resolver.load_lazy("my_namespace.lazy_hook")
lazy_hook = lazy_hook_symbol.value
lazy_hook("arg1", key="value")