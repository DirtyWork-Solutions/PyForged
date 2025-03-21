import logging
from abc import ABC


#
class BaseForgeProject(ABC):
    def __init__(self):
        self._meta = {
            "name": "unknown",
            "latest_version": "unknown",
            "all_versions": [],
            "conf_profiles": {
                "dev": None,
                "test": None,
                "prod": None
            },
        }
        self._dependencies = []


    def add_dependency(self):
        pass

    def remove_dependency(self):
        pass

    def update_dependency(self):
        pass

    def clear_dependencies(self):
        self._dependencies = []
        logging.info(f"")

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def metadata(self) -> dict:
        return self._meta

    @property
    def label(self):
        return self._meta["name"].capitalize()

    @property
    def current_version(self):
        return self._meta["version"]

    @property
    def all_versions(self):
        return self._meta["all_versions"]

    def update_latest_version(self, version_no, date_of_release):
        old = self.current_version
        try:
            self._meta["latest_version"] = version_no
            self._meta["all_versions"].append(self.current_version)
        except Exception as e:
            print(e)


#
class BaseTask(ABC):
    pass


#
class BaseQueue(ABC):
    pass