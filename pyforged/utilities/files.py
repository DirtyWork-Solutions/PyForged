import asyncio
import json
import os
import tempfile
import time
import xml.etree.ElementTree as ET
from contextlib import contextmanager
from pathlib import Path
from typing import Optional
import yaml


@contextmanager
def atomic_write(file_path):
    temp_path = file_path + ".tmp"
    with open(temp_path, 'w') as temp_file:
        yield temp_file
    os.replace(temp_path, file_path)

# 1. Efficient Large File Reader
def read_large_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()


# 2. JSON/YAML/XML Serializer
def serialize_json(obj):
    return json.dumps(obj, indent=2)

def serialize_yaml(obj):
    return yaml.dump(obj)

def serialize_xml(obj):
    root = ET.Element("root")
    for k, v in obj.items():
        child = ET.SubElement(root, k)
        child.text = str(v)
    return ET.tostring(root, encoding='unicode')


# 3. Safe Temporary File Manager
@contextmanager
def temp_file():
    temp = tempfile.NamedTemporaryFile(delete=False)
    try:
        yield temp.name
    finally:
        os.unlink(temp.name)



# 4.
class DirectoryWatcher:
    def __init__(self, directory):
        self.directory = Path(directory)

    async def watch(self, callback):
        before = set(self.directory.iterdir())
        while True:
            await asyncio.sleep(1)
            after = set(self.directory.iterdir())
            changes = after - before
            if changes:
                if asyncio.iscoroutinefunction(callback):
                    await callback(changes)
                else:
                    callback(changes)
            before = after

    def watch_sync(self, callback, interval: Optional[int]):
        pause_secs = interval if interval else 1
        before = set(self.directory.iterdir())
        while True:
            time.sleep(pause_secs)
            after = set(self.directory.iterdir())
            changes = after - before
            if changes:
                callback(changes)
            before = after