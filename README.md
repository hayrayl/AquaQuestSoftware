```markdown
# Archie's AquaQuest

Archie’s AquaQuest is an interactive water quality testing and education platform designed for children. It combines environmental science, sensor integration, and gamified learning through a touchscreen-based GUI powered by a Raspberry Pi. The project includes data acquisition, simulation, testing walkthroughs, and quizzes—all led by Archie, an alligator snapping turtle, an endangered species native to Indiana.

## Key Features

- **Live Sensor Data Collection**  
  Collect real-time measurements for:
  - pH
  - Temperature
  - Turbidity
  - TDS (Total Dissolved Solids)

- **Test Strip Analysis**  
  Input results from nitrate/nitrite and heavy metal test strips.

- **Interactive Learning Modules**
  - Explore what pollutes water
  - Learn why testing matters
  - Understand parameters through Archie’s chalkboard lessons

- **Simulation Module**
  - Adjust environmental conditions with a slider
  - See how parameters like temperature, pH, and heavy metals affect water health

- **Engaging Quiz System**
  - Multiple-choice questions with fun feedback
  - Educational reinforcement through humor and pop culture

- **Child-Friendly UI**
  - Large buttons, bright visuals, and guided walkthroughs with Archie as a host

---

## Getting Started

### Requirements

- Python 3.8+
- PyQt5
- Raspberry Pi 4 or 5 (Recommended)
- ADS1263 ADC HAT for sensor integration
- Sensors for:
  - Temperature (DS18B20)
  - Turbidity
  - TDS
  - pH
- Test strips for:
  - Nitrate/Nitrite
  - Lead, Mercury, Chromium, Magnesium, Cadmium, Calcium

### Installation

1. **Clone the repo:**

   ```bash
   git clone https://github.com/hayrayl/SeniorDesigUI.git
   cd archies-aquaquest
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the main application:**

   ```bash
   python main.py
   ```

---

## Project Structure

```plaintext
├── main.py                      # Entry point
├── screens/
│   ├── home_screen.py
│   ├── live_data_screen.py
│   ├── analyze_screen.py
│   ├── test_strips_screen.py
│   ├── quiz_screen.py
│   ├── simulation_screen.py
│   ├── learning_screen.py
│   ├── classroom_screen.py
│   └── how_pollutants_screen.py
├── materials/                  # Educational and threshold data
│   ├── parameters.txt
│   ├── how_pollute.txt
│   ├── why_test.txt
│   ├── question1.txt
│   └── thresholds.txt
├── ui/                         # PyQt5 UI files (converted from .ui)
├── images/                     # All background and asset images
├── utils.py                    # Shared functions for GUI styling and image loading
└── AD_HAT/
    └── sensorRead.py           # Functions for reading ADC sensor data
```

---

## Developer Notes

- Use `.showEvent()` methods to reset state when switching between screens.
- Data collected from `live_data_screen.py` and `test_strips_screen.py` is aggregated in `analyze_screen.py`.
- The quiz system reads from `materials/question1.txt` and dynamically parses the format.
- Threshold logic is centralized in `thresholds.txt` and supports dynamic color and mood responses from Archie.

---

## Credits

Created by a senior design team at Purdue University as an educational tool for teaching water quality testing and environmental awareness to students aged 8-12.

Archie, the alligator snapping turtle, is our mascot and guide. 

---

## Contact

For questions, reach out to Haylie Rayl/hcrayl@purdue.edu or Ariana Hollis-Brau/ahollisb@purdue.edu.

```
