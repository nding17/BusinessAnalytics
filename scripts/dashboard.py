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
import pandas as pd

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
        
        self.module_idx = 0
        self.tracker_idx = 0

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
        self.module_idx = i
    
    def select_tracker(self, i):
        self.tracker_idx = i
    
    def regi_hist(self,course):
        df_student_regi = pd.read_csv("../../data/studentRegistration.csv")
        group = df_student_regi.groupby(['code_module']).get_group(course)
        ax = group['date_registration'].hist(cumulative=True, histtype='bar')
        ax.set_xlabel('registration date (relative to day 0)')
        ax.set_ylabel('learners (cumulative)')
        ax.set_title(f'Course Module - {course}')
        
    def progress_plot(self,course):
        df_stu_assess = pd.read_csv('../../data/studentAssessment.csv')
        df_assess = pd.read_csv('../../data/assessments.csv')
        df_assess_merged = pd.merge(df_stu_assess, df_assess[['code_module', 'id_assessment']], 
                            on='id_assessment', how='left')
        
        ids = df_assess_merged[df_assess_merged['code_module'] == course]['id_assessment'].unique()        
        total = len(ids)
        progress = []
        
        students = df_assess_merged['id_student'].unique()
        df_module = df_assess_merged[df_assess_merged['code_module']==course]
        for s in students:
            prog = df_module[df_module['id_student']==s]['id_assessment'].unique().shape[0]
            for i in range(prog):
                progress.append(i/total)
        
        progress.sort(reverse=False)
        ax = pd.Series(progress).hist(cumulative=False, histtype='bar', bins=5)
        ax.set_xlabel('course progress in proportion')
        ax.set_ylabel('number of learners')
        ax.set_title(f'Course Module - {course}')
    
    def grade_boxplot(self,course):
        df_stu_assess = pd.read_csv('../../data/studentAssessment.csv')
        df_assess = pd.read_csv('../../data/assessments.csv')
        df_assess_merged = pd.merge(df_stu_assess, df_assess[['code_module', 'id_assessment']], 
                            on='id_assessment', how='left')
        df_course = df_assess_merged[df_assess_merged['code_module']==course]
        ax = df_course.boxplot(by='id_assessment', column=['score'], grid=False)
        ax.set_xlabel('course ID')
        ax.set_ylabel('score')
        ax.set_title(f'Course Module - {course}')

    def plot(self):
        self.figure.clear()
        plots = [self.regi_hist, self.progress_plot, self.grade_boxplot]
        course_modules = ['AAA','BBB','CCC','DDD','EEE','FFF','GGG']
        
        plots[self.tracker_idx](course_modules[self.module_idx])
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