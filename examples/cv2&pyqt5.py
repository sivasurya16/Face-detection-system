 # from https://stackoverflow.com/a/55468544/6622587
import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap



# creating a Thread
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    # Inside the Thread we are getting data from video camera using cv2
    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            self.convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = self.convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)


# Main window
class App(QWidget):
    def __init__(self):
        super().__init__()
        # defining some default stuff as instance variables
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        # Defining default properties of UI 
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(640,480)
        # create a label
        self.label = QLabel(self)
        self.label.resize(640, 480)
        # Creating thread which runs independent from GUI to prevent freezing
        th = Thread(self)
        # Connecting to change frames 
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()


if __name__ == '__main__':
    # running the GUI by instancing APP class
    app = QApplication(sys.argv)
    ex = App()
    exit(app.exec_())