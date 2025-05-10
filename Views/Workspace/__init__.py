from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from Views import Editor
from Views import Display


class WorkspaceView(QtWidgets.QSplitter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        editor = Editor.EditorView()
        display = Display.DisplayView()
        display.setup_display_event(editor.display_required)

        self.addWidget(editor)
        self.addWidget(display)

        self.setSizes([500, 900])
        self.setHandleWidth(0)

