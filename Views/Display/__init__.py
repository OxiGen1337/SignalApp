from PySide6 import QtWidgets
from PySide6.QtCore import Signal


from thinkdsp import Signal, CosSignal

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MatplotlibWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.figure.set_facecolor('#2d2d2d')
        self.axes.tick_params(axis='x', colors='#ffffff')
        self.axes.tick_params(axis='y', colors='#ffffff')
        self.axes.set_facecolor('#2d2d2d')
        for spine in self.axes.spines.values():
            spine.set_edgecolor('#1d1d1d')
        super().__init__(self.figure)
        self.setParent(parent)

    def plot(self, x, y):
        self.axes.plot(x, y)

    def plot_by_signal(self, signal: Signal):
        wave = signal.make_wave(signal.period * 3, start=0, framerate=11025)
        self.plot(wave.ts, wave.ys)


class DisplayView(QtWidgets.QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()

    def __on_display_event(self):
        print('got it')

    def setup_display_event(self, signal: Signal):
        # signal.connect(self.__on_display_event)
        pass

    def switch_view(self, view):
        pass

    def setup_ui(self):
        w = MatplotlibWidget(self)
        self.addWidget(w)
        w.plot_by_signal(CosSignal())

