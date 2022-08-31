import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Window(QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        
        self.resize(300, 150)
        self.setWindowTitle("ScreenRuler")

        self.pushButton = QPushButton("Open", self)
        self.pushButton.setFont(QFont("Arial", 15))
        self.pushButton.setGeometry(5, 5, 80, 80)
        self.pushButton.clicked.connect(self.openBase)
        
        self.heightEntry = QLineEdit(self)
        self.heightEntry.setFont(QFont("Arial", 10))
        self.heightEntry.setValidator(QIntValidator())
        self.heightEntry.setGeometry(90, 5, 200, 40)
        self.heightEntry.setText("120")

        self.base = Base(int(self.heightEntry.text()))

    def openBase(self):
        self.base.updateViewHeight(int(self.heightEntry.text()))
        self.base.show()


class Base(QWidget):
    def __init__(self, height, parent = None):
        super(Base, self).__init__(parent)
        self.app = QApplication(sys.argv)
        self.screen = self.app.primaryScreen()
        self.size = self.screen.availableSize()

        self.width = self.size.width()
        self.height = self.size.height()
        self.viewHeight = height
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.move(0, 0)
        self.resize(self.width, self.height)
        self.setMouseTracking(True)

        self.tracker = QWidget(self)
        self.tracker.setGeometry(0, 0, self.width, self.viewHeight)
        self.tracker.setStyleSheet("background-color: white;")
        self.tracker.setGraphicsEffect(QGraphicsOpacityEffect(opacity=0.01))
        self.tracker.setMouseTracking(True)

        self.overlayTop = QWidget(self)
        self.overlayTop.setGeometry(0, 0, self.width, self.height)
        self.overlayTop.setStyleSheet("background-color: black;")
        self.overlayTop.setGraphicsEffect(QGraphicsOpacityEffect(opacity=0.9))
        self.overlayTop.setMouseTracking(True)

        self.overlayBot = QWidget(self)
        self.overlayBot.setGeometry(0, 0, self.width, self.height)
        self.overlayBot.setStyleSheet("background-color: black;")
        self.overlayBot.setGraphicsEffect(QGraphicsOpacityEffect(opacity=0.9))
        self.overlayBot.setMouseTracking(True)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, event):
        self.cursorPos = (event.x(), event.y())
        self.tracker.move(0, event.y()-(self.viewHeight/2))
        self.overlayTop.move(0, event.y()-(self.viewHeight/2)-self.height)
        self.overlayBot.move(0, event.y()+(self.viewHeight/2))
    
    def updateViewHeight(self, height):
        self.viewHeight = height



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
