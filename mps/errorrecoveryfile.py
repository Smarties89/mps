import json
import os
import logging
import string
import random
from datetime import datetime

log = logging.getLogger(__name__)


# Slighty modified version of
# http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
def randstr(n):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(n))


class ErrorRecoveryFile(object):
    def __init__(self, save_path, data, prefix=None):
        self.save_path = save_path 
        self.data = data
        if prefix is None:
            prefix = ""

        self.dataid = prefix
        self.dataid += datetime.now().strftime("%y_%m_%d_%H_%M")
        self.dataid += "__" + randstr(6)
        self._status = 'inprogress'
        self.current = self._new_current(self._status)
        with open(self.current, "w") as f:
            f.write(json.dumps(self.data))

    def get_status(self):
        return self._status
    
    def set_status(self, value):
        new_status = value
        if new_status is None or self.current is None:
            log.error(u"Tried to move {} to {} for {}, but can't be None".
                format(self.current, new_status, self.dataid))
            return
        self._status = new_status
        new_current = self._new_current(new_status)
        os.rename(self.current, new_current)
        self.current = new_current

    def _new_current(self, new_status):
        return os.path.join(
            self.save_path, new_status + '_' + self.dataid + ".json")

    def remove(self):
        if self.current is None:
            log.warning(u"remove called twice for {}".format(self.dataid))
            return
        os.remove(self.current)
        self.current = None
    
    status = property(get_status, set_status)
