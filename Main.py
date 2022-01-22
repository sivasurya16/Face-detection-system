import sys
from pathlib import Path

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import json,pickle,cv2,face_recognition

from Modules import *


def encode_faces():
    # make required directories if it doesn't exist
    Path('pictures').mkdir(parents=True, exist_ok=True)
    Path('encodings/names.json').touch(exist_ok=True)
    Path('encodings/encodings.dat').touch(exist_ok=True)


    # faces encondings and names
    images = []
    names = []
    encode_list = []
    users = list(Path('pictures').iterdir())

    def update(images,encode_list):
        # encoding images
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
            encode_list.append(encodes_cur_frame)
        with open('encodings/encodings.dat','wb') as f:
            pickle.dump(encode_list, f)

    # Get users in pictures folder
    for user in users:
        cur_img = cv2.imread(f'{user}')
        images.append(cur_img)
        names.append(user.stem)

    # Add encodings to respective files
    with open('encodings/names.json','r+') as f:
        data = f.read()
        f.seek(0)
        if not data:
            json.dump(names, f)
            print('Adding data for 1st time')
            update(images, encode_list)

        elif len(json.loads(data))!= len(names):
            json.dump(names, f)
            update(images, encode_list)
            print('Updating data')
        
        else:
            print('Encodings already in latest version')


class AddWindow(AddPicture.Ui_add_pic,QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(431,460)
        self.setupUi(self)
        self.browseButton.clicked.connect(self.file_browser)
        self.nameLabel.textEdited.connect(self.checker)
        self.addButton.clicked.connect(self.add_button)
        self.addButton.setEnabled(False)
        self.updated = False

    def checker(self):
        if len(self.nameLabel.text()) and len(self.showDir.toPlainText()):
            self.addButton.setEnabled(True)
        else:
            self.addButton.setEnabled(False)

    def add_button(self):
        picture = Path(self.showDir.toPlainText())
        data = open(picture,'rb').read()
        with open(f'pictures/{self.nameLabel.text()}{picture.suffix}','wb') as f:
            f.write(data)
            self.updated = True
        
        # Message box stuff
        msg = QMessageBox()
        icon = QIcon()
        icon.addPixmap(QPixmap("UI_Files\\facial-recognition.png"), QIcon.Normal, QIcon.Off)
        msg.setWindowIcon(icon)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('info')
        msg.setText("Picture added!!")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
        msg.exec()        

    def file_browser(self):
        fname,_ = QFileDialog.getOpenFileName(self, "Select Picture", "", "JPG Files (*.jpg);; PNG Files (*.png);;JPEG Files (*.jpeg)")
        self.picture = QPixmap(fname)
        self.size = self.pictureLabel.width(),self.pictureLabel.height()
        self.pictureLabel.setPixmap(self.picture.scaled(*self.size,Qt.KeepAspectRatio))
        if fname:
            self.showDir.setText(fname)          
        else:
            self.showDir.setText('')
            self.addButton.setEnabled(False)

    def closeEvent(self, event):
        if self.updated:
            encode_faces()           
        Root.show()



class AboutWindow(AboutUs.Ui_Dialog,QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(432,421)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self) 


class FaceWindow(FaceGui.MainWindow):
    def __init_(self):
        super().__init__()

    def closeEvent(self, event):
        super().closeEvent(event)            
        Root.show()


class MainWindow(startWindow.Ui_MainWindow,QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None  # External window slot.

        self.setFixedSize(606, 499)
        self.setupUi(self) 
        
        self.Start.clicked.connect(self.face_detect_window)
        self.About.clicked.connect(self.About_window)
        self.addPicture.clicked.connect(self.Add_window)

    def Add_window(self,checked):
        self.w = AddWindow()
        self.w.show()
        self.close()

    def About_window(self, checked):
        self.w = AboutWindow()
        self.w.exec()

    def face_detect_window(self,checked):
        self.w = FaceWindow()
        self.w.show()
        self.close()


encode_faces()
app = QApplication(sys.argv)
Root = MainWindow()
Root.show()
app.exec()