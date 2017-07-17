import falcon
import falcon_json.hooks as hooks

from utils.functrace import trace_scope, dump_context
from .userdb import UserDb
from .sessiondb import SessionDb



class UserResource:
    @trace_scope("on_get")
    @falcon.before(hooks.process_json_request)
    @dump_context()
    def on_get(self, req: falcon.Request, resp: falcon.Response, uuid: str = None):
        resp.content_type = "application/json"
        doc = req.context['json']
        suid = doc["suid"]
        puid = SessionDb.instance().get_project(suid)
        userdb = UserDb(puid)