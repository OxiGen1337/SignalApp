from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer, QSize
import os
import vlc
from PySide6.QtGui import QIcon

from Resources import Icons

class SoundPlayer(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__layout = None
        self.__title = None
        self.__slider = None
        self.__time_label = None
        self.__time_total = None
        self.__play_btn = None
        self.__volume_slider = None

        self.__vlc = vlc.Instance('--input-repeat=-1')
        self.__player = self.__vlc.media_player_new()
        self.__track_length = 0
        self.__updating_slider = False

        self.setup_ui()

        self.__timer = QTimer(self)
        self.__timer.setInterval(500)
        self.__timer.timeout.connect(self.update_slider)

        self.set_volume(75)

    def setup_ui(self):
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.__layout = QtWidgets.QGridLayout(self)
        self.__layout.setColumnStretch(0, 7)
        self.__layout.setColumnStretch(1, 3)
        self.__layout.setVerticalSpacing(5)
        self.__layout.setHorizontalSpacing(20)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.__title = QtWidgets.QLabel('10_05_2025-15_50.wav')
        self.__title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__layout.addWidget(self.__title, 0, 0)

        self.__slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.__slider.setRange(0, 1000)
        self.__slider.sliderMoved.connect(self.seek)
        self.__layout.addWidget(self.__slider, 1, 0)

        time_layout = QtWidgets.QHBoxLayout()
        self.__time_label = QtWidgets.QLabel("0:00")
        self.__play_btn = QtWidgets.QPushButton(QIcon(Icons.path() + r'\play.png'), '')
        self.__play_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 0;
            }
        """)
        self.__play_btn.setIconSize(QSize(16, 16))
        self.__play_btn.clicked.connect(self.toggle_play)
        self.__time_total = QtWidgets.QLabel("0:00")
        time_layout.addWidget(self.__time_label)
        time_layout.addStretch()
        time_layout.addWidget(self.__play_btn)
        time_layout.addStretch()
        time_layout.addWidget(self.__time_total)
        self.__layout.addLayout(time_layout, 2, 0)

        self.__volume_slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.__volume_slider.setRange(0, 100)
        self.__volume_slider.setValue(75)
        self.__volume_slider.valueChanged.connect(self.set_volume)
        self.__layout.addWidget(QtWidgets.QLabel('Volume', alignment=Qt.AlignmentFlag.AlignCenter), 0, 1)
        self.__layout.addWidget(self.__volume_slider, 1, 1)
        volume_labels = QtWidgets.QHBoxLayout()

        volume_labels.addWidget(QtWidgets.QLabel('0%'))
        volume_labels.addStretch()
        volume_labels.addWidget(QtWidgets.QLabel('100%'))
        self.__layout.addLayout(volume_labels, 2, 1)



    def load(self, path):
        media = self.__vlc.media_new(path)
        self.__player.set_media(media)
        base = os.path.basename(path)
        self.__title.setText(base)
        self.__player.play()
        # self.__play_btn.setVisible(False)
        QTimer.singleShot(100, self.update_length)

    def update_length(self):
        self.__track_length = self.__vlc.get_length() / 1000
        self.__slider.setEnabled(True)
        self.__time_total.setText(self.format_time(self.__track_length))

    def toggle_play(self):
        if self.__player.is_playing():
            self.__player.pause()
            # self.play_btn.setVisible(True)
            # self.pause_btn.setVisible(False)
        else:
            self.__player.play()
            # self.play_btn.setVisible(False)
            # self.pause_btn.setVisible(True)

    def seek(self, value):
        if not self.__track_length:
            return
        self.__updating_slider = True
        pos = value / 1000.0
        self.__player.set_position(pos)
        self.__updating_slider = False

    def set_volume(self, value):
        self.__player.audio_set_volume(value)

    def update_slider(self):
        if self.__player.is_playing() and not self.__updating_slider:
            pos = self.__player.get_position()
            sec = self.__track_length * pos
            self.__time_label.setText(self.format_time(sec))
            self.__slider.setValue(int(pos * 1000))
        elif not self.__player.is_playing():
            if self.__player.get_position() >= 0.99:
                self.__slider.setValue(0)
                # self.play_btn.setVisible(True)
                # self.pause_btn.setVisible(False)

    @staticmethod
    def format_time(seconds):
        m, s = divmod(int(seconds), 60)
        return f"{m}:{s:02d}"
