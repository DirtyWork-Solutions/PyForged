import json
import os
import yaml
import xml.etree.ElementTree as ET
from loguru import logger
from typing import Dict
from functools import lru_cache
import re

@lru_cache(maxsize=32)
def load_hook_config(file_path: str) -> Dict:
    """
    Load hook configuration from a JSON, YAML, or XML file.

    :param file_path: Path to the configuration file.
    :return: Configuration as a dictionary.
    :raises ValueError: If the file format is unsupported.
    :raises FileNotFoundError: If the file does not exist.
    :raises IOError: If there is an error reading the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    supported_extensions = {".yaml", ".yml", ".json", ".xml"}

    if ext not in supported_extensions:
        raise ValueError(f"Unsupported configuration file format: '{ext}'")

    try:
        with open(file_path, "r") as f:  # TODO: Use commons tools for opening file
            if ext in {".yaml", ".yml"}:
                config = yaml.safe_load(f)
            elif ext == ".json":
                config = json.load(f)
            elif ext == ".xml":
                tree = ET.parse(f)
                config = {elem.tag: elem.text for elem in tree.iter()}
    except IOError as e:
        logger.error(f"Error reading configuration file '{file_path}': {e}")
        raise

    config = _substitute_env_vars(config)
    logger.success(f"Configuration loaded successfully from '{file_path}'")
    return config  # TODO: Integrate with native-conf system

def _substitute_env_vars(config: Dict) -> Dict:
    """
    Substitute environment variables in the configuration.

    :param config: Configuration dictionary.
    :return: Configuration dictionary with environment variables substituted.
    """
    pattern = re.compile(r'\$\{(\w+)\}')

    def replace_env_vars(value):
        if isinstance(value, str):
            return pattern.sub(lambda match: os.getenv(match.group(1), match.group(0)), value)
        elif isinstance(value, dict):
            return {k: replace_env_vars(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [replace_env_vars(v) for v in value]
        else:
            return value

    return replace_env_vars(config)