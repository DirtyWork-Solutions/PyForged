"""

"""

import threading
import os
import platform

#
if platform.system() == 'Windows':  # TODO: Move this
    import msvcrt
else:
    import fcntl


#
class ProcessLock:
    """
    Implements a file-based lock for process safety.

    **Note:** This uses *fcntl* in Unix based systems. For Windows systems, *msvcrt* is used.
    """
    def __init__(self, lock_file):
        self.lock_file = lock_file
        self._file_handle = None

    def acquire(self):
        try:
            self._file_handle = open(self.lock_file, 'w')
            if platform.system() == 'Windows':
                msvcrt.locking(self._file_handle.fileno(), msvcrt.LK_LOCK, 1)
            else:
                fcntl.flock(self._file_handle, fcntl.LOCK_EX)
        except:
            if self._file_handle:
                self._file_handle.close()
            raise

    def release(self):
        if self._file_handle:
            if platform.system() == 'Windows':
                msvcrt.locking(self._file_handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(self._file_handle, fcntl.LOCK_UN)
            self._file_handle.close()
            self._file_handle = None


#
class DistributedLock:
    def __init__(self, key):
        self.key = key
        self._lock = threading.Lock()

    def acquire(self):
        self._lock.acquire()

    def release(self):
        self._lock.release()


# Example usage:
if __name__ == "__main__":
    file_lock = ProcessLock("myapp.lock")
    file_lock.acquire()
    try:
        print("File lock acquired. Do critical work here.")
    finally:
        file_lock.release()

    dist_lock = DistributedLock("resource_key")
    dist_lock.acquire()
    try:
        print("Distributed lock (stub) acquired.")
    finally:
        dist_lock.release()