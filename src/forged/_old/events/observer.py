from typing import Any, Callable, List, Tuple, Union
from abc import ABC, abstractmethod
import threading
import heapq
from weakref import WeakSet
import asyncio

class Observer(ABC):
    @abstractmethod
    async def update(self, subject: 'Subject', message: str) -> None:
        pass

    @abstractmethod
    def is_interested(self, message: str) -> bool:
        pass

class Subject:
    def __init__(self, name: str):
        self._name = name
        self._observers = []
        self._active_observers = WeakSet()
        self._lock = threading.Lock()

    def attach(self, observer: Observer, priority: int = 0) -> None:
        with self._lock:
            heapq.heappush(self._observers, (-priority, observer))
            self._active_observers.add(observer)

    def detach(self, observer: Observer) -> None:
        with self._lock:
            self._active_observers.discard(observer)
            self._observers = [(p, o) for p, o in self._observers if o in self._active_observers]
            heapq.heapify(self._observers)

    async def notify(self, message: str) -> None:
        with self._lock:
            observers_snapshot = list(self._observers)
        for _, observer in observers_snapshot:
            if observer.is_interested(message):
                if asyncio.iscoroutinefunction(observer.update):
                    await observer.update(self, message)
                else:
                    observer.update(self, message)

    def update_priority(self, observer: Observer, new_priority: int) -> None:
        with self._lock:
            self._observers = [(p, o) for p, o in self._observers if o != observer]
            heapq.heappush(self._observers, (-new_priority, observer))

    @property
    def name(self) -> str:
        return self._name

    def __eq__(self, other: 'Subject') -> bool:
        return self._name == other._name

    def __ne__(self, other: 'Subject') -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f"Subject(name={self._name})"

    def __hash__(self) -> int:
        return hash(self._name)

class ConcreteObserver(Observer):
    def __init__(self, name: str, interested_in: str, active: bool = True):
        self._name = name
        self._interested_in = interested_in
        self._last_message = ""
        self._active = active

    @property
    def last_message(self) -> str:
        return self._last_message

    @last_message.setter
    def last_message(self, value: str) -> None:
        self._last_message = value

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value

    async def update(self, subject: Subject, message: str) -> None:
        self._last_message = message
        print(f"{self._name} received message from {subject.name}: {message}")

    def is_interested(self, message: str) -> bool:
        return self._interested_in in message

    def __lt__(self, other: 'ConcreteObserver') -> bool:
        return self._name < other._name

    def __eq__(self, other: 'ConcreteObserver') -> bool:
        return self._name == other._name

    def __ne__(self, other: 'ConcreteObserver') -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f"ConcreteObserver(name={self._name}, interested_in={self._interested_in})"

    def __hash__(self) -> int:
        return hash((self._name, self._interested_in))

if __name__ == '__main__':
    async def main():
        subject1 = Subject("Subject 1")
        subject2 = Subject("Subject 2")

        observer1 = ConcreteObserver("Observer 1", "Subject 1")
        observer2 = ConcreteObserver("Observer 2", "Subject 2")

        subject1.attach(observer1)
        subject1.attach(observer2)
        subject2.attach(observer1)

        await subject1.notify("Message for Subject 1")
        await subject2.notify("Message for Subject 2")

        subject1.detach(observer1)

        await subject1.notify("Observer 1 has been detached from Subject 1")
        await subject2.notify("Observer 1 is still attached to Subject 2")

    asyncio.run(main())