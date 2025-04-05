# utils.py
import os
from PyQt5 import QtCore, QtGui, QtWidgets

def set_background(background):
    background.setScaledContents(True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "images/background/pond_background.jpg")
    background.setPixmap(QtGui.QPixmap(background_path))

def blue_background_White_text(button):
    button.setStyleSheet("background-color: #78CFE2; color: black; border-radius: 15px;border: 8px solid black")

def text_blue(text):
    # text.setStyleSheet("color: #1E2F97;")background-color: #f5fbfb;
    # text.setStyleSheet(" color: black; border-radius: 15px;border: 2px solid #8e9387")
    text.setStyleSheet("background-color: rgba(251, 247, 245, 150); color: black; border-radius: 15px;")

def simulation_explanation_change(label, color):
    label.setStyleSheet(f'border: 12px solid {color}; padding: 10px;background-color: rgba(120, 207, 226, 200); color: black; border-radius: 15px;')

# used for the slider in the simulation page
def slider(slider):
    slider.setStyleSheet("""
        QSlider::groove:vertical {
            background: #37A8C8;  /* Change this to your desired color */
            width: 20px;  /* Adjust the width of the pole */
        }

        QSlider::handle:vertical {
            background: #CBEDEE;  /* Change this to your desired color */
            border: 5px solid #37A8C8;
            height: 80px;  /* Adjust the height of the slider handle */
            width: 25px;  /* Adjust the width of the slider handle */
            margin: -30px;  /* Move the slider handle in/out */
            border-radius: 35px;  /* Make the handle circular */
        }
        """)
    
# Live Data Section 
def water_background(background):
    background.setScaledContents(True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "images/background/water_background.jpeg")
    # background_path = os.path.join(current_dir, "images/water.png")
    background.setPixmap(QtGui.QPixmap(background_path))

def new_image(image, file):
    image.setScaledContents(True)
    filepath = f'images/liveData/{file}'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, filepath)
        # self.background.setPixmap(QtGui.QPixmap(".\\../src/ui/water_background.jpeg"))
    image.setPixmap(QtGui.QPixmap(background_path))

# different color combinations for the classroom 
def classroom_background(background):
    background.setScaledContents(True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "images/background/Classroom.png")
        # self.background.setPixmap(QtGui.QPixmap(".\\../src/ui/water_background.jpeg"))
    background.setPixmap(QtGui.QPixmap(background_path))

def class_buttons(button):
    button.setStyleSheet("background-color: #fff3d1; color: #bc6033; border-radius: 15px; border: 8px solid #f2a20c;")

def class_chalkbaord(text):
    text.setStyleSheet("color: #fbf7f5;")


def how_pol_background(background, path):
    background.setScaledContents(True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, path)
        # self.background.setPixmap(QtGui.QPixmap(".\\../src/ui/water_background.jpeg"))
    background.setPixmap(QtGui.QPixmap(background_path))

def how_pol_button(button):
    button.setStyleSheet("background-color: #A8CC5C; color: black; border-radius: 15px; border: 8px solid black;")

def how_pol_text(text):
    text.setStyleSheet("background-color: rgba(251, 247, 245, 150); color: black; border-radius: 15px;")

def archie_arm_out(archie):
    archie_set(archie, "images/archie/archie_one_arm.png")

def archie_arm_out_teach(archie):
    archie_set(archie, "images/archie/archie_one_arm_teach.png")

def archie_arm_out_quiz(archie):
    archie_set(archie, "images/archie/archie_one_arm_quiz.png")

def archie_arms_out(archie):
    archie_set(archie, "images/archie/archie_arms_out.png")

def archie_arms_out_quiz(archie):
    archie_set(archie, "images/archie/archie_arms_out_quiz.png")

def archie_arms_out_teach(archie):
    archie_set(archie, "images/archie/archie_arms_out_teach.png")

def archie_arms_down(archie):
    archie_set(archie, "images/archie/archie_arms_down.png")    

def archie_arms_down_teach(archie):
    archie_set(archie, "images/archie/archie_arms_down_teach.png")    

def archie_arms_down_quiz(archie):
    archie_set(archie, "images/archie/archie_arms_down_quiz.png")    

def archie_sampling(archie):
    archie_set(archie, "images/archie/archie_sampling_happy.png")

def archie_sampling_nervous(archie):
    archie_set(archie, "images/archie/archie_sampling_nervous.png")

def archie_sampling_bad(archie):
    archie_set(archie, "images/archie/archie_sampling_bad.png")

def archie_set(archie, path):
    archie.setScaledContents(True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, path)
    archie.setPixmap(QtGui.QPixmap(background_path))


