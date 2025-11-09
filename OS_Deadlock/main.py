import sys
from PyQt5.QtWidgets import QApplication
from gui import DeadlockGUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = DeadlockGUI()
    gui.show()
    sys.exit(app.exec_())
