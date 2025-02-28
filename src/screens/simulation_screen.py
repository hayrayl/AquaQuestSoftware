import sys 
import os 
from PyQt5 import QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
from simulation import UI_simulation  # Import the generated UI class





class SimulationScreen(QtWidgets.QWidget, UI_simulation):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.design_setup()

        self.pushButton_back.clicked.connect(self.go_back)

        # Connect buttons to their respective functions
        self.pushButton_S_Temperature.clicked.connect(self.show_temperature)
        self.pushButton_S_Ph.clicked.connect(self.show_ph)
        self.pushButton_S_Turbidity.clicked.connect(self.show_turbidity)
        self.pushButton_S_HeavyMetals.clicked.connect(self.show_heavyMetals)

        # Initialize the simulation by showing temperature
        self.show_temperature()

    def design_setup(self):
        utils.set_background(self.background)
        utils.slider(self.sim_slider)

        utils.text_blue(self.label_S_CurrentSimulating)
        utils.text_blue(self.label_S_sliderValue)

        utils.blue_background_White_text(self.pushButton_back)
        utils.blue_background_White_text(self.pushButton_S_HeavyMetals)
        utils.blue_background_White_text(self.pushButton_S_Ph)
        utils.blue_background_White_text(self.pushButton_S_Temperature)
        utils.blue_background_White_text(self.pushButton_S_Turbidity)

        self.label_S_explanation.setWordWrap(True)
        utils.blue_background_White_text(self.label_S_explanation)

    def go_back(self):
        self.parent().setCurrentIndex(0)  # Assuming the main screen is at index 0 in the QStackedWidget

    def show_temperature(self):
        self.label_S_CurrentSimulating.setText("Temperature:")
        try:
            self.sim_slider.valueChanged.disconnect()  # Disconnect any previous connections
        except TypeError:
            pass  # Ignore if no connection exists
        self.sim_slider.valueChanged.connect(self.update_temperature)
        self.update_temperature(self.sim_slider.value())  # Update immediately to reflect current value

    def show_ph(self):
        self.label_S_CurrentSimulating.setText("Ph:")
        try:
            self.sim_slider.valueChanged.disconnect()  # Disconnect any previous connections
        except TypeError:
            pass  # Ignore if no connection exists
        self.sim_slider.valueChanged.connect(self.update_ph)
        self.update_ph(self.sim_slider.value())  # Update immediately to reflect current value

    def show_turbidity(self):
        self.label_S_CurrentSimulating.setText("Turbidity:")
        try:
            self.sim_slider.valueChanged.disconnect()  # Disconnect any previous connections
        except TypeError:
            pass  # Ignore if no connection exists
        self.sim_slider.valueChanged.connect(self.update_turbidity)
        self.update_turbidity(self.sim_slider.value())  # Update immediately to reflect current value
    
    def show_heavyMetals(self):
        self.label_S_CurrentSimulating.setText("Heavy Metals:")
        try:
            self.sim_slider.valueChanged.disconnect()
        except TypeError:
            pass
        self.sim_slider.valueChanged.connect(self.update_heavyMetals)
        self.update_heavyMetals(self.sim_slider.value())

    def update_temperature(self, value):
        self.label_S_sliderValue.setText(f"{value} °F")

        if value < 32:
            self.label_S_explanation.setText("Water is frozen and generally considered safe from bacterial contamination. However, other contaminants may still be present.")
            self.border_darkblue()
        elif 32 <= value <= 39:
            self.label_S_explanation.setText("Water is cold. Bacterial growth is slow, but chemical contaminants may still be present.")
            self.border_blue()
        elif 40 <= value <= 60:
            self.label_S_explanation.setText("Water is at a cool temperature. Some bacteria can start to grow, but contamination risk is moderate.")
            self.border_green()
        elif 61 <= value <= 75:
            self.label_S_explanation.setText("Water is at a mild temperature. This is an optimal range for bacterial growth, and the risk of contamination increases.")
            self.border_yellow()
        elif 76 <= value <= 95:
            self.label_S_explanation.setText("Water is warm. Bacterial and microbial contamination risk is high. Chemical contaminants may also be present.")
            self.border_orange()
        elif value > 95:
            self.label_S_explanation.setText("Water is hot. Some bacteria may be killed at these temperatures, but others can thrive, and chemical contamination is still a concern.")
            self.border_red()
        else:
            self.label_S_explanation.setText("Water temperature is unknown.")
            self.border_none()
            

    def update_ph(self, value):
        ph = value * 0.14  # Adjust according to your slider range
        self.label_S_sliderValue.setText(f"{ph:.1f} pH")

        if ph < 3.0:
            self.label_S_explanation.setText("Water is highly acidic. Unsafe for most aquatic life and can cause severe health issues.")
            self.border_red()
        elif 3.0 <= ph < 6.0:
            self.label_S_explanation.setText("Water is acidic. Unsafe for many aquatic organisms and can cause irritation or health problems.")
            self.border_orange()
        elif 6.0 <= ph <= 8.5:
            self.label_S_explanation.setText("Water is neutral. Safe for drinking and most aquatic life.")
            self.border_green()
        elif 8.5 < ph <= 12.0:
            self.label_S_explanation.setText("Water is alkaline. May be unsafe for some aquatic life and can cause health issues.")
            self.border_yellow()
        elif ph > 12.0:
            self.label_S_explanation.setText("Water is highly alkaline. Unsafe for most aquatic life and can cause severe health issues.")
            self.border_red()
        else:
            self.label_S_explanation.setText("Water pH level is unknown.")
            self.border_none()

    def update_turbidity(self, value):
        turbidity = int(value * 0.6)

        self.label_S_sliderValue.setText(f"{turbidity} NTU")

        if turbidity <= 5:
            self.label_S_explanation.setText("Water is clear. Safe for drinking and most aquatic life.")
            self.border_green()
        elif 6 <= turbidity <= 25:
            self.label_S_explanation.setText("Water is slightly cloudy. Generally safe but may affect some sensitive aquatic organisms.")
            self.border_yellow()
        elif 26 <= turbidity <= 50:
            self.label_S_explanation.setText("Water is cloudy. Unsafe for drinking and may harm aquatic life.")
            self.border_orange()
        elif turbidity > 50:
            self.label_S_explanation.setText("Water is very cloudy. Unsafe for drinking and harmful to most aquatic life.")
            self.border_red()
        else:
            self.label_S_explanation.setText("Water turbidity level is unknown.")
            self.border_none()

    def update_heavyMetals(self,value):
        heavyMetals = int(value * 0.6)

        self.label_S_sliderValue.setText(f"{heavyMetals} ppb")

        if heavyMetals <= 5:
            self.label_S_explanation.setText("Heavy metals concentration is low. Water is safe for drinking and most aquatic life.")
            self.border_green()
        elif 6 <= heavyMetals <= 25:
            self.label_S_explanation.setText("Heavy metals concentration is slightly elevated. Generally safe for most purposes, but caution is advised.")
            self.border_yellow()
        elif 26 <= heavyMetals <= 50:
            self.label_S_explanation.setText("Heavy metals concentration is high. Unsafe for drinking and harmful to aquatic life")
            self.border_orange()
        elif heavyMetals > 50:
            self.label_S_explanation.setText("Heavy metals concentration is very high. Unsafe for drinking and highly toxic to most aquatic life.")
            self.border_red()
        else:
            self.label_S_explanation.setText("Heavy metal level is unknown.")
            self.border_none()

    def border_green(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#84DC7D")

    def border_darkblue(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#81C4FB")

    def border_blue(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#81FBF5")

    def border_orange(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#F6B14E")
    
    def border_yellow(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#F5F57E")
    
    def border_red(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#D40407")

    def border_none(self):
        utils.simulation_explanation_change(self.label_S_explanation,"#1E2F97")
    