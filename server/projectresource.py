import falcon
import json
import datetime
import falcon_json.hooks as hooks

from .projectdb import ProjectDb
from .sessiondb import SessionDb
from utils import XferNewProject
from utils.functrace import trace_scope, dump_context
from .config import readonly_rights


def validate_session(context):
    suid = context["suid"]
    reqtime = datetime.datetime.utcnow()
    SessionDb.instance().validate_session(suid, reqtime)


class ProjectResource:
    @trace_scope("on_get")
    @falcon.before(hooks.process_json_request)
    @dump_context()
    def on_get(self, req: falcon.Request, resp: falcon.Response, puid: str = None):
        """if proj is None: returns a list of current projects
            else: expects an authorization attribute to log onto the project
        """
        resp.content_type = "application/json"
        resp.status = falcon.HTTP_200
        #
        doc = req.context["json"]
        auth = doc["password_hash"]
        if puid:
            project_item = ProjectDb(puid=puid)
            if project_item.is_authorized(auth, readonly_rights):
                newdict = project_item.as_dict()
                newdict["suid"] = project_item.login(auth)
                resp.body = json.dumps()
            else:
                raise falcon.HTTP_UNAUTHORIZED
        else:
            project_list = SessionDb.instance().project_list(doc["name"], doc["password_hash"])
            resp.body = json.dumps([p.as_dict() for p in project_list])

    @trace_scope("on_post")
    @falcon.before(hooks.process_json_request)
    @dump_context()
    def on_post(self, req: falcon.Request, resp: falcon.Response):
        resp.content_type = "application/json"
        doc = req.context['json']
        xfer = XferNewProject(doc)
        puid = ProjectDb.new_project(xfer)
        uuid = doc["uuid"]
        if puid:
            suid = SessionDb.instance().open_session(puid, uuid)
            doc["suid"] = resp.set_cookie("auth", str(suid))
            resp.status = falcon.HTTP_200
            resp.body = str(puid)
        else:
            raise falcon.HTTP_NOT_ACCEPTABLE

    def on_delete(self, req: falcon.Request, resp: falcon.Response, proj:str):
        user = req.cookies["auth"]
        pass
