import uuid
import datetime


class UserDb:
    def __init__(self):
        self._uid = uuid.uuid4()
        self._version = 1
        self._creation_date = datetime.datetime.today()
        self._modification_date = datetime.datetime.today()
        self._deletion_date = None
        self.name = ""
        self.fullname = ""
        self.comments = ""
