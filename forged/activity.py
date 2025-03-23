from abc import ABC, abstractmethod


class BaseActivity(ABC):

    @abstractmethod
    def __init__(self, conf: dict = None):
        self.name = 'unknown'
        # Setup conf
        self._conf = {}
        if conf:
            self._conf.update(conf)

class Activity(BaseActivity, ABC):
    _default_conf = {
        "auditing": {},
        "hooking": []
    }
    def __init__(self, conf=None):
        super().__init__(conf=conf)



