# Drone Water Sampling UI Design

## Project Overview
This repository contains the user interface (UI) design for a senior design project focused on water sampling using a drone. The UI is developed using PyQt5 and provides features to support learning modules, live data readings, quizzes, and simulations related to water sampling.

## Features
- **Learning Modules:** Interactive modules to educate users about water sampling and related concepts.
- **Live Data Reading:** Real-time visualization of data collected during water sampling missions.
- **Quiz:** Assessment quizzes to test users' understanding of water sampling and environmental science.
- **Simulation:** Simulation tools to plan and practice water sampling missions.

### Python 3.12.7

### Python Packages 
PyQt5==5.15.11

PyQt5-Qt5==5.15.2

PyQt5_sip==12.17.0

PyQt5Designer==5.14.1

### Development Notes:
designer is a drag-and-drop used to get the layout. Once the package is installed, open a CLI and use the command "designer" and the UI will open up. This will save the file as a .ui file. to transform it into Python use the command "pyuic5 -x \fileName.ui -o fileName.py"
**warning**: this will override whatever was in the python file before. Make sure you are backing up to your branch. 

Do not directly push to the main branch. Create your own branch that you can push to first so that someone can check the merge request. 

let me know if you have any questions -Haylie 
