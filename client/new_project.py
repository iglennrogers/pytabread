import PyQt4.QtGui as QtGui
import PyQt4.uic as uic
from PyQt4.QtCore import pyqtSlot

from .config import *


class NewProjectDialog(QtGui.QDialog):
    def __init__(self, parent, xfer):
        super(NewProjectDialog, self).__init__(parent)
        uic.loadUi(ui_new_project, self)
        self.setModal(True)
        #
        self.xfer = xfer
        self.editProjName.setText(xfer.project_name)
        self.editProjDesc.setPlainText(xfer.project_desc)
        self.editProjDb.setText(xfer.project_db)
        self.editName.setText(xfer.name)
        self.editPassword.setText(xfer.password)
        self.editPassword2.setText(xfer.password)
        #
        self.editProjName.textChanged.connect(self.on_edit)
        self.editProjDb.textChanged.connect(self.on_edit)
        self.editName.textChanged.connect(self.on_edit)
        self.editPassword.textChanged.connect(self.on_edit)
        self.editPassword2.textChanged.connect(self.on_edit)
        self.on_edit()
        self.show()

    @pyqtSlot()
    def on_edit(self):
        enabled = len(self.editProjName.text()) > 0 and len(self.editProjDb.text()) > 0 and \
                len(self.editName.text()) > 0 and self.editPassword.text() == self.editPassword2.text()
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(enabled)

    @pyqtSlot()
    def accept(self):
        self.xfer.project_name = self.editProjName.text()
        self.xfer.project_desc = self.editProjDesc.toPlainText()
        self.xfer.project_db = self.editProjDb.text()
        self.xfer.name = self.editName.text()
        self.xfer.password = self.editPassword.text()
        super(NewProjectDialog, self).accept()

    def closeEvent(self, event):
        event.accept()
    #

