from PyQt6.QtWidgets import QApplication,QLabel,QWidget,QGridLayout,QLineEdit,QPushButton,\
    QDialog,QMainWindow,QTableWidget,QTableWidgetItem,QVBoxLayout,QComboBox,QToolBar,QStatusBar,QMessageBox
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
        about_action.triggered.connect(self.about)

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
        edit = QPushButton(QIcon('icons/edit.png'),'Edit')
        edit.clicked.connect(self.edit)

        delete = QPushButton(QIcon('icons/delete.png'),'Delete')
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

    def about(self):
        dialog = About()
        dialog.exec()




class About(QMessageBox):
    def __init__(self):
        super().__init__()

        # creating window for the Dialog box
        self.setWindowTitle('About')
        content ="""
        This a student management app used for  managing student record
        """

        self.setText(content)

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
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


        confirmation = QMessageBox()
        confirmation.setWindowTitle('Insert Sucess')
        confirmation.setText('Sucessfully')
        confirmation.exec()


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
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update')
        self.setFixedWidth(300)
        self.setFixedHeight(400)

        layout = QVBoxLayout()
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()

        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)


        course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physis']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        student_contact = main_window.table.item(index, 3).text()
        self.student_contact = QLineEdit(student_contact)
        layout.addWidget(self.student_contact)
        index = main_window.table.currentRow()
        button = QPushButton('Update')
        button.clicked.connect(self.update_student)
        layout.addWidget(button)
        self.setLayout(layout)

    def update_student(self):
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0)
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE  students SET name=?,course =?,mobile=? WHERE id =?",
                       (self.student_name.text(), self.course_name.itemText(self.course_name.currentIndex()),
                        self.student_contact.text(),student_id,))
        connection.commit()
        cursor.close()
        main_window.load_data()
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete')


        layout = QGridLayout()
        confirmation = QLabel('Are you sure you want to delete')
        yes = QPushButton('Yes')
        no = QPushButton('No')

        layout.addWidget(confirmation,0,0,1,2)
        layout.addWidget(yes,1,0)
        layout.addWidget(no,1,1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)
       # no.clicked.connect(main_window.load_data())

    def delete_student(self):
        # Get student and student id from selected row
        index=  main_window.table.currentRow()
        student_id = main_window.table.item(index,0).text()

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('DELETE from students WHERE id=?',(student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()

        comfirmation = QMessageBox()
        comfirmation.setWindowTitle('Success')
        comfirmation.setText('The record was deleted sucessfully')
        comfirmation.exec()







#calling our various function and classes

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())