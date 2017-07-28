import datetime
import glob

import falcon
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, exc

from utils import uniqueid
from utils.functrace import trace_scope, logger
from . import config
from . import tables
from .projectdb import ProjectDb


class SessionDb:
    _instance = None

    def __init__(self):
        self._logger = logger(self.__module__)
        self._engine = None
        self._Session = None
        self._session_db = None
        #
        self._project_cache = {}
        self._project_info = {}

    @staticmethod
    def instance():
        if not SessionDb._instance:
            SessionDb._instance = SessionDb()
            SessionDb._instance.initialize()
        return SessionDb._instance

    @trace_scope("Initialise session")
    def initialize(self):
        self._engine = create_engine('sqlite:///mem.sqdb', echo=False)
        self._Session = sessionmaker(bind=self._engine)
        self._session_db = self._Session()
        tables.SessionBase.metadata.create_all(self._engine)
        #
        self.search_for_projects()

    @trace_scope("Get project list")
    def project_list(self, user, auth):
        db_list = []
        for db_file in self._project_info.values():
            pinfo = ProjectDb.read_base_info(db_file, user, auth)
            if pinfo:
                self._logger.info("...%s authorized for user %s", db_file, user)
                db_list.append(pinfo)
            else:
                self._logger.info("...%s not authorized for user %s", db_file, user)
        return db_list

    @trace_scope("Validate session")
    def validate_session(self, **kwargs):
        timestamp = datetime.datetime.utcnow()
        row = self._extract_row(kwargs)
        if row.expires < timestamp:
            self.close_session(row=row)
            raise falcon.HTTP_UNAUTHORIZED
        else:
            row.expires = timestamp + datetime.timedelta(minutes=config.timeout_minutes)
            row.update()
            self._session_db.commit()

    @trace_scope("Create session")
    def create_session(self, puid, uuid):
        suid = uniqueid.newvalue()
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=config.timeout_minutes)
        new_row = tables.SessionTable(puid=puid, uuid=uuid, suid=suid, expires=expiry_time)
        self._session_db.add(new_row)
        self._session_db.commit()
        self.__add_project_to_cache(puid)
        return suid

    @trace_scope("Close session")
    def close_session(self, **kwargs):
        old_row = self._extract_row(kwargs)
        self._session_db.delete(old_row)
        self._session_db.commit()
        self.__remove_project_from_cache(old_row.puid)

    @trace_scope("Open session")
    def open_session(self, puid, uuid):
        row = self._extract_row(puid=puid, uuid=uuid)
        if row:
            self.validate_session(row=row)
            return row.suid
        else:
            return self.create_session(puid, uuid)

    @trace_scope("Get project")
    def get_project(self, suid):
        row = self._extract_row(suid=suid)
        self.validate_session(row=row)
        return row.puid

    @trace_scope("Get user")
    def get_user(self, suid):
        row = self._extract_row(suid=suid)
        self.validate_session(row=row)
        return row.uuid

    @trace_scope("Extract row from args")
    def _extract_row(self, **kwargs):
        self._logger.info(kwargs)
        if "suid" in kwargs:
            suid = kwargs["suid"]
            return self._session_db.query(tables.SessionTable.suid == suid).one()
        elif "row" in kwargs:
            return kwargs["row"]
        elif "puid" in kwargs and "uuid" in kwargs:
            puid = kwargs["puid"]
            uuid = kwargs["uuid"]
            try:
                row = self._session_db.query(tables.SessionTable)\
                    .filter(tables.SessionTable.puid == puid)\
                    .filter(tables.SessionTable.uuid == uuid).one()
            except exc.NoResultFound:
                row = None
            return row
        else:
            raise NotImplementedError

    @trace_scope("Search for data files")
    def search_for_projects(self):
        for db_file in glob.glob(config.base_directory + "*.sqlite"):
            self._logger.info("...%s found", db_file)
            self.register_project(db_file)

    @trace_scope("Register project")
    def register_project(self, db_file, puid=None):
        if not puid:
            puid = ProjectDb(db_file).project_uid
        self._project_info[puid] = db_file

    @trace_scope("Add project to cache")
    def __add_project_to_cache(self, puid):
        if puid in self._project_cache:
            use, db = self._project_cache[puid]
        else:
            use = 0
            db = ProjectDb(self._project_info[puid])
        self._project_cache[puid] = (use + 1, db)

    @trace_scope("Remove project from cache")
    def __remove_project_from_cache(self, puid):
        use, db = self._project_cache[puid]
        use -= 1
        if use > 0:
            self._project_cache[puid] = (use, db)
        else:
            del self._project_cache[puid]
