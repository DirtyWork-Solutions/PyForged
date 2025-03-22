from abc import ABC, abstractmethod
from uuid import UUID

from forged._old.utilities.assorted import get_new_id


class BaseJob(ABC):
    """
    Abstract base class for 'Job'
    """

    @abstractmethod
    def __init__(self,
                 unique_id: str | UUID | None,
                 label: str | None
                 ):
        """

        """
        # Set the metadata
        self._meta = {
            "uid": get_new_id(unique_id),
            "label": label if label else 'new job'
        }

    @property
    def metadata(self) -> dict:
        """

        """
        return self._meta

    @property
    def label(self):
        return self._meta["label"]

    @abstractmethod
    def name(self):
        return self.label

