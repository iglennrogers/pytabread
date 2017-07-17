import logging

import PyQt4.QtGui as QtGui

from client import mainwindow


if __name__ == "__main__":
    try:
        app = QtGui.QApplication([])
    except RuntimeError:
        app = QtGui.QApplication.instance()
    logging.basicConfig()
    logging.getLogger('pytabread.client').setLevel(logging.INFO)
    mw = mainwindow.MainWindow()
    app.exec_()
