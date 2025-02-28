import sys 
import os 
from PyQt5 import QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
from quiz import UI_quiz 

class QuizScreen(QtWidgets.QWidget, UI_quiz):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Used to know what question we are on 
        self.count = 0 

        self.questions = self.parse_questions()
        # question, options, correct, explantion = self.questions[0]
        self.design_setup()
        self.new_question()
        self.pushButton_back.clicked.connect(self.go_back)

        self.pushButton_Q_answer1.clicked.connect(lambda: self.check_answer(number=1))
        self.pushButton_Q_answer2.clicked.connect(lambda: self.check_answer(number=2))
        self.pushButton_Q_answer3.clicked.connect(lambda: self.check_answer(number=3))
        self.pushButton_Q_next.clicked.connect(lambda: self.next())

    def go_back(self):
        self.parent().setCurrentIndex(0)  

    def design_setup(self):
        utils.set_background(self.background)

        utils.text_blue(self.label_Q_question)
        utils.text_blue(self.label_Q_results)
        utils.blue_background_White_text(self.pushButton_Q_answer1)
        utils.blue_background_White_text(self.pushButton_Q_answer2)
        utils.blue_background_White_text(self.pushButton_Q_answer3)
        utils.blue_background_White_text(self.pushButton_back)
        utils.blue_background_White_text(self.pushButton_Q_next)

    def new_question(self):

        if self.count < len(self.questions):
            question, options, correct, explantion = self.questions[self.count]

            self.label_Q_question.setText(question)
            self.label_Q_results.setText("")
            self.pushButton_Q_answer1.setText(options[0])
            self.pushButton_Q_answer2.setText(options[1])
            self.pushButton_Q_answer3.setText(options[2])
        else:
            self.label_Q_question.setText("")
            self.label_Q_results.setText("That is the end of the Quiz! Thank you for learning with me!")
            self.pushButton_Q_answer1.hide()
            self.pushButton_Q_answer2.hide()
            self.pushButton_Q_answer3.hide()            

        self.pushButton_Q_next.hide()

    def parse_questions(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "../quizes/question1.txt")


        with open(file_path, 'r') as file:
            content = file.read().strip().split('\n\n')  # Split by double newlines to separate question blocks

        questions = []
        for block in content:
            lines = block.strip().split('\n')
            question = lines[0]
            options = lines[1:4]
            correct = int(lines[4])   
            explanation = lines[5]
            questions.append((question, options, correct, explanation))

        return questions

    def check_answer(self, number):
        question, options, correct, explantion = self.questions[self.count]
        print(correct)

        if(number == int(correct)):
            self.label_Q_results.setText(explantion)
            self.pushButton_Q_next.show()
        else:
            self.label_Q_results.setText("Incorrect. Try again! You've got this!")

    def next(self):
        print("Next button")
        self.count += 1 
        self.new_question()


    def showEvent(self, event):
        super().showEvent(event)
        self.count = 0  # Reset count when the screen is shown
        self.new_question()  # Load the first question again
    
        
