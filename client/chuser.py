import PyQt4.QtGui as QtGui
import PyQt4.uic as uic
from PyQt4.QtCore import pyqtSlot

from .config import *


class ChangeUserDialog(QtGui.QDialog):
    def __init__(self, parent, xfer):
        super(ChangeUserDialog, self).__init__(parent)
        uic.loadUi(ui_change_user, self)
        self.setModal(True)
        #
        self.xfer = xfer
        self.editName.setText(xfer.name)
        self.editPassword.setText(xfer.password)
        #
        self.editName.textChanged.connect(self.on_edit)
        self.editPassword.textChanged.connect(self.on_edit)
        #
        self.on_edit()
        self.show()

    @pyqtSlot()
    def on_edit(self):
        enabled = len(self.editName.text()) > 0
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(enabled)

    @pyqtSlot()
    def accept(self):
        self.xfer.name = self.editName.text()
        self.xfer.password = self.editPassword.text()
        super(ChangeUserDialog, self).accept()

    def closeEvent(self, event):
        event.accept()
    #
