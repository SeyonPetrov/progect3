import sys
from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow


class Sque(QMainWindow):
    def __init__(self):
        super(Sque, self).__init__()
        uic.loadUi('Кобъектив-2.ui', self)
        self.do_paint = False
        self.pushButton.clicked.connect(self.paint)

    def paint(self):
        self.k = float(self.lineEdit.text())
        self.n = int(self.lineEdit_2.text())
        self.do_paint = True
        self.repaint()

    def paintEvent(self, event):
        if self.do_paint:
            pai = QPainter(self)
            pai.begin(self)
            self.painter(pai)

            pai.end()

    def painter(self, pai):
        pai.setPen(QColor(0, 0, 0))

        pai.drawLine(120, 100, 400, 100)
        pai.drawLine(120, 380, 400, 380)
        pai.drawLine(120, 100, 120, 380)
        pai.drawLine(400, 100, 400, 380)

        q, w, e, r = (120, 100), (400, 100), (120, 380), (400, 380)
        for x in range(self.n):
            pai.drawLine(q[0] + ((w[0] - q[0]) - (w[0] - q[0]) * self.k), q[1], w[0], w[1] / self.k)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sq = Sque()
    sq.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())