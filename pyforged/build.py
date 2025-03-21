"""

"""

from pyforged.namespaces import NamespaceManager
from pyforged.services import ServiceRegistry

# Defaults, templates and
_BUILD_TEMPLATE = {
    "name": "MyApp",
    "version": "1.0.0",
    "authors": ['DirtyWork Solutions Limited'],
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