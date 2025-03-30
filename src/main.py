import sys
from PyQt5 import QtWidgets
from screens.home_screen import HomeScreen  
from screens.simulation_screen import SimulationScreen 
from screens.learning_screen import LearningScreen
from screens.live_data_screen import LiveDataScreen
from screens.quiz_screen import QuizScreen
from screens.learning_modules.classroom_screen import ClassroomScreen
from screens.learning_modules.how_pollutants_screen import HowPolluteScreen


# Index for which screen: 
# 0 : home 
# 1 : simulation 
# 2 : live data 
# 3 : quiz 
# 4 : learning modules 
# 5 : Classroom Learning Module 
# 6 : How water become poluted Learning Module 

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.home_screen = HomeScreen(self)
        self.simulation_screen = SimulationScreen(self)
        self.live_data_screen = LiveDataScreen(self)
        self.quiz_screen = QuizScreen(self)
        self.learning_screen = LearningScreen(self)
        self.classroom_screen = ClassroomScreen(self)
        self.howPollute_screen = HowPolluteScreen(self)
        
        self.stackedWidget.addWidget(self.home_screen)          # 0
        self.stackedWidget.addWidget(self.simulation_screen)    # 1
        self.stackedWidget.addWidget(self.live_data_screen)     # 2
        self.stackedWidget.addWidget(self.quiz_screen)          # 3
        self.stackedWidget.addWidget(self.learning_screen)      # 4
        self.stackedWidget.addWidget(self.classroom_screen)     # 5 
        self.stackedWidget.addWidget(self.howPollute_screen)    # 6 

        self.stackedWidget.setCurrentIndex(0)

        self.resize(1024,600) # setting the size of the screen 
        self.setMaximumSize(1024,600)
        
    def setIndex(self, index):
        self.stackedWidget.setCurrentIndex(int(index))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
