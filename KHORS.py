from PyQt5.QtCore import Qt, QPoint
import sys
from PyQt5.QtGui import QPainter, QColor, QPolygon
from random import randint
from PyQt5.QtWidgets import QApplication, QWidget


def rand_num():
    return randint(10, 300)


def rand_col():
    return tuple([randint(0, 255) for _ in range(3)])


class SuperMat(QWidget):
    def __init__(self):
        super(SuperMat, self).__init__()
        self.setFixedSize(800, 600)
        self.setWindowTitle('Суперматизм')
        self.x = 0
        self.y = 0
        self.do_paint = False
        self.form = 0
        self.setMouseTracking(True)

    def paintEvent(self, event):
        if self.do_paint:
            pai = QPainter(self)
            pai.begin(self)
            self.paint(pai)
            pai.end()

    def paint(self, pai):

        n = rand_col()
        m = rand_num()
        pai.setBrush(QColor(200, n[1], n[2]))
        pai.setPen(QColor(200, n[1], n[2]))
        if self.form == 'к':
            pai.drawEllipse(int(self.x) - (m // 2), int(self.y) - (m // 2), m, m)
        if self.form == 'кв':
            pai.drawRect(int(self.x) - (m // 2), int(self.y) - (m // 2), m, m)
        if self.form == 'три':
            points = [QPoint(int(self.x), int(self.y) - (m // 2)),
                      QPoint(int(self.x) + (m // 2), int(self.y) + (m // 2)),
                      QPoint(int(self.x) - (m // 2), int(self.y) + (m // 2))]
            pol = QPolygon(points)
            pai.drawPolygon(pol)
        self.do_paint = False

    def painter(self):
        self.do_paint = True
        self.repaint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.form = 'три'
            self.painter()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.form = 'к'
            self.painter()
        if event.button() == Qt.RightButton:
            self.form = 'кв'
            self.painter()

    def mouseMoveEvent(self, event):
        self.x = event.x()
        self.y = event.y()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sm = SuperMat()
    sm.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())