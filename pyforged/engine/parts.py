from abc import ABC


class BaseEnginePart(ABC):  # TODO: Relocate to bases
    pass

class EnginePart(BaseEnginePart):
    pass

class UniqueCarPart(EnginePart):  # TODO: make a dynamic singleton?
    pass

class Engine:  # TODO: Make singleton?
    """

    """

    def __init__(self):
        self._components = []

    def add_part(self, part: BaseEnginePart) -> None:
        self._components.append(part)
