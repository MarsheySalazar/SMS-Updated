from PyQt5.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, 
                           QLineEdit, QDateEdit, QComboBox, QHeaderView,
                           QLabel)
from PyQt5.QtCore import Qt, QDate
from backend import (add_student, get_students, search_students, 
                    update_student, delete_student)

class StudentPanel(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setup_ui()
        self.load_students()
        self.setWindowTitle("Student Management System")
        self.resize(1000, 700)
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        # Title
        title = QLabel("Student Management")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        
        # Form for adding/editing students
        self.form = QWidget()
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(10)
        
        # Form fields - updated to match new structure
        self.std_id = QLineEdit()
        self.fullname = QLineEdit()
        self.course = QComboBox()
        self.course = QLineEdit()
        self.section = QLineEdit()
        self.dob = QDateEdit(calendarPopup=True)
        self.dob.setDate(QDate.currentDate())
        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female", "Other"])
        self.mobile = QLineEdit()
        
        # Add fields to form
        form_layout.addRow("Student ID:", self.std_id)
        form_layout.addRow("Full Name:", self.fullname)
        form_layout.addRow("Course:", self.course)
        form_layout.addRow("Section:", self.section)
        form_layout.addRow("Date of Birth:", self.dob)
        form_layout.addRow("Gender:", self.gender)
        form_layout.addRow("Mobile:", self.mobile)
        
        # Form buttons
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add Student")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.add_btn.clicked.connect(self.add_student)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_form)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        
        form_layout.addRow(btn_layout)
        self.form.setLayout(form_layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        
        self.search_field = QComboBox()
        self.search_field.addItems(["Student ID", "Full Name", "Course", "Section", "Mobile"])
        self.search_field.setFixedWidth(120)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        
        self.search_btn = QPushButton("Search")
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.search_btn.clicked.connect(self.search_students)
        
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        
        # Student table - updated columns
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(9)
        self.student_table.setHorizontalHeaderLabels(
            ["ID", "Student ID", "Full Name", "Course", "Section", "DOB", "Gender", "Mobile", "Actions"]
        )
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.student_table.verticalHeader().setVisible(False)
        self.student_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Set selection behavior
        self.student_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.student_table.setSelectionMode(QTableWidget.SingleSelection)
        self.student_table.cellClicked.connect(self.populate_form_from_table)
        
        # Add widgets to main layout
        main_layout.addWidget(title)
        main_layout.addWidget(self.form)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.student_table)
        
        self.setLayout(main_layout)
        
        # Disable form if user is not admin
        if self.role != 'admin':
            self.disable_form()
    
    def disable_form(self):
        """Disable form fields for regular users"""
        self.std_id.setReadOnly(True)
        self.fullname.setReadOnly(True)
        self.course.setEnabled(False)
        self.section.setReadOnly(True)
        self.dob.setReadOnly(True)
        self.gender.setEnabled(False)
        self.mobile.setReadOnly(True)
        self.add_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
    
    def load_students(self):
        students = get_students()
        self.student_table.setRowCount(len(students))
        
        for row, student in enumerate(students):
            for col, value in enumerate(student):
                self.student_table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Add action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            if self.role == 'admin':
                edit_btn = QPushButton("Edit")
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        padding: 5px;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
                edit_btn.clicked.connect(lambda _, sid=student[0]: self.update_student(sid))
                btn_layout.addWidget(edit_btn)
                
                delete_btn = QPushButton("Delete")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        padding: 5px;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                """)
                delete_btn.clicked.connect(lambda _, sid=student[0]: self.delete_student(sid))
                btn_layout.addWidget(delete_btn)
            
            btn_widget.setLayout(btn_layout)
            self.student_table.setCellWidget(row, 8, btn_widget)
    
    def populate_form_from_table(self, row, col):
        """Populate form with data from selected row"""
        if self.role != 'admin':
            return
        
        student_id = self.student_table.item(row, 0).text()
        std_id = self.student_table.item(row, 1).text()
        fullname = self.student_table.item(row, 2).text()
        course = self.student_table.item(row, 3).text()
        section = self.student_table.item(row, 4).text()
        dob = self.student_table.item(row, 5).text()
        gender = self.student_table.item(row, 6).text()
        mobile = self.student_table.item(row, 7).text()
        
        # Update form fields
        self.std_id.setText(std_id)
        self.fullname.setText(fullname)
        self.course.setText(course)
        self.section.setText(section)
        self.dob.setDate(QDate.fromString(dob, "yyyy-MM-dd"))
        self.gender.setCurrentText(gender)
        self.mobile.setText(mobile)
        
        # Change button text
        self.add_btn.setText("Update")
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(lambda: self.update_student(student_id))
    
    def clear_form(self):
        """Clear all form fields"""
        self.std_id.clear()
        self.fullname.clear()
        self.course.clear()
        self.section.clear()
        self.dob.setDate(QDate.currentDate())
        self.gender.setCurrentIndex(0)
        self.mobile.clear()
        
        # Reset button
        self.add_btn.setText("Add Student")
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.add_student)
    
    def add_student(self):
        """Add a new student"""
        data = {
            'std_id': self.std_id.text().strip(),
            'fullname': self.fullname.text().strip(),
            'course': self.course.text().strip(),
            'section': self.section.text().strip(),
            'dob': self.dob.date().toString("yyyy-MM-dd"),
            'gender': self.gender.currentText(),
            'mobile': self.mobile.text().strip()
        }
        
        # Validate required fields
        if not all([data['std_id'], data['fullname'], data['course']]):
            QMessageBox.warning(self, "Error", "Student ID, Full Name, and Course are required")
            return
        
        if add_student(**data):
            QMessageBox.information(self, "Success", "Student added successfully")
            #self.clear_form()
            self.load_students()
        else:
            QMessageBox.warning(self, "Error", "Student ID already exists")
        
    def update_student(self, student_id):
        """Update existing student"""
        data = {
            'std_id': self.std_id.text().strip(),
            'fullname': self.fullname.text().strip(),
            'course': self.course.text().strip(),
            'section': self.section.text().strip(),
            'dob': self.dob.date().toString("yyyy-MM-dd"),
            'gender': self.gender.currentText(),
            'mobile': self.mobile.text().strip()
        }
        
        if update_student(int(student_id), **data):
            QMessageBox.information(self, "Success", "Student updated successfully")
            self.clear_form()
            self.load_students()
        else:
            QMessageBox.warning(self, "Error", "Failed to update student")
    
    def delete_student(self, student_id):
        """Delete a student"""
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            "Are you sure you want to delete this student?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if delete_student(student_id):
                QMessageBox.information(self, "Success", "Student deleted successfully")
                self.load_students()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete student")
    
    def search_students(self):
        """Search students based on criteria"""
        search_by = self.search_field.currentText().lower().replace(" ", "")
        search_term = self.search_input.text().strip()
        
        if not search_term:
            self.load_students()
            return
        
        # Map UI field names to database column names
        field_map = {
            "studentid": "std_id",
            "fullname": "fullname",
            "course": "course",
            "section": "section",
            "mobile": "mobile"
        }
        
        db_field = field_map.get(search_by, "std_id")
        results = search_students(**{db_field: search_term})
        self.student_table.setRowCount(len(results))
        
        for row, student in enumerate(results):
            for col, value in enumerate(student):
                self.student_table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Add action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            if self.role == 'admin':
                edit_btn = QPushButton("Edit")
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        padding: 5px;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
                edit_btn.clicked.connect(lambda _, sid=student[0]: self.update_student(sid))
                btn_layout.addWidget(edit_btn)
                
                delete_btn = QPushButton("Delete")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        padding: 5px;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                """)
                delete_btn.clicked.connect(lambda _, sid=student[0]: self.delete_student(sid))
                btn_layout.addWidget(delete_btn)
            
            btn_widget.setLayout(btn_layout)
            self.student_table.setCellWidget(row, 8, btn_widget)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    window = StudentPanel("admin")
    window.show()
    app.exec_()