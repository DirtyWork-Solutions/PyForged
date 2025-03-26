"""
A lightweight abstraction layer for managing signals (events) and reactive streams, allowing you to plug in different
backends like PyDispatcher and RxPy under a unified interface
"""
from forged.elements.events.core.actions import Action
from forged.elements.events.core.activities import Activity

__all__ = ["Action", "Activity"]
