from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Signal

from Views.Editor.SignalEditors.SinSignalEditor import SinSignalEditorView
from Views.Editor.SignalEditors.CosSignalEditor import CosSignalEditorView
from Views.Editor.SoundPlayer import SoundPlayer


class EditorView(QtWidgets.QWidget):
    display_required = Signal(str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__layout = None

        self.__signal_combo_box = None
        self.__signal_editor_viewport = None
        self.__wave_editor_viewport = None

        self.__signals = ['SinSignal', 'CosSignal', 'SquareSignal']
        self.__signal_editors = [SinSignalEditorView(self), CosSignalEditorView(self), QtWidgets.QPushButton(self)]

        self.__wave_duration_input = None
        self.__wave_framerate_input = None

        self.__wave_tools_viewport = None
        self.__sound_player = None

        self.setup_ui()

    def register_editors(self):
        for editor in self.__signal_editors:
            self.__signal_editor_viewport.addWidget(editor)

    def setup_ui(self):
        self.__layout = QtWidgets.QVBoxLayout(self)

        self.__signal_combo_box = QtWidgets.QComboBox(self)
        self.__signal_combo_box.addItems(self.__signals)
        self.__signal_combo_box.currentIndexChanged.connect(self.on_signal_selected)
        self.__layout.addWidget(QtWidgets.QLabel('Select the signal you want to work with'))
        self.__layout.addWidget(self.__signal_combo_box)

        self.__signal_editor_viewport = QtWidgets.QStackedWidget(self)
        self.__signal_editor_viewport.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum)

        self.__signal_editor_viewport.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.__layout.addWidget(QtWidgets.QLabel('Enter parameters for the signal'))
        self.__layout.addWidget(self.__signal_editor_viewport)

        self.register_editors()

        self.__wave_editor_viewport = QtWidgets.QFrame(self)
        self.__wave_editor_viewport.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        wave_editor_layout = QtWidgets.QVBoxLayout(self.__wave_editor_viewport)
        self.__wave_editor_viewport.setLayout(wave_editor_layout)
        self.__layout.addWidget(QtWidgets.QLabel('Make the wave with specified parameters'))
        self.__layout.addWidget(self.__wave_editor_viewport)

        self.__wave_duration_input = QtWidgets.QDoubleSpinBox(self, minimum=0, maximum=2048, decimals=1)
        wave_editor_layout.addWidget(QtWidgets.QLabel('Duration'))
        wave_editor_layout.addWidget(self.__wave_duration_input)

        self.__wave_framerate_input = QtWidgets.QSpinBox(self, minimum=0, maximum=100000)
        wave_editor_layout.addWidget(QtWidgets.QLabel('Framerate'))
        wave_editor_layout.addWidget(self.__wave_framerate_input)

        create_wave_btn = QtWidgets.QPushButton('Make wave')
        wave_editor_layout.addWidget(create_wave_btn)

        self.__layout.addStretch()

        self.__sound_player = SoundPlayer(self)
        self.__layout.addWidget(self.__sound_player)

        self.__wave_tools_viewport = QtWidgets.QFrame(self)
        self.__wave_tools_viewport.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        wave_tools_viewport_layout = QtWidgets.QGridLayout(self.__wave_tools_viewport)
        # wave_tools_viewport_layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.addWidget(self.__wave_tools_viewport)

        wave_tools_viewport_layout.addWidget(QtWidgets.QPushButton('Plot'), 0, 0)
        wave_tools_viewport_layout.addWidget(QtWidgets.QPushButton('Spectrogram'), 1, 0)
        wave_tools_viewport_layout.addWidget(QtWidgets.QPushButton('Int. spectrogram'), 2, 0)

    def on_signal_selected(self):
        index = self.__signal_combo_box.currentIndex()
        self.__signal_editor_viewport.setCurrentIndex(index)
