import sys
import device
from pathlib import Path

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import cv2

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle('Face Recognition')
        self.resize(640,480)

        stylesheet = open(Path(__file__+r'\..\style\buttons.qss')).read()

        #creating main layout
        self.MainLayout = QVBoxLayout()

        # actually setting it as mainlayout
        self.setLayout(self.MainLayout)
        self.setStyleSheet(stylesheet)

        #creating label and adding it to main layout
        self.label = QLabel()
        # self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(640,480)


        self.combo_box = QComboBox()
        self.combo_box.addItems(device.getDeviceList())
        self.combo_box.setFixedSize(300,50)


        self.selectcam = QPushButton('select device')
        self.selectcam.setFixedSize(150,50)
        
        # self.selectcam.setStyleSheet(stylesheet)
        self.selectcam.clicked.connect(self.camupdate)
        

        self.MainLayout.addWidget(self.label,alignment=Qt.AlignCenter)
        self.MainLayout.addWidget(self.combo_box,alignment=Qt.AlignCenter)
        self.MainLayout.addWidget(self.selectcam,alignment=Qt.AlignCenter | Qt.AlignTop)
        

        # running opencv thread and connecting it to label 
        self.Worker1 = Worker1()
        # self.Worker1.index = self.cameraindex
        self.Worker1.start()
        self.Worker1.changePixmap.connect(self.ImageUpdateSlot)

    
    def ImageUpdateSlot(self,image):
        self.label.setPixmap(QPixmap.fromImage(image)) 
    
    def camupdate(self):
        self.Worker1.changeindex(self.combo_box.currentIndex())

class Worker1(QThread):
    def __init__(self):
        super(Worker1,self).__init__()
        self.index = 0
        self.ThreadActive = True
        self.Cap = cv2.VideoCapture(0)
        self.Cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    changePixmap = pyqtSignal(QImage)

    def main(self,Cap):
        while True:
            if not self.ThreadActive:
                print(self.index)
                Cap.release()
                Cap = cv2.VideoCapture(self.index)
                self.ThreadActive = True

            ret,frame = Cap.read()
        
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = self.Cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=7,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x,y,z,h) in faces:
                center = (x + z//2, y + h//2)
                frame = cv2.ellipse(frame, center, (z//2, h//2), 0, 0, 360, (255, 0, 255), 4)
            
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FlippedImage = cv2.flip(rgbImage, 1)
            self.convertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1],FlippedImage.shape[0], QImage.Format_RGB888)
            p = self.convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)



    def run(self):
        self.main(self.Cap)

    def changeindex(self,index):
        self.index = index 
        self.ThreadActive = False
        print(self.isFinished())







# just recommeded way to run program just follow this 
if __name__ == "__main__":
    App = QApplication(sys.argv) # this is for closing the app
    # calling MainWindow class and just showing it 
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())