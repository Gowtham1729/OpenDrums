import os
import sys
import cv2
from pygame import mixer
import time
import serial
import random

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimeZone, QThread, pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox

from open_drum import Ui_OpenDrum

mixer.init()


class VideoThread(QThread):
    signal = pyqtSignal("PyQt_PyObject")

    def __init__(self, gui):
        QThread.__init__(self)
        self.gui = gui
        self.prev = 0

    def __del__(self):
        self.wait()

    def run(self):

        while True:
            # ret, frame = self.gui.cap.read()
            # cv2.imshow('frame', frame)
            sound = mixer.Sound("drums/" + self.gui.ui.drum_type.currentText() + '/' + self.gui.ui.sound.currentText())
            # print("playing", "drums/" + self.gui.ui.drum_type.currentText() + '/' + self.gui.ui.sound.currentText())
            args = str(self.gui.ard.readline())
            try:
                count = (args[2:-5])
                count = int(count)
                if 235 < count < 245:
                    print(count)
                    if count > self.prev + 2:
                        sound.play()
                        print("playing")
                self.prev = count
            except ValueError:
                print("value error")

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        # self.gui.cap.release()
        # cv2.destroyAllWindows()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_OpenDrum()
        self.ui.setupUi(self)

        self.drum_type = os.listdir("drums")
        self.ui.drum_type.addItems(self.drum_type)
        self.ui.drum_type.currentIndexChanged.connect(self.drum_sound)

        self.ui.sound.addItems(os.listdir("drums/606 Basic"))

        self.ui.start.clicked.connect(self.start_game)
        self.ui.randomize.clicked.connect(self.random_sound)

        self.cap = cv2.VideoCapture(0)
        self.PORT_NO = "/dev/ttyACM0"
        self.ard = serial.Serial(self.PORT_NO, 9600)
        self.video_thread = None

    def drum_sound(self):
        self.ui.sound.clear()
        self.ui.sound.addItems(os.listdir("drums/" + self.ui.drum_type.currentText()))

    def start_game(self):
        self.ui.start.setEnabled(False)
        self.video_thread = VideoThread(gui=self)
        self.video_thread.start()

    def random_sound(self):
        print(len(os.listdir("drums/" + self.ui.drum_type.currentText())))
        self.ui.sound.setCurrentIndex(random.choice(0, 5))


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
