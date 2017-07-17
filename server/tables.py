import datetime

from sqlalchemy import Column, Integer, String, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base

from . import uniqueid


SessionBase = declarative_base()
ProjectBase = declarative_base()


class SessionTable(SessionBase):
    __tablename__ = "session"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    puid = uniqueid.defn()
    uuid = uniqueid.defn()
    suid = uniqueid.defn()
    expires = Column(DateTime)

    def __repr__(self):
        return "<SessionTable(project='%s', user='%s', session='%s', expires='%s')>" % (
            self.puid, self.uuid, self.suid, str(self.expires))

    def as_dict(self):
        return {"puid": self.puid, "uuid": self.uuid, "suid": self.suid,
                "expires": str(self.expires)}


class ProjInfoTable(ProjectBase):
    __tablename__ = "projinfo"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    puid = uniqueid.defn()
    name = Column(String(50))
    description = Column(String(255))
    creation_date = Column(DateTime)
    owner = uniqueid.defn()
    schema_version = Column(Integer)

    def __repr__(self):
        return "<ProjInfoTable(project='%s', name='%s', description='%s', creation='%s', owner='%s')>" % (
            self.puid, self.name, self.description, self.creation_date, self.owner)

    def as_dict(self):
        return {"puid": self.puid, "name": self.name, "description": self.description,
                "creation_date": str(self.creation_date), "owner": self.owner,
                "schema_version": str(self.schema_version)}


class AccessTable(ProjectBase):
    __tablename__ = "access"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    uuid = uniqueid.defn()
    name = Column(String(50))
    full_name = Column(String(50))
    password_hash = Column(String(50))
    rights = Column(Integer)

    def __repr__(self):
        return "<AccessTable(user='%s', name='%s', rights='%s')>" % (
            self.uuid, self.name, self.rights)

    def as_dict(self):
        return {"uuid": self.uuid, "name": self.name, "full_name": self.full_name,
                "password_hash": self.password_hash,
                "rights": str(self.rights)}

