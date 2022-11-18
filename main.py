import sys
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog


class Imagine(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Управление прозрачностью')
        self.main_l = QVBoxLayout(self)
        self.sec_lay = QHBoxLayout(self)

        self.sli = QSlider()
        self.sli.setOrientation(Qt.Vertical)
        self.sli.setTickPosition(QSlider.TicksAbove)
        self.for_im = QLabel(self)
        self.imname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '',
                                                  'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        self.pix = QPixmap(self.imname)
        self.for_im.setPixmap(self.pix)

        self.sec_lay.addWidget(self.sli)
        self.sec_lay.addWidget(self.for_im)
        self.main_l.addLayout(self.sec_lay)

        self.sli.valueChanged.connect(self.limpid)

    def limpid(self):
        val = self.sli.value()
        print(val)
        im = Image.open(self.imname)
        im.putalpha(int(255 * (val / 100)))

        im.save('lol.png')
        self.pix = QPixmap('lol.png')
        self.for_im.setPixmap(self.pix)
        im.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Imagine()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

