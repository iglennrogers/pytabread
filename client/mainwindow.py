import json

import PyQt4.QtGui as QtGui
import PyQt4.uic as uic
from PyQt4.QtCore import pyqtSlot  # , pyqtSignal
import requests

from .config import *
from utils import XferNewProject
from utils.functrace import logger, trace_scope
from .new_project import NewProjectDialog
from .xfer_chuser import XferChangeUser
from .chuser import ChangeUserDialog
from .project import ProjectWidget


class MainWindow(QtGui.QMainWindow):
    # require_userdata_trigger = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(ui_mainwindow, self)
        self._logger = logger(self.__module__)
        self.actionNewProject.triggered.connect(self.on_action_newproject_triggered)
        self.actionQuit.triggered.connect(self.on_action_quit_triggered)
        self.menuProject.aboutToShow.connect(self.on_menu_open_triggered)
        self.actionLogin.triggered.connect(self.on_action_login_triggered)
        self.actionLogout.triggered.connect(self.on_action_logout_triggered)
        #
        self.userdata = XferChangeUser()
        # self.require_userdata_trigger.connect(self.on_action_login_triggered)
        self.on_action_login_triggered()
        #
        self.project_form = ProjectWidget(self)
        self.setCentralWidget(self.project_form)
        self.show()
    #

    @trace_scope("Login triggered")
    def on_action_login_triggered(self):
        self.menuUser.setTitle("No user")
        self.menuBar().setEnabled(False)
        userdlg = ChangeUserDialog(self, self.userdata)
        if userdlg.exec():
            self._logger.info("Got user {}".format(self.userdata.name))
            self.menuBar().setEnabled(True)
            resp = requests.get(url_project_resource, json=self.userdata.to_dict())
            project_list = json.loads(resp.text)
            self.menuOpen.setEnabled(len(project_list) > 0)
            self.menuUser.setTitle(self.userdata.name)
        else:
            self._logger.info("No user")
            #

    @trace_scope("Close Event")
    def closeEvent(self, event):
        event.accept()
    #

    @pyqtSlot()
    def on_action_quit_triggered(self):
        self.actionLogin.triggered.disconnect(self.on_action_login_triggered)
        self.on_action_logout_triggered()
        self.close()

    @pyqtSlot()
    @trace_scope("New Project triggered")
    def on_action_newproject_triggered(self):
        xfer = XferNewProject()
        dlg = NewProjectDialog(self, xfer)
        if dlg.exec():
            print(xfer)
            doc = xfer.save()
            resp = requests.post(url_project_resource, json=doc)
            print(resp.text)

    @pyqtSlot()
    @trace_scope("Logout triggered")
    def on_action_logout_triggered(self):
        self.project_form.close()
        self.on_action_login_triggered()

    @pyqtSlot()
    @trace_scope("Open menu triggered")
    def on_menu_open_triggered(self):
        resp = requests.get(url_project_resource, json=self.userdata.to_dict())
        project_list = json.loads(resp.text)
        self.menuOpen.clear()
        self.menuOpen.setEnabled(len(project_list) > 0)
        for project in project_list:
            action = self.menuOpen.addAction(project["name"])
            action.setData(project)
            action.triggered.connect(self.on_action_openproject_triggered)

    @pyqtSlot()
    @trace_scope("Open project triggered")
    def on_action_openproject_triggered(self):
        project = self.sender().data()
        self._logger.info(project)
        self.project_form.open(project)
        pass
