#!/usr/bin/python3

import falcon
import logging

import server.userresource as user
import server.projectresource as project
from server.sessiondb import SessionDb


logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('pytabread.server').setLevel(logging.INFO)
#
api = application = falcon.API()
api.add_route('/project', project.ProjectResource())
api.add_route('/project/{project}', project.ProjectResource())
api.add_route('/user/{uuid}', user.UserResource())
api.add_route('/user', user.UserResource())
