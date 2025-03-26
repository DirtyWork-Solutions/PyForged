"""

"""
from forged._old.services import ServiceRegistry
from forged.namespacing import Namespace, CompositeNamespace

_anvil_ns = Namespace("anvil")

global_namespace = CompositeNamespace()

# anvil_ns.unregister('testing')
print(_anvil_ns.to_dict(exclude_root=True))

global_namespace.add_layer(_anvil_ns)

print(global_namespace)