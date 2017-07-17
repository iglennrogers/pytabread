import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import schema_version, admin_rights
from .tables import ProjectBase, ProjInfoTable, AccessTable
from utils.functrace import logger, trace_scope


class ProjectDb:

    @staticmethod
    def new_project(xfer):
        project = ProjectDb(xfer.project_db)
        return project.populate(xfer)

    @staticmethod
    def make_db_uri(dbname=None):
        return "sqlite:///" + dbname

    @staticmethod
    def read_base_info(dbname, user, auth):
        log = logger(__name__)
        log.info("About to read %s as user %s", dbname, user)
        proj = ProjectDb(dbname)
        if proj.is_authorized(auth):
            log.info("...authorized")
            return proj._project_db.query(ProjInfoTable).one()
        log.info("...not authorized")
        return None

    def __init__(self, dbname):
        self._logger = logger(self.__module__)
        self._engine = create_engine(ProjectDb.make_db_uri(dbname), echo=False)
        self._Session = sessionmaker(bind=self._engine)
        self._project_db = self._Session()
        ProjectBase.metadata.create_all(self._engine)

    def populate(self, xfer):
        base_info = ProjInfoTable(puid=xfer.puid, name=xfer.project_name, description=xfer.project_desc,
                                  creation_date=datetime.datetime.utcnow(), owner=xfer.uuid,
                                  schema_version=schema_version)
        access = AccessTable(uuid=xfer.uuid, name=xfer.name, password_hash=xfer.password_hash,
                             rights=admin_rights)
        self._project_db.add(base_info)
        self._project_db.add(access)
        self._project_db.commit()
        return base_info.puid

    def is_authorized(self, auth):
        return True
        # return self._project_db.query(AccessTable).filter(AccessTable.password_hash == auth).count() == 1

    @trace_scope("Get project uid")
    @property
    def project_uid(self):
        return self._project_db.query(ProjInfoTable).one().puid

    @staticmethod
    def get_project(puid):
        pass
        # def open_session(self, puid, auth):
        #     proj = self._open_projects[puid] = ProjectDb(puid)
        #     proj.open()

        # def close_project(self, suid):
        #     proj = self._open_projects[suid]
        #     del self._open_projects[suid]
        #     proj.open()
