from abc import ABC


class PyForgedBase:
    pass

# TODO: add module hooks
class BaseNamespaceItem(ABC, PyForgedBase):
    def __init__(self, name: str = 'default_name'):
        self.name = name
        self.value = None

    pass


class BaseNamespace(ABC, PyForgedBase):
    def __init__(self, ns_name: str = 'root'):
        self.name = ns_name