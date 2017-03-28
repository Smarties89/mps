from uuid import uuid4
import json
import os
import logging

log = logging.getLogger(__name__)

class ErrorRecoveryFile(object):
    def __init__(self, save_path, data):
        self.save_path = save_path 
        self.data = data
        self.dataid = str(uuid4())
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
