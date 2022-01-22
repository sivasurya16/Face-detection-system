import sys
import device
from pathlib import Path
import pickle,json
import time

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import face_recognition
import numpy as np

import cv2

from Modules import groupbox

class details(groupbox.Ui_Details,QGroupBox):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(322, 223) 


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Face Recognition')
        self.resize(640,480)
        icon = QIcon()
        icon.addPixmap(QPixmap("UI_Files\\facial-recognition.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        # self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

        stylesheet = open(Path(__file__,'../../style/buttons.qss')).read()

        #creating main layout
        self.MainLayout = QVBoxLayout()


        # actually setting it as mainlayout
        self.setLayout(self.MainLayout)
        self.setStyleSheet(stylesheet)

        #creating label and adding it to main layout
        self.sideBySide = QWidget()
        self.sideBySide.setStyleSheet('background-color:rgba(255,0,0,0)')
        self.sideBySideLayout = QHBoxLayout(self.sideBySide)
        self.label = QLabel()
        self.label.setPixmap(QPixmap("UI_Files\\no-camera.png").scaled(300,300,Qt.KeepAspectRatio))

        self.label.setScaledContents(True)

        self.Details = details()
        self.Details.setStyleSheet("QGroupBox{ margin-bottom : 0px; margin-top: 5px ;padding-top: 5px;subcontrol-origin: margin;subcontrol-position: top center;} QGroupBox:title{ subcontrol-origin: margin;subcontrol-position: top center; font:Bold }")

        self.sideBySideLayout.addWidget(self.label)
        self.sideBySideLayout.addWidget(self.Details)
        

        try:
            self.Devices = device.getDeviceList()
        except SystemError:
            self.Devices = ['You have no camera']

        self.combo_box = QComboBox()
        self.combo_box.addItems(self.Devices)
        self.combo_box.setFixedSize(300,50)


        self.selectcam = QPushButton('select device')
        self.selectcam.setFixedSize(150,50)

        if self.Devices == ['You have no camera']:
            self.combo_box.setDisabled(True)
            self.selectcam.setDisabled(True)
        
        self.selectcam.clicked.connect(self.camupdate)
        

        self.MainLayout.addWidget(self.sideBySide,alignment=Qt.AlignCenter)
        self.MainLayout.addWidget(self.combo_box,alignment=Qt.AlignCenter)
        self.MainLayout.addWidget(self.selectcam,alignment=Qt.AlignCenter | Qt.AlignTop)
        

        # running opencv thread and connecting it to label 
        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.changePixmap.connect(self.ImageUpdateSlot)
        self.Worker1.updateName.connect(self.updateName)


    def updateName(self,name):
        self.Details.nameLabel.setText(name)
    
    def ImageUpdateSlot(self,image):
        self.label.setPixmap(QPixmap.fromImage(image)) 
    
    def camupdate(self):
        self.Worker1.changeindex(self.combo_box.currentIndex())

    def closeEvent(self,event):
        self.Worker1.ThreadActive = False
        self.Worker1.forcequit = True

class Worker1(QThread):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.ThreadActive = True
        self.forcequit = False
        self.camcount = 1

        self.Cap = cv2.VideoCapture(0)
        if self.Cap is None or not self.Cap.isOpened():
            self.camcount = None
        self.Cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    changePixmap = pyqtSignal(QImage)
    updateName = pyqtSignal(str)

    def main(self,Cap,count):
        Threadran = False
        waitTime = None

        self.name = "unknown"
        self.names = json.load(open('encodings/names.json'))
        self.encode_list = pickle.load(open('encodings/encodings.dat','rb'))

        while True:
            if count == None:
                break
            if not self.ThreadActive:
                Cap.release()
                if self.forcequit:
                    break

                Cap = cv2.VideoCapture(self.index)
                self.ThreadActive = True


            ret,frame = Cap.read()
            imgs = cv2.resize(frame, (0,0),None,0.25,0.25)
            imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
            # face recognition
            if Threadran == False:
                faces_cur_frame = face_recognition.face_locations(imgs)
                encodes_cur_frame = face_recognition.face_encodings(imgs, faces_cur_frame)

                Threadran = True
                waitTime = time.time()
                for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
                    self.name = "unknown"
                    match = face_recognition.compare_faces(self.encode_list, encodeFace, tolerance=0.60)
                    face_dis = face_recognition.face_distance(self.encode_list, encodeFace)
                    best_match_index = np.argmin(face_dis)

                    if match[best_match_index]:
                        self.name = self.names[best_match_index].capitalize()
                        self.updateName.emit(self.name)
                        


            if time.time()-waitTime > 5:
                Threadran = False
                    
                    
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = self.Cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(100,100),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x,y,z,h) in faces:
                center = (x + z//2, y + h//2)
                frame = cv2.ellipse(frame, center, (z//2, h//2), 0, 0, 360, (255, 0, 255), 4)
                cv2.putText(frame, self.name, (x + 6, y - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            self.convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1],rgbImage.shape[0], QImage.Format_RGB888)
            p = self.convertToQtFormat.scaled(*frame.shape[:2], Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

    def run(self):
        self.main(self.Cap,self.camcount)

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
