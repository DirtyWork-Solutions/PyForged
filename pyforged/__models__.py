
#
try:
    from pydantic import BaseModel
except ModuleNotFoundError as e:  # TODO: Log missing pydantic
    pass