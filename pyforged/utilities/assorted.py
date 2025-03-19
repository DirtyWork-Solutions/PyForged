from typing import List
from uuid import UUID, uuid4


def get_new_id(use_this: str | UUID | None = None) -> str:
    """


    :param use_this:

    :returns: string of the validated/generated UUID
    :raises:
    """

    if use_this is not None:
        try:
            validated = UUID(use_this)
            return str(validated)
        except Exception as e:
            # TODO: Log error handle action here
            return str(uuid4())
    # N
    else:
        return str(uuid4())

