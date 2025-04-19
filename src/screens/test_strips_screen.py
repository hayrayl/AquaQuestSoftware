import sys 
import os 

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils

from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
from test_strips import Ui_test_strip  # Import the generated UI class

class TestStripScreen(QtWidgets.QWidget, Ui_test_strip):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Call the setupUi method

        self.pushButton_selection_1.clicked.connect(lambda: self.button_pressed(value = 0))
        self.pushButton_selection_2.clicked.connect(lambda: self.button_pressed(value = 1))
        self.pushButton_selection_3.clicked.connect(lambda: self.button_pressed(value = 2))
        self.pushButton_selection_4.clicked.connect(lambda: self.button_pressed(value = 3))
        self.pushButton_selection_5.clicked.connect(lambda: self.button_pressed(value = 4))
        self.pushButton_selection_6.clicked.connect(lambda: self.button_pressed(value = 5))
        self.pushButton_selection_7.clicked.connect(lambda: self.button_pressed(value = 6))

        self.pushButton_restart.clicked.connect(self.restart)
        self.pushButton_bottom.clicked.connect(self.go_to_live_data)

        self.data =  {
            "Nitrite": ["0.0", "0.5", "1.0", "5.0", "10", "25"],
            "Nitrate": ["0", "10", "25", "50", "100", "250", "500"],
            "Lead": ["0", "5", "15", "30", "50"],
            "Mercury": ["0", "0.002", "0.005", "0.01", "0.02", "0.04", "0.08"],
            "Chromium": ["0", "2", "5", "10", "30", "50", "100"],
            "Magnesium": ["25", "50", "100", "250", "425", "1000"],
            "Cadmium": ["0", "5", "15", "30", "60"],
            "Calcium": ["< 10", "25", "50", "100", "250", "425"]
        }

        self.images =  {
            "Nitrite": "nitrite_highlight.png",
            "Nitrate": "nitrate_highlight.png",
            "Lead": "lead_highlight.png",
            "Mercury": "mercury_highlight.png",
            "Chromium": "chromium_highlight.png",
            "Magnesium": "magnesium_highlight.png",
            "Cadmium": "cadium_highlight.png",
            "Calcium": "calcium_highlight.png"
        }

        self.count = 0

        self.results = {
            "Nitrite": "0",
            "Nitrate": "0",
            "Lead": "0",
            "Mercury": "0",
            "Chromium": "0",
            "Magnesium": "0",
            "Cadmium": "0",
            "Calcium": "0"
        }

        self.units = {
            "Nitrite": " ppm",
            "Nitrate": " ppm",
            "Lead": " ppb",
            "Mercury": " mg/L",
            "Chromium": " mg/L",
            "Magnesium": " mg/L",
            "Cadmium": " mg/L",
            "Calcium": " mg/L",
        }

        self.key_count = len(list(self.results.keys()))

        self.design_setup()

    # update the screen to display the options for button selection    
    def update_screen(self):

        if self.count == 8:
            self.get_results()
        else: 
            print(f'Counter in Update Screeen: {self.count}')
            key = list(self.data.keys())[self.count] 
            num_buttons = len(self.data[key])
            file = self.images[key]

            utils.new_image(image=self.label_image, file=file)

            self.label_title.setText(key)

            self.label_explanation_side.hide()
            self.pushButton_bottom.hide()

            self.pushButton_selection_1.show()
            self.pushButton_selection_2.show()
            self.pushButton_selection_3.show()
            self.pushButton_selection_4.show()
            self.pushButton_selection_5.show()

            self.pushButton_selection_1.setText(self.data[key][0])
            self.pushButton_selection_2.setText(self.data[key][1])
            self.pushButton_selection_3.setText(self.data[key][2])
            self.pushButton_selection_4.setText(self.data[key][3])
            self.pushButton_selection_5.setText(self.data[key][4])

            if num_buttons >= 6:
                self.pushButton_selection_6.show()
                self.pushButton_selection_6.setText(self.data[key][5])
            else: 
                self.pushButton_selection_6.hide()

            if num_buttons >= 7: 
                self.pushButton_selection_7.show()
                self.pushButton_selection_7.setText(self.data[key][6])
            else: 
                self.pushButton_selection_7.hide()

    # this will update the screen upon each entry of the screen 
    def showEvent(self, event):
        super().showEvent(event)  # Call the base class implementation
        self.update_screen()  # Run update_screen whenever this screen is shown

    # function to handle a selection that was made 
    def button_pressed(self, value):
        key = list(self.data.keys())[self.count] 

        # set the result 

        self.results[key] = self.data[key][value]

        print(self.results)
        self.count += 1

        if self.count == 2 or self.count == 8:
            self.show_results()
        elif self.count >= self.key_count:
            self.show_results()
        else:
            self.update_screen()

    # handle restarting the selections from the buttons 
    def restart(self):
        if self.count <= 2:
            self.count = 0
        else: 
            self.count = 2 
        print("RESTART PRESSED ")
        self.update_screen()

    # This will display the results 
    def show_results(self):
        keys = list(self.results.keys())

        print("Showing Results")
        self.pushButton_selection_1.hide()
        self.pushButton_selection_2.hide()
        self.pushButton_selection_3.hide()
        self.pushButton_selection_4.hide()
        self.pushButton_selection_5.hide()
        self.pushButton_selection_6.hide()
        self.pushButton_selection_7.hide()

        self.pushButton_bottom.show()
        self.label_explanation_side.show()

        if self.count == 2:
            txt = f'{keys[0]}: {self.results[keys[0]]}{self.units[keys[0]]}\n{keys[1]}: {self.results[keys[1]]}{self.units[keys[1]]}'
            file = "nitrate_bottle.jpg"
        else:
            txt = f'{keys[2]}: {self.results[keys[2]]}{self.units[keys[2]]}\n{keys[3]}: {self.results[keys[3]]}{self.units[keys[3]]}\n{keys[4]}: {self.results[keys[4]]}{self.units[keys[4]]}\n{keys[5]}: {self.results[keys[5]]}{self.units[keys[5]]}\n{keys[6]}: {self.results[keys[6]]}{self.units[keys[6]]}\n{keys[7]}: {self.results[keys[7]]}{self.units[keys[7]]}'
            file = "heavy_metal_bottle.png"

        utils.new_image(image=self.label_image, file=file)
        self.label_explanation_side.setText(txt)
        self.label_title.setText("Results")

    # return the result 
    def get_results(self):
        return self.results
    
    # return back to the live data section 
    def go_to_live_data(self):
        if self.count < 4:
            self.update_screen()
        else: 
            self.parentWidget().setCurrentIndex(7)  # Use parentWidget() to refer to QStackedWidget
    
    def design_setup(self):
        utils.water_background(self.background)

        utils.text_blue(self.label_title)
        utils.text_blue(self.label_explanation_side)
        utils.blue_background_White_text(self.pushButton_selection_1)
        utils.blue_background_White_text(self.pushButton_selection_2)
        utils.blue_background_White_text(self.pushButton_selection_3)
        utils.blue_background_White_text(self.pushButton_selection_4)
        utils.blue_background_White_text(self.pushButton_selection_5)
        utils.blue_background_White_text(self.pushButton_selection_6)
        utils.blue_background_White_text(self.pushButton_selection_7)
        utils.blue_background_White_text(self.pushButton_restart)
        utils.blue_background_White_text(self.pushButton_bottom)
