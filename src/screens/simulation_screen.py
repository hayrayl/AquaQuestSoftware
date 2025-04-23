import sys 
import os 
from PyQt5 import QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
from simulation import Ui_simulation_ui  # Import the generated UI class

class SimulationScreen(QtWidgets.QWidget, Ui_simulation_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.design_setup()

        self.pushButton_back.clicked.connect(self.go_back)

        self.thresholds, self.value_ranges = self.load_thresholds()

        self.current_param = "temperature"

        # Connect buttons to their respective functions
        self.pushButton_S_Temperature.clicked.connect(self.show_temperature)
        self.pushButton_S_Ph.clicked.connect(self.show_ph)
        self.pushButton_S_Turbidity.clicked.connect(self.show_turbidity)
        self.pushButton_S_TDS.clicked.connect(self.show_tds)
        self.pushButton_S_Nitrite.clicked.connect(self.show_nitrite)
        self.pushButton_S_Mercury.clicked.connect(self.show_mercury)

        # connect the slider movement 
        self.sim_slider.valueChanged.connect(self.update_slider_value)

        # Initialize the simulation by showing temperature
        self.show_temperature()

    def design_setup(self):
        utils.set_background(self.background)
        utils.slider(self.sim_slider)

        utils.text_blue(self.label_S_CurrentSimulating)
        utils.text_blue(self.label_S_sliderValue)

        utils.blue_background_White_text(self.pushButton_back)
        utils.blue_background_White_text(self.pushButton_S_TDS)
        utils.blue_background_White_text(self.pushButton_S_Ph)
        utils.blue_background_White_text(self.pushButton_S_Temperature)
        utils.blue_background_White_text(self.pushButton_S_Turbidity)
        utils.blue_background_White_text(self.pushButton_S_Mercury)
        utils.blue_background_White_text(self.pushButton_S_Nitrite)

        self.label_S_explanation.setWordWrap(True)
        utils.blue_background_White_text(self.label_S_explanation)

    def go_back(self):
        self.parent().setCurrentIndex(0)  # Assuming the main screen is at index 0 in the QStackedWidget


    def show_temperature(self):
        self.current_param = "temperature"
        self.label_S_CurrentSimulating.setText("Temperature:")
        self.label_S_CurrentSimulating.adjustSize()
        self.update_slider_value(self.sim_slider.value())

    def show_ph(self):
        self.current_param = "pH"
        self.label_S_CurrentSimulating.setText("Ph:")
        self.label_S_CurrentSimulating.adjustSize()
        self.update_slider_value(self.sim_slider.value())

    def show_turbidity(self):
        self.current_param = "turbidity"
        self.label_S_CurrentSimulating.setText("Turbidity:")
        self.label_S_CurrentSimulating.adjustSize()
        self.update_slider_value(self.sim_slider.value())

    def show_tds(self):
        self.current_param = "tds"
        self.label_S_CurrentSimulating.setText("TDS:")
        self.label_S_CurrentSimulating.adjustSize()
        self.update_slider_value(self.sim_slider.value())

    def show_nitrite(self):
        self.current_param = "nitrite"
        self.label_S_CurrentSimulating.setText("Nitrite:")
        self.label_S_CurrentSimulating.adjustSize()
        self.update_slider_value(self.sim_slider.value())

    def show_mercury(self):
        self.current_param = "mercury"
        self.label_S_CurrentSimulating.setText("Mercury:")
        self.label_S_CurrentSimulating.adjustSize()
        self.update_slider_value(self.sim_slider.value())


    def update_slider_value(self, slider_value):
        param = self.current_param.lower()

        # Get min/max from thresholds
        if param in self.value_ranges:
            min_val, max_val = self.value_ranges[param]
        else:
            min_val, max_val = 0, 100  # fallback

        # Scale slider (0–100) to true range
        scaled_value = min_val + (slider_value / 100.0) * (max_val - min_val)

        # Format for display
        if param == "ph":
            self.label_S_sliderValue.setText(f"{scaled_value:.1f}")
        elif param == "turbidity":
            self.label_S_sliderValue.setText(f"{int(scaled_value)} NTU")
        elif param == "tds":
            self.label_S_sliderValue.setText(f"{int(scaled_value)} ppm")
        elif param == "nitrite":
            self.label_S_sliderValue.setText(f"{scaled_value:.3f} ppm")
        elif param == "mercury":
            self.label_S_sliderValue.setText(f"{scaled_value:.3f} mg/L")
        else:  # temperature
            self.label_S_sliderValue.setText(f"{scaled_value:.1f} °F")

        
        self.label_S_sliderValue.setMaximumWidth(420)  # Set a maximum width (adjust to your needs)
        self.label_S_sliderValue.adjustSize()  # Resize within the constraints

        self.apply_threshold(param, scaled_value)

    def load_thresholds(self):
        thresholds = {}
        value_ranges = {}  
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "../materials/thresholds.txt")
        with open(filepath, 'r') as file:
            for line in file:
                if line.strip():
                    param, low, high, message, mood = line.strip().split(',', 4)
                    low = float(low)
                    high = float(high)
                    key = param.lower()
                    thresholds.setdefault(key, []).append({
                        'low': low,
                        'high': high,
                        'message': message,
                        'mood': mood.lower()
                    })

                    # Update range
                    if key not in value_ranges:
                        value_ranges[key] = [low, high]
                    else:
                        value_ranges[key][0] = min(value_ranges[key][0], low)
                        value_ranges[key][1] = max(value_ranges[key][1], high)

        return thresholds, value_ranges


    def border_green(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#84DC7D")
        utils.archie_sampling(self.archie)

    def border_darkblue(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#81C4FB")
        utils.archie_sampling(self.archie)

    def border_blue(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#81FBF5")
        utils.archie_sampling(self.archie)

    def border_orange(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#F6B14E")
        utils.archie_sampling_nervous(self.archie)
    
    def border_yellow(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#F5F57E")
        utils.archie_sampling_nervous(self.archie)
    
    def border_red(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#D40407")
        utils.archie_sampling_bad(self.archie)

    def border_none(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#1E2F97")
        utils.archie_sampling(self.archie)
    
    def apply_threshold(self, param, value):
        param = param.lower()
        thresholds = self.thresholds.get(param, [])
        for entry in thresholds:
            if entry['low'] <= value <= entry['high']:
                self.label_S_explanation.setText(entry['message'])
                self.set_border_by_mood(entry['mood'])
                return
        self.label_S_explanation.setText("No matching threshold found.")
        self.border_none()

    def set_border_by_mood(self, mood):
        if mood == 'happy':
            self.border_green()
        elif mood == 'nervous':
            self.border_yellow()
        elif mood == 'scared':
            self.border_red()
        else:
            self.border_none()
