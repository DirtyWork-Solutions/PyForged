"""
This module implements the Observer design pattern. It includes the following classes:
- Observer: An abstract base class for observers.
- Subject: A class that maintains a list of observers and notifies them of any changes.
- ConcreteObserver: A concrete implementation of the Observer class.

Classes:
    Observer(ABC): An abstract base class for observers.
    Subject: A class that maintains a list of observers and notifies them of any changes.
    ConcreteObserver: A concrete implementation of the Observer class.

Usage:
    subject1 = Subject("Subject 1")
    observer1 = ConcreteObserver("Observer 1", "Subject 1")
    subject1.attach(observer1)
    subject1.notify("Message for Subject 1")
"""

from abc import ABC, abstractmethod
import threading
import heapq
from weakref import WeakSet

class Observer(ABC):
    """
    Abstract base class for observers.

    Methods:
        update(subject: Subject, message: str) -> None:
            Abstract method to update the observer with a message from the subject.
        is_interested(message: str) -> bool:
            Abstract method to check if the observer is interested in the message.
    """
    @abstractmethod
    def update(self, subject: 'Subject', message: str) -> None:
        pass

    @abstractmethod
    def is_interested(self, message: str) -> bool:
        pass

class Subject:
    """
    A class that maintains a list of observers and notifies them of any changes.

    Attributes:
        _name (str): The name of the subject.
        _observers (list): A list of observers sorted by priority.
        _active_observers (WeakSet): A set of active observers.
        _lock (threading.Lock): A lock to ensure thread safety.

    Methods:
        attach(observer: Observer, priority: int = 0) -> None:
            Attach an observer to the subject with an optional priority.
        detach(observer: Observer) -> None:
            Detach an observer from the subject.
        notify(message: str) -> None:
            Notify all interested observers with a message.
        name() -> str:
            Get the name of the subject.
    """
    def __init__(self, name: str):
        self._name = name
        self._observers = []
        self._active_observers = WeakSet()
        self._lock = threading.Lock()

    def attach(self, observer: Observer, priority: int = 0) -> None:
        """
        Attach an observer to the subject with an optional priority.

        Args:
            observer (Observer): The observer to attach.
            priority (int, optional): The priority of the observer. Defaults to 0.
        """
        with self._lock:
            heapq.heappush(self._observers, (-priority, observer))
            self._active_observers.add(observer)

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.

        Args:
            observer (Observer): The observer to detach.
        """
        with self._lock:
            self._active_observers.discard(observer)
            self._observers = [(p, o) for p, o in self._observers if o in self._active_observers]
            heapq.heapify(self._observers)

    def notify(self, message: str) -> None:
        """
        Notify all interested observers with a message.

        Args:
            message (str): The message to notify observers with.
        """
        with self._lock:
            observers_snapshot = list(self._observers)
        for _, observer in observers_snapshot:
            if observer.is_interested(message):
                observer.update(self, message)

    @property
    def name(self) -> str:
        """
        Get the name of the subject.

        Returns:
            str: The name of the subject.
        """
        return self._name

class ConcreteObserver(Observer):
    """
    A concrete implementation of the Observer class.

    Attributes:
        _name (str): The name of the observer.
        _interested_in (str): The message the observer is interested in.

    Methods:
        update(subject: Subject, message: str) -> None:
            Update the observer with a message from the subject.
        is_interested(message: str) -> bool:
            Check if the observer is interested in the message.
        __lt__(other: 'ConcreteObserver') -> bool:
            Compare two observers based on their names.
    """
    def __init__(self, name: str, interested_in: str):
        self._name = name
        self._interested_in = interested_in

    def update(self, subject: Subject, message: str) -> None:
        """
        Update the observer with a message from the subject.

        Args:
            subject (Subject): The subject sending the message.
            message (str): The message from the subject.
        """
        print(f"{self._name} received message from {subject.name}: {message}")

    def is_interested(self, message: str) -> bool:
        """
        Check if the observer is interested in the message.

        Args:
            message (str): The message to check.

        Returns:
            bool: True if the observer is interested in the message, False otherwise.
        """
        return self._interested_in in message

    def __lt__(self, other: 'ConcreteObserver') -> bool:
        """
        Compare two observers based on their names.

        Args:
            other (ConcreteObserver): The other observer to compare with.

        Returns:
            bool: True if this observer's name is less than the other observer's name, False otherwise.
        """
        return self._name < other._name

if __name__ == '__main__':
    subject1 = Subject("Subject 1")
    subject2 = Subject("Subject 2")

    observer1 = ConcreteObserver("Observer 1", "Subject 1")
    observer2 = ConcreteObserver("Observer 2", "Subject 2")

    subject1.attach(observer1)
    subject1.attach(observer2)
    subject2.attach(observer1)

    subject1.notify("Message for Subject 1")
    subject2.notify("Message for Subject 2")

    subject1.detach(observer1)

    subject1.notify("Observer 1 has been detached from Subject 1")
    subject2.notify("Observer 1 is still attached to Subject 2")