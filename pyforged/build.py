"""

"""

from pyforged.namespaces import NamespaceManager
from pyforged.services import ServiceRegistry

# Defaults, templates and
_BUILD_TEMPLATE = {
    "name": "MyApp",
    "version": "1.0.0",
    "author": ['DirtyWork Solutions Limited'],
    "description": "",
    "install": {
        "requirements": [
            "python<3.12"
        ],
        "dependencies": [
            "pyforged~=0.2.6"
        ]
    },
    "namespaces": [  # usually the app name

    ],

}


#

from pyforged.namespaces import NamespaceManager

namespaces = NamespaceManager()

namespaces.set("globals", NamespaceManager())
namespaces.set("forged", NamespaceManager())
namespaces.set("forged.ecosystem.community", NamespaceManager())
print(namespaces.list_all_namespaces())

# print(namespaces.forged)