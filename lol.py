import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Search2(QMainWindow):
    def __init__(self):
        super(Search2, self).__init__()
        uic.loadUi('поиск.ui', self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        year = self.lineEdit.text()
        name = self.lineEdit_2.text()
        long = self.lineEdit_3.text()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ser = Search2()
    ser.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())