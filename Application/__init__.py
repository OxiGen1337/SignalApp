from PySide6 import QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from Resources import Icons
from Views.Workspace import WorkspaceView


class Application:
    def __init__(self):
        self.__app = QtWidgets.QApplication()
        self.__window = QtWidgets.QMainWindow()
        self.__central_widget = None
        self.setup_ui()

    def setup_ui(self):
        self.__window.setWindowTitle('SignalApp')
        self.__app.setWindowIcon(QIcon(Icons.path() + r'\wave-sound.ico'))
        self.__window.resize(QSize(900, 600))
        self.__central_widget = WorkspaceView(self.__window)
        self.__window.setCentralWidget(self.__central_widget)

    def run(self):
        self.__window.show()
        return self.__app.exec()
