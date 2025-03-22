from typing import Any
from loguru import logger as log
from forged.namespacing import Namespace

#
_events_ns = Namespace('events')

def add_to_library(event) -> None:
    _events_ns.register(path=event, value=event, metadata={})

def remove_from_library() -> None:
    pass

def get_from_library() -> Any:
    pass

if __name__ == '__main__':
    pass