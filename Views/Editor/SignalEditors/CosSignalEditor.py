from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class CosSignalEditorView(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__layout = None
        self.__frequency_input = None
        self.__amplitude_input = None
        self.__offset_input = None
        self.setup_ui()

    def setup_ui(self):
        self.__layout = QtWidgets.QVBoxLayout(self)

        self.__frequency_input = QtWidgets.QSpinBox(self, minimum=0, maximum=2048)
        self.__frequency_input.setSingleStep(64)
        self.__layout.addWidget(QtWidgets.QLabel('Frequency'))
        self.__layout.addWidget(self.__frequency_input)

        self.__amplitude_input = QtWidgets.QDoubleSpinBox(self, minimum=0, maximum=1, decimals=1)
        self.__amplitude_input.setSingleStep(0.1)
        self.__layout.addWidget(QtWidgets.QLabel('Amplitude'))
        self.__layout.addWidget(self.__amplitude_input)

        self.__offset_input = QtWidgets.QSpinBox(self, minimum=0, maximum=2048)
        self.__layout.addWidget(QtWidgets.QLabel('Offset'))
        self.__layout.addWidget(self.__offset_input)


