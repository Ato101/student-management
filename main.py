from PyQt6.QtWidgets import QApplication,QLabel,QWidget,QGridLayout,QLineEdit,QPushButton,\
    QDialog,QMainWindow,QTableWidget,QTableWidgetItem,QVBoxLayout,QComboBox,QToolBar,QStatusBar
from PyQt6.QtGui import QAction,QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        self.setMinimumSize(800,600)
        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&help')
        search_menu_item = self.menuBar().addMenu('Edit')

        add_student_action = QAction(QIcon('icons/add.png'),'Add student',self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About',self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction(QIcon('icons/search.png'),'Search',self)
        search_action.triggered.connect(self.search)
        search_menu_item.addAction(search_action)

        # create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        # adding toolbar
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        #Detect cell

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit = QPushButton(QIcon('icons/edit.png'),'edit')
        edit.clicked.connect(self.edit)

        delete = QPushButton(QIcon('icons/delete.png'),'delete')
        delete.clicked.connect(self.delete)



        children =self.status_bar.findChildren(QPushButton)

        if children:
            for child in children:
                self.status_bar.removeWidget(child)
        self.status_bar.addWidget(edit)
        self.status_bar.addWidget(delete)







    # Loading data from the data_base
    def load_data(self):

        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')
        self.table.setRowCount(0)
        # populating our GUI as a widget
        for row_number,row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))

        connection.close()

    # inserting data into our data_base
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()
    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()
class EditDialog(QDialog):
    def __int__(self):
        super().__init__()
        self.setWindowTitle('Edit student records')
        self.setFixedHeight(300)
        self.setFixedWidth(300)
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete')
        self.setFixedWidth(200)
        self.setFixedHeight(200)

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        # creating window for the Dialog box
        self.setWindowTitle('insert Student records')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        #Add combo box of courses


        self.course_name = QComboBox()
        courses =['Biology','Math','Astronomy','Physis']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.student_contact = QLineEdit()
        self.student_contact.setPlaceholderText('Number')
        layout.addWidget(self.student_contact)

        button = QPushButton('Submit')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.student_contact.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name,course,mobile) VALUES(?,?,?)",
                       (name,course,mobile))

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('search records')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.search_text = QLineEdit()
        self.search_text.setPlaceholderText('Search')
        layout.addWidget(self.search_text)


        buttom = QPushButton('Search Record')
        buttom.clicked.connect(self.search_record)
        layout.addWidget(buttom)

        self.setLayout(layout)

    def search_record(self):
        search = self.search_text.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        result=cursor.execute("SELECT * FROM students where name = ?",(search,))
        row = list(result)
        items = main_window.table.findItems(search, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(),1).setSelected(True)
        cursor.close()
        connection.close()


#calling our various function and classes

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())