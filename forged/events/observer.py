from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass

import threading

class Subject:
    def __init__(self, name: str):
        self._name = name
        self._observers = []
        self._lock = threading.Lock()

    def attach(self, observer: Observer) -> None:
        with self._lock:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        with self._lock:
            self._observers.remove(observer)

    def notify(self, message: str) -> None:
        with self._lock:
            observers_snapshot = list(self._observers)
        for observer in observers_snapshot:
            observer.update(self, message)

    @property
    def name(self) -> str:
        return self._name

class ConcreteObserver(Observer):
    def __init__(self, name: str):
        self._name = name

    def update(self, subject: Subject, message: str) -> None:
        print(f"{self._name} received message from {subject.name}: {message}")


if __name__ == '__main__':
    subject1 = Subject("Subject 1")
    subject2 = Subject("Subject 2")

    observer1 = ConcreteObserver("Observer 1")
    observer2 = ConcreteObserver("Observer 2")

    subject1.attach(observer1)
    subject1.attach(observer2)
    subject2.attach(observer1)

    subject1.notify("Message for Subject 1")
    subject2.notify("Message for Subject 2")

    subject1.detach(observer1)

    subject1.notify("Observer 1 has been detached from Subject 1")
    subject2.notify("Observer 1 is still attached to Subject 2")