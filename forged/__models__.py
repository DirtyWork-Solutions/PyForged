from loguru import logger
#
try:
    from pydantic import BaseModel
except ModuleNotFoundError as e:  # TODO: Log missing pydantic
    logger.warning("Pydantic is not installed.")