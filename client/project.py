import PyQt4.QtGui as QtGui
import PyQt4.uic as uic
from PyQt4.QtCore import pyqtSlot
import requests

from .config import *
from utils.functrace import logger, trace_scope


class ProjectWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(ProjectWidget, self).__init__(parent)
        uic.loadUi(ui_projectwidget, self)
        #
        self.xfer = None
        self.editName.textChanged.connect(self.on_edit)
        self.editDesc.textChanged.connect(self.on_edit)
        self.cbExpandInfo.clicked.connect(self.frameInfo.setVisible)
        self.frameInfo.setVisible(False)
        #
        self.hide()

    @trace_scope("Open project")
    def open(self, xfer):
        self.editName.setText(xfer["name"])
        self.editDesc.setPlainText(xfer["description"])
        self.tableInfo.setCellWidget(0, 0, QtGui.QLabel("PUID"))
        self.tableInfo.setCellWidget(0, 1, QtGui.QLabel(xfer["puid"]))
        self.tableInfo.setCellWidget(1, 0, QtGui.QLabel("Creation Date"))
        self.tableInfo.setCellWidget(1, 1, QtGui.QLabel(xfer["creation_date"]))
        self.tableInfo.setCellWidget(2, 0, QtGui.QLabel("Owner"))
        # self.tableInfo.setCellWidget(2, 1, QtGui.QLabel(xfer["owner"]))
        self.tableInfo.setCellWidget(3, 0, QtGui.QLabel("Schema Version"))
        self.tableInfo.setCellWidget(3, 1, QtGui.QLabel(xfer["schema_version"]))
        self.xfer = xfer
        self.show()
        #

    @trace_scope("Close project")
    def close(self):
        self.xfer = None
        self.editName.setText("")
        self.editDesc.setPlainText("")
        self.hide()
        #

    @pyqtSlot()
    @trace_scope("Edit name/desc")
    def on_edit(self):
        if self.xfer:
            # TODO save to db
            newName = self.editName.Text()
            #
            pass
        pass


