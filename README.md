# Archie's AquaQuest: Water Sampling Educational UI

## Project Overview
Archie’s AquaQuest is an interactive water quality testing and education platform designed for children. It combines environmental science, sensor integration, and gamified learning through a touchscreen-based GUI powered by a Raspberry Pi. The project includes data acquisition, simulation, testing walkthroughs, and quizzes—all led by Archie, an alligator snapping turtle, an endangered species native to Indiana.

## Features
- **Learning Modules**  
  Interactive screens that teach about water quality parameters (like pH, temperature, TDS, turbidity, nitrates, nitrites, heavy metals), how water gets polluted, and why testing is important. 

- **Live Data Collection**  
  Guides the user through setting up and calibrating sensors, then collects data in real time using sensors (via ADS1263 ADC) and test strips. Visuals, sensor animations, and explanations update dynamically.

- **Simulation Mode**  
  Allows students to adjust parameters using a slider and see how Archie reacts. Each parameter change triggers threshold-based mood updates and educational messaging.

- **Quiz Mode**  
  A fun, multiple-choice quiz led by Archie that reinforces learning with feedback and humor. Designed for younger students.

- **Archie the Mascot**  
  Appears throughout the interface with different animations and emotional states (happy, nervous, scared) based on water quality thresholds. 

## File Structure
```
project-root/
│
├── main.py                        # Entry point for the GUI (manages screens via QStackedWidget)
├── ui/                            # Auto-generated .py files from Qt Designer .ui files
├── screens/                       # Contains all screen Python files
│   ├── home_screen.py
│   ├── intro_screen.py
│   ├── learning_screen.py
│   ├── classroom_screen.py
│   ├── how_pollutants_screen.py
│   ├── live_data_screen.py
│   ├── test_strips_screen.py
│   ├── analyze_screen.py
│   └── simulation_screen.py
│
├── materials/                     # Educational and data text files
│   ├── parameters.txt
│   ├── how_pollute.txt
│   ├── why_test.txt
│   ├── thresholds.txt
│   └── question1.txt
│
├── images/                        # Backgrounds, Archie animations, test strip photos
├── AD_HAT/                        # SensorReader class to interface with ADS1263 and sensors
├── utils.py                       # Utility functions for UI styling and image updates
└── README.md                      # This file
```

## Code and Development Info
### Python Version
Python 3.12.7

### Required Python Packages
```
PyQt5==5.15.11
PyQt5-Qt5==5.15.2
PyQt5_sip==12.17.0
PyQt5Designer==5.14.1
```

### Qt Designer Notes
To design new UI screens:
1. Run `designer` in the command line (after installing PyQt5Designer).
2. Save your layout as a `.ui` file.
3. Convert it to Python using:  
   `pyuic5 -x filename.ui -o filename.py`
   > ⚠️ This will overwrite the target `.py` file — make sure to commit or back up any manual changes before regenerating.

### Git Practices
- **Do not push directly to `main`.**
- Create a branch for your feature, push changes there, and submit a merge request for review.

## Educational Goal
This project was developed to introduce students to environmental science, electronics, and data interpretation through an engaging and interactive platform. Archie helps guide students through the journey of learning why clean water matters and how to test it.

## Authors
Purdue ECE Senior Design Team (Spring 2025)

## Contact
For questions or contributions, reach out to Haylie Rayl/hcrayl@purdue.edu or Ariana Hollis-Brau/ahollisb@purdue.edu.
