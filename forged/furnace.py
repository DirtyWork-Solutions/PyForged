"""

"""
from platform import system

from forged.namespacing.tree import print_namespace
from pyforged.ecosystem.bases import PyForgeProjectRegistry
from pyforged.ecosystem.forest import ForgedEcosystem
from forged.namespacing.core.namespace import Namespace
from forged.namespacing.core.decorators import register
from pyforged.services import ServiceRegistry

GLOBAL_NAMESPACES = Namespace(name='globe')

GLOBAL_NAMESPACES.register("testing.hello", 123)

print(GLOBAL_NAMESPACES.to_dict())

