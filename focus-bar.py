import sys
from tokenize import Double
from unicodedata import decimal
import pynput
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# create app
app = QApplication(sys.argv)
screen = app.primaryScreen().size()
res = {
    "width": screen.width(),
    "height": screen.height()
}

# initialise overlays
overlay_top = QWidget()
overlay_bot = QWidget()

def create_overlays(x, y):
    """create overlays
    
    x : width of screen
    y : height of screen
    """

    opacity = float(opacity_input.text())
    view_height = int(height_input.text())
    print(view_height)

    # create top and bottom overlay
    # into variables defined above
    overlay_top.setGeometry(0, 0, x, y)
    overlay_top.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    overlay_top.setStyleSheet("background-color: black;")
    overlay_top.setWindowOpacity(opacity)
    overlay_top.show()
    
    overlay_bot.setGeometry(0, 0, x, y)
    overlay_bot.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    overlay_bot.setStyleSheet("background-color: black;")
    overlay_bot.setWindowOpacity(opacity)
    overlay_bot.show()

    on_move(0, view_height/2)

def on_move(x, y):
    view_height = int(height_input.text())
    overlay_top.move(0, y-res["height"]-(view_height/2))
    overlay_bot.move(0, y+(view_height/2))

def on_press(key):
    if key == pynput.keyboard.Key.esc:
        overlay_top.hide()
        overlay_bot.hide()

# mouse pos and esc button listeners
mouse_listener = pynput.mouse.Listener(on_move=on_move)
mouse_listener.start()
keyboard_listener = pynput.keyboard.Listener(on_press=on_press)
keyboard_listener.start()


# create base window
window = QWidget()
window.resize(400, 250)
window.setWindowTitle("focus bar")

# create start button
button = QPushButton("Start", window)
button.setGeometry(10, 10, 50, 50)
button.clicked.connect(lambda: create_overlays(res["width"], res["height"]))

# height input/validator
QLabel("Bar height:", window).move(70, 15)
height_input = QLineEdit(window)
height_input.insert("60")
height_val = QIntValidator().setRange(2, res["height"])
height_input.setValidator(height_val)
height_input.setGeometry(170, 10, 50, 20)

# opacity input/validator
QLabel("Overlay Opacity:", window).move(70, 35)
opacity_input = QLineEdit(window)
opacity_input.insert("0.8")
opacity_val = QDoubleValidator(bottom=0, top=1, decimals=2)
opacity_input.setValidator(opacity_val)
opacity_input.setGeometry(170, 35, 50, 20)
window.show()


app.exec()