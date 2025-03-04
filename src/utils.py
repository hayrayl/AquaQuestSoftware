# utils.py
import os
from PyQt5 import QtCore, QtGui, QtWidgets

def set_background(background):
    background.setScaledContents(True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "images/water.png")
    # background_path = os.path.join(current_dir, "images/water_background.jpeg")
    # self.background.setPixmap(QtGui.QPixmap(".\\../src/ui/water_background.jpeg"))
    background.setPixmap(QtGui.QPixmap(background_path))

def blue_background_White_text(button):
    button.setStyleSheet("background-color: #1E2F97; color: #FFFFFF; border-radius: 15px;")

def text_blue(text):
    text.setStyleSheet("color: #1E2F97;")

def simulation_explanation_change(label, color):
    label.setStyleSheet(f'border: 12px solid {color}; padding: 10px;background-color: #1E2F97; color: #FFFFFF; border-radius: 15px;')

# used for the slider in the simulation page
def slider(slider):
    slider.setStyleSheet("""
        QSlider::groove:vertical {
            background: #B1E3FA;  /* Change this to your desired color */
            width: 20px;  /* Adjust the width of the pole */
        }

        QSlider::handle:vertical {
            background: #00bcf2;  /* Change this to your desired color */
            border: 5px solid #B1E3FA;
            height: 100px;  /* Adjust the height of the slider handle */
            width: 20px;  /* Adjust the width of the slider handle */
            margin: -40px;  /* Move the slider handle in/out */
            border-radius: 45px;  /* Make the handle circular */
        }
        """)
    

# different color combinations for the classroom 
def classroom_background(background):
    background.setScaledContents(True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "images/classroom.png")
        # self.background.setPixmap(QtGui.QPixmap(".\\../src/ui/water_background.jpeg"))
    background.setPixmap(QtGui.QPixmap(background_path))

def class_buttons(button):
    button.setStyleSheet("background-color: #fff3d1; color: #bc6033; border-radius: 15px; border: 8px solid #f2a20c;")

def class_chalkbaord(text):
    text.setStyleSheet("color: #fbf7f5;")

