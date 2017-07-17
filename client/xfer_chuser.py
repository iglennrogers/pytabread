import uuid
import base64


class XferChangeUser:
    def __init__(self, doc=None):
        if doc:
            self.from_dict(doc)
        else:
            self._name = ""
            self._password_hash = ""
        self.dirty = False
        self.password = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        if n != self._name:
            self._name = n
            self.dirty = True

    @property
    def password(self):
        return "********"

    @property
    def password_hash(self):
        return self._password_hash

    @password.setter
    def password(self, pwd):
        ph = base64.encodebytes((self._name + ":" + pwd).encode()).decode()
        if ph != self._password_hash:
            self._password_hash = ph
            self.dirty = True

    def to_dict(self):
        doc = {"name": self._name, "password_hash": self._password_hash}
        return doc

    def from_dict(self, doc):
        self._name = doc["name"]
        self._password_hash = doc["password_hash"]

    def __repr__(self):
        return "<User Data(user='%s', hash='%s')>" % (self._name, self._password_hash)
