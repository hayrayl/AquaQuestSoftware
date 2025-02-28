# utils.py
import os
from PyQt5 import QtCore, QtGui, QtWidgets

def test():
    print("Test")

def set_background(background):
    background.setScaledContents(True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "images/water_background.jpeg")
    # self.background.setPixmap(QtGui.QPixmap(".\\../src/ui/water_background.jpeg"))
    background.setPixmap(QtGui.QPixmap(background_path))

def blue_background_White_text(button):
    button.setStyleSheet("background-color: #1E2F97; color: #CFF0F3; border-radius: 15px;")

def text_blue(text):
    text.setStyleSheet("color: #1E2F97;")

def simulation_explanation_change(label, color):
    label.setStyleSheet(f'border: 12px solid {color}; padding: 10px;background-color: #1E2F97; color: #CFF0F3 ; border-radius: 15px;')

def slider(slider):
    slider.setStyleSheet("""
        QSlider::groove:vertical {
            background: #CFF0F3;  /* Change this to your desired color */
            width: 20px;  /* Adjust the width of the pole */
        }

        QSlider::handle:vertical {
            background: #1E2F97;  /* Change this to your desired color */
            border: 5px solid #CFF0F3;
            height: 100px;  /* Adjust the height of the slider handle */
            width: 20px;  /* Adjust the width of the slider handle */
            margin: -40px;  /* Move the slider handle in/out */
            border-radius: 45px;  /* Make the handle circular */
        }
        """)

