import sys
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
    # create top and bottom overlay
    # into variables defined above
    overlay_top.setGeometry(0, 0, x, y)
    overlay_top.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    overlay_top.setStyleSheet("background-color: black;")
    overlay_top.setWindowOpacity(0.8)
    overlay_top.show()
    
    overlay_bot.setGeometry(0, 0, x, y)
    overlay_bot.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    overlay_bot.setStyleSheet("background-color: black;")
    overlay_bot.setWindowOpacity(0.8)
    overlay_bot.show()

# create base window
window = QWidget()
window.resize(400, 250)
window.setWindowTitle("focus bar")
# create button
button = QPushButton("Start", window)
button.move(50, 50)
button.clicked.connect(lambda: create_overlays(res["width"], res["height"]))
window.show()

def on_move(x, y):
    overlay_top.move(0, y-res["height"]-(100/2))
    overlay_bot.move(0, y+(100/2))

def on_press(key):
    if key == pynput.keyboard.Key.esc:
        overlay_top.hide()
        overlay_bot.hide()

# mouse pos and esc button listeners
mouse_listener = pynput.mouse.Listener(on_move=on_move)
mouse_listener.start()
keyboard_listener = pynput.keyboard.Listener(on_press=on_press)
keyboard_listener.start()

app.exec()