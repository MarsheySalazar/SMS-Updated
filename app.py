import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show login window
    login = LoginWindow()
    login.setStyleSheet("QWidget { background-color: #ffff}")
    login.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()