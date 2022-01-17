import sys
import device
from pathlib import Path,PurePath
import os
import threading
import time

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import face_recognition
import numpy as np

import cv2

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Face Recognition')
        self.resize(640,480)
        icon = QIcon()
        icon.addPixmap(QPixmap("UI_Files\\facial-recognition.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        # self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

        stylesheet = open(PurePath(__file__,'../../style/buttons.qss')).read()

        #creating main layout
        self.MainLayout = QVBoxLayout()


        # actually setting it as mainlayout
        self.setLayout(self.MainLayout)
        self.setStyleSheet(stylesheet)

        #creating label and adding it to main layout
        self.label = QLabel()
        self.label.setPixmap(QPixmap("UI_Files\\no-camera.png").scaled(300,300,Qt.KeepAspectRatio))
        # self.label.resize(640,480)
        # self.MainLayout.setFixedSize(self.label.size())
        self.label.setScaledContents(True)
        # self.label.setAlignment(Qt.AlignCenter)
        

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

    def main(self,Cap,count):
        PATH = 'pictures'
        if not os.path.exists(PATH):
            os.mkdir(PATH)

        # faces encondings and names
        images = []
        self.names = []
        self.encode_list = []
        users = os.listdir(PATH)
        self.name = "unknown"
        
        # print(users)

        # getting img name from img files
        for ppl in users:
            cur_img = cv2.imread(f'{PATH}/{ppl}')
            images.append(cur_img)
            self.names.append(os.path.splitext(ppl)[0])

        # encoding images
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
            # encode = face_recognition.face_encodings(img)[0]
            self.encode_list.append(encodes_cur_frame)

        while True:
            if count == None:
                break
            if not self.ThreadActive:
                Cap.release()
                if self.forcequit:
                    break

                print(self.index)
                Cap = cv2.VideoCapture(self.index)
                self.ThreadActive = True


            ret,frame = Cap.read()
            imgs = cv2.resize(frame, (0,0),None,0.25,0.25)
            imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

            # self.faceDetectThread = faceDetect(imgs=imgs,encode_list=self.encode_list,names=self.names,name=self.name)
            # self.faceDetectThread.start()
                    
            # self.facerec(frame, self.encode_list, self.names, self.name,imgs)
            
            th = threading.Thread(target=self.facerec,args=(frame, self.encode_list, self.names, self.name,imgs))
            th.start()
            # th.join()
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = self.Cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x,y,z,h) in faces:
                center = (x + z//2, y + h//2)
                frame = cv2.ellipse(frame, center, (z//2, h//2), 0, 0, 360, (255, 0, 255), 4)
                # frame = cv2.rectangle(frame, (x, y), (x+z, y+h), (225, 0, 0), 2)
                # cv2.putText(frame, self.name, (x + 6, y - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # FlippedImage = cv2.flip(rgbImage, 1)
            # print(frame.shape[:2])
            
            self.convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1],rgbImage.shape[0], QImage.Format_RGB888)
            p = self.convertToQtFormat.scaled(*frame.shape[:2], Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

    def facerec(self,frame,encode_list_known,names,name,imgs):
        faces_cur_frame = face_recognition.face_locations(imgs)
        encodes_cur_frame = face_recognition.face_encodings(imgs, faces_cur_frame)
        # count = 0
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            name = "unknown"
            match = face_recognition.compare_faces(self.encode_list, encodeFace, tolerance=0.60)
            face_dis = face_recognition.face_distance(self.encode_list, encodeFace)
            best_match_index = np.argmin(face_dis)
            # print("s",best_match_index)
            # print(self.name)
            if match[best_match_index]:
                name = names[best_match_index].upper()
                print(name)
                # time.sleep(10)

    def run(self):
        self.main(self.Cap,self.camcount)

    def changeindex(self,index):
        self.index = index 
        self.ThreadActive = False
        print(self.isFinished())


# class faceDetect(QtConcurent):
#     """docstring for FaceDetect"""
#     def __init__(self,imgs,encode_list,names,name):
#         super().__init__()
#         self.imgs = imgs
#         self.encode_list = encode_list
#         self.names = names
#         self.name = name
#     def run(self):
#         # face recognition
#         faces_cur_frame = face_recognition.face_locations(self.imgs)
#         encodes_cur_frame = face_recognition.face_encodings(self.imgs, faces_cur_frame)
#         # count = 0
#         for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
#             self.name = "unknown"
#             match = face_recognition.compare_faces(self.encode_list, encodeFace, tolerance=0.60)
#             face_dis = face_recognition.face_distance(self.encode_list, encodeFace)
#             best_match_index = np.argmin(face_dis)
#             # print("s",best_match_index)
#             # print(self.name)
#             if match[best_match_index]:
#                 self.name = self.names[best_match_index].upper()
#                 print(self.name)
#                 # y1, x2, y2, x1 = (i*4 for i in faceLoc)
#                 # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 # cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 255, 0), cv2.FILLED)
#                 # cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

        # for i in range(5):
        #     time.sleep(10)
        #     print('aye')
            






# just recommeded way to run program just follow this 
if __name__ == "__main__":
    App = QApplication(sys.argv) # this is for closing the app
    # calling MainWindow class and just showing it 
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
