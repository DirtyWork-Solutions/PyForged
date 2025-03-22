from abc import ABC, abstractmethod


class BaseActivity(ABC):

    @abstractmethod
    def __init__(self, conf: dict = None, conf_allow_new: bool = True):
        self.name = 'unknown'
        # Setup conf
        self._conf = {
            "reporting": {
                "logging": {
                    "enabled": True
                }
            },
            "announcing": {
                "enabled": True
            }
        }
        if conf:
            self._conf.update(conf)

class Activity(BaseActivity, ABC):
    _default_conf = {
        "auditing": {},
        "hooking": []
    }
    def __init__(self, conf=None):
        super().__init__(conf=conf)



