from pydispatch import dispatcher

class PyDispatcherAction:
    def __init__(self, name):
        self.name = name

    def emit(self, *args, **kwargs):
        dispatcher.send(signal=self.name, sender=self, **kwargs)

    def connect(self, handler):
        dispatcher.connect(handler, signal=self.name, sender=dispatcher.Any)

    def disconnect(self, handler):
        dispatcher.disconnect(handler, signal=self.name)