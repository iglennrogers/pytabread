import uuid
import base64


class XferNewProject:
    def __init__(self, doc=None):
        if doc:
            self.load(doc)
        else:
            self._name = "admin"
            self._password_hash = ""
            self.uuid = str(uuid.uuid4())
            self._project_name = ""
            self._project_desc = ""
            self._project_db = ""
            self.puid = str(uuid.uuid4())
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

    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, n):
        if n != self._project_name:
            self._project_name = n
            self.dirty = True

    @property
    def project_desc(self):
        return self._project_desc

    @project_desc.setter
    def project_desc(self, n):
        if n != self._project_desc:
            self._project_desc = n
            self.dirty = True

    @property
    def project_db(self):
        return self._project_db

    @project_db.setter
    def project_db(self, n):
        if n != self._project_db:
            self._project_db = n
            self.dirty = True

    def save(self):
        doc = {"name": self._name, "password_hash": self._password_hash, "uuid": self.uuid,
               "project_name": self._project_name, "project_desc": self._project_desc,
               "project_db": self._project_db, "puid": self.puid}
        return doc

    def load(self, doc):
        self._name = doc["name"]
        self._password_hash = doc["password_hash"]
        self.uuid = doc["uuid"]
        self._project_name = doc["project_name"]
        self._project_desc = doc["project_desc"]
        self._project_db = doc["project_db"]
        self.puid = doc["puid"]

    def __repr__(self):
        return "<New Project Data(name='%s', description='%s', db='%s', puid='%s', admin='%s', hash='%s', uuid='%s')>" % \
            (self._project_name, self._project_desc, self._project_db, self.puid,
                self._name, self._password_hash, self.uuid)
