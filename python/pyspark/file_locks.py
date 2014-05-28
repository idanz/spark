import os
import fcntl
import logging
import tempfile
import hashlib
logger = logging.getLogger('filelock')

class FileLock(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'FileLock({}, {})'.format(self.name, self._path)

    @property
    def _path(self):
        return os.path.join(tempfile.gettempdir(), 'filelock-{}.lock'.format(hashlib.md5(self.name).hexdigest()))

    def acquire(self, blocking = True):
        self.fp = open(self._path, 'w')
        try:
            flags = fcntl.LOCK_EX
            if not blocking:
                flags |= fcntl.LOCK_NB
            fcntl.lockf(self.fp, flags)
        except IOError:
            return False
        self.fp.write(str(os.getpid()))

    def release(self):
        if not self.fp:
            raise Exception('No file descriptor, probably not acquired')
        self.fp.close()

    __enter__ = acquire

    def __exit__(self, t, v, tb):
        self.release()

    def __call__(self, func): # For use as a decorator
        @wraps(func)
        def wrapper(*a, **kw):
            with self:
                return func(*a, **kw)

        return wrapper


TEST_LOCK_NAME = 'test'
if __name__ == '__main__':
    import time
    start_time = time.time()
    with FileLock(TEST_LOCK_NAME):
        end_time = time.time()
    print end_time-start_time