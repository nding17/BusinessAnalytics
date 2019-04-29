from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableWidget
from PyQt5 import QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class LearnerTabs(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Learning Analytics Dashboard")

        tabwidget = QTabWidget()
        tabwidget.addTab(SupportTab(), "Support")
        tabwidget.addTab(AnalyticsTab(), "Analytics")
        tabwidget.addTab(TrackerTab(), "Tracking")

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(tabwidget)

        self.setLayout(vboxLayout)

class SupportTab(QWidget):
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
    

class AnalyticsTab(QWidget):
    def __init__(self, parent=None):
        super(AnalyticsTab, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.adjustSize()

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
        ax = pd.Series(progress).hist(cumulative=False, histtype='bar', bins=6)
        ax.set_xlabel('course progress in proportion')
        ax.set_ylabel('number of learners')
        ax.set_title(f'Course Module - {course}')
    
    def grade_boxplot(self,course):
        df_stu_assess = pd.read_csv('../../data/studentAssessment.csv')
        df_assess = pd.read_csv('../../data/assessments.csv')
        df_assess_merged = pd.merge(df_stu_assess, df_assess[['code_module', 'id_assessment']], 
                            on='id_assessment', how='left')
        df_course = df_assess_merged[df_assess_merged['code_module']==course]
        
        ax = sns.boxplot(x="id_assessment", y="score", data=df_course)
        ax.set_xlabel('course ID')
        ax.set_ylabel('score')
        ax.set_title(f'Course Module - {course}')


    def plot(self):
        self.figure.clear()
        plots = [self.regi_hist, self.progress_plot, self.grade_boxplot]
        course_modules = ['AAA','BBB','CCC','DDD','EEE','FFF','GGG']
        
        plots[self.tracker_idx](course_modules[self.module_idx])
        self.canvas.draw()

                
class TrackerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.studentID = QLabel("Student ID:          ")
        self.studentID_input = QLineEdit()
        self.module = QLabel("Course Module:          ")
                
        self.fileButton = QPushButton('Load File + Predict')
        self.fileButton.clicked.connect(self.choosefile)
        
        self.moduleBox = QComboBox()
        
        course_modules = ['AAA','BBB','CCC','DDD','EEE','FFF','GGG']

        for module in course_modules:
            self.moduleBox.addItem(f'Course Module - {module}')
        self.moduleBox.currentIndexChanged.connect(self.select_module)
        
        self.button = QPushButton('Predict')
        self.button.clicked.connect(self.predict)    
        
        self.result = QLabel()
        
        self.module_idx = 0
        self.data_file = ""
        
        ftablayout = QGridLayout()
        ftablayout.setSpacing(10)
        
        ftablayout.addWidget(self.studentID, 1,0)
        ftablayout.addWidget(self.studentID_input,1,1)
        ftablayout.addWidget(self.module,2,0)
        ftablayout.addWidget(self.moduleBox,2,1)
        ftablayout.addWidget(self.button,3,0)
        ftablayout.addWidget(self.fileButton, 3,1)
        ftablayout.addWidget(self.result,4,1)

        self.setLayout(ftablayout)
        
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Data Files (*.csv)", 
                                                  options=options)
        if fileName:
            self.data_file = fileName
        
    
    def select_module(self, i):
        self.module_idx = i
        
    
    def choosefile(self):
        self.openFileNameDialog()
    
    def predict(self):
        studentId = self.studentID_input.text()
        data = pd.read_csv('../../data/visual_set.csv')
        try:
            id_int = int(studentId)
            X = data[data['id_student']==id_int]
            course_modules = ['AAA','BBB','CCC','DDD','EEE','FFF','GGG']
            course = course_modules[self.module_idx]
            X = X[X['code_module']==course]
            text = f"""
            The probability that student {id_int}
            will pass course module {course} is 
            {X['pass_prob'].tolist()[0]}
            
            Following are his features:
                gender : {X['gender'].tolist()[0]} 
                highest_education : {X['highest_education'].tolist()[0]}
                imd_band : {X['imd_band'].tolist()[0]}
                age_band : {X['age_band'].tolist()[0]}
                num_of_prev_attempts : {X['num_of_prev_attempts'].tolist()[0]}
                studied_credits : {X['studied_credits'].tolist()[0]}
                disability : {X['disability'].tolist()[0]}
                Early Bird : {X['Early Bird'].tolist()[0]}
                Last Minute : {X['Last Minite'].tolist()[0]}
                Late Reg : {X['Late Reg'].tolist()[0]}
                Regular Reg : {X['Regular Reg'].tolist()[0]}
                sum_click : {X['sum_click'].tolist()[0]}
                Regular Reg : {X['Regular Reg'].tolist()[0]}
                sum_click : {X['sum_click'].tolist()[0]}
                learning_pattern_0 : {X['learning_pattern_0'].tolist()[0]}
                learning_pattern_1 : {X['learning_pattern_1'].tolist()[0]}
                learning_pattern_2 : {X['learning_pattern_2'].tolist()[0]}
                avg_ahead_ddl : {X['avg_ahead_ddl'].tolist()[0]}
                std_assess_score : {X['std_assess_score'].tolist()[0]}
            """
        
            self.result.setText(text)
            newfont = QtGui.QFont("Serif", 15, QtGui.QFont.Bold)
            self.result.setFont(newfont)
        except:
            text = 'Based on our predication\nThe probability that\nthis student will complete the course is 0'
            self.result.setText(text)
            newfont = QtGui.QFont("Serif", 20, QtGui.QFont.Bold)
            self.result.setFont(newfont)