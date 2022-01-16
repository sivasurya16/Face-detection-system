import sys
import device

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from Modules import AboutUs,FaceGui,startWindow


class AboutWindow(AboutUs.Ui_Dialog,QDialog):
    def __init__(self):
        super().__init__()
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
        
        self.setupUi(self) 
        
        self.Start.clicked.connect(self.face_detect_window)
        self.About.clicked.connect(self.About_window)

    def About_window(self, checked):
        self.w = AboutWindow()
        self.w.exec()

    def face_detect_window(self,checked):
        self.w = FaceWindow()
        self.hide()
        self.w.show()



app = QApplication(sys.argv)
Root = MainWindow()
Root.show()
app.exec()