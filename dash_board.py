from PyQt5.QtWidgets import QMainWindow, QTabWidget
from PyQt5.QtGui import QIcon
from admin_panel import AdminPanel
from student_panel import StudentPanel

class DashBoard(QMainWindow):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setWindowTitle(f"Student Management System - {role.capitalize()} Panel")
        self.setMinimumSize(1000, 700)
        self.setWindowIcon(QIcon("icon.jpg"))  # Add your icon file
        self.setup_ui()
        
    def setup_ui(self):
        # Create tabs
        self.tabs = QTabWidget()
        
        # Always add student panel
        self.student_panel = StudentPanel(self.role)
        self.tabs.addTab(self.student_panel, "Student Management")
        
        # Add admin panel if user is admin
        if self.role == 'admin':
            self.admin_panel = AdminPanel()
            self.tabs.addTab(self.admin_panel, "User Management")
        
        self.setCentralWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage(f"Logged in as {self.role}")
        
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
            }
            QTabBar::tab {
                padding: 8px 12px;
                background: #e0e0e0;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #fff;
                margin-bottom: -1px;
            }
        """)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    window = DashBoard("admin")  # For testing
    window.show()
    app.exec_()