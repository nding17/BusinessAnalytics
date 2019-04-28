from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class LearnerTabs(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Learning Analytics Dashboard")

        tabwidget = QTabWidget()
        tabwidget.addTab(ProgressTab(), "Progress")
        tabwidget.addTab(PerformanceTab(), "Performance")
        tabwidget.addTab(BehaviorTab(), "Behavior")

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(tabwidget)

        self.setLayout(vboxLayout)

class ProgressTab(QWidget):
     def __init__(self):
         super().__init__()
 
         filenameLabel = QLabel("Name:")
         fileNameEdit = QLineEdit()
 
         dob = QLabel("Birth Date:")
         dobedit = QLineEdit()
 
         age = QLabel("Age:")
         ageedit = QLineEdit()
 
         PhoneNu = QLabel("Phone:")
         phonedit = QLineEdit()
 
         ftablayout = QVBoxLayout()
         ftablayout.addWidget(filenameLabel)
         ftablayout.addWidget(fileNameEdit)
         ftablayout.addWidget(dob)
         ftablayout.addWidget(dobedit)
         ftablayout.addWidget(age)
         ftablayout.addWidget(ageedit)
         ftablayout.addWidget(PhoneNu)
         ftablayout.addWidget(phonedit)
 
         self.setLayout(ftablayout)
    

class PerformanceTab(QWidget):
    def __init__(self, parent=None):
        super(PerformanceTab, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.comboBox = QComboBox()
        self.comboBox.addItem('Registration Tracking Board')
        self.comboBox.addItem('Learning Progress Tracking Board')
        self.comboBox.addItem('Performance Tracking Board')
        self.comboBox.addItem('Learning Behavior Tracking Board')
        self.comboBox.currentIndexChanged.connect(self.select_tracker)
        
        course_modules = ['AAA','BBB','CCC','DDD','EEE','FFF','GGG']
        self.moduleBox = QComboBox()
        for module in course_modules:
            self.moduleBox.addItem(f'Course Module - {module}')
        self.moduleBox.currentIndexChanged.connect(self.select_module)
        
        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.moduleBox)
        layout.addWidget(self.button)
        self.setLayout(layout)
    
    def select_module(self, i):
        pass
    
    def select_tracker(self, i):
        pass
    
    def regi_hist(self,course):
        import pandas as pd
        df_student_regi = pd.read_csv("../data/studentRegistration.csv")
        group = df_student_regi.groupby(['code_module']).get_group(course)
        ax = group['date_registration'].hist(cumulative=True, histtype='bar')
        ax.set_xlabel('registration date (relative to day 0)')
        ax.set_ylabel('learners (cumulative)')
        ax.set_title(f'Course Module - {course}')

    def plot(self):
        self.figure.clear()
        # create an axis
        #ax = self.figure.add_subplot(111)
        # discards the old graph
        #ax.hold(False) # deprecated, see above
        # plot data
        #ax.plot(data, '*-')
        self.regi_hist('AAA')
        # refresh canvas
        self.canvas.draw()

                

class BehaviorTab(QWidget):
    def __init__(self):
        super().__init__()


        label = QLabel("Terms And Conditions")
        listWidget = QListWidget()
        list = []

        for i in range(1,20):
            list.append("This Is Terms And Condition")

        listWidget.insertItems(0, list)
        checkBox = QCheckBox("Check The Terms And Conditions")


        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(listWidget)
        layout.addWidget(checkBox)
        self.setLayout(layout)