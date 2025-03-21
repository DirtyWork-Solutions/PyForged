"""

"""

from forged.namespacing.core.namespace import Namespace

GLOBAL_NAMESPACES = Namespace(name='globe')

GLOBAL_NAMESPACES.register("testing.hello", 123)

print(GLOBAL_NAMESPACES.to_dict())

