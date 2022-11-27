import sys
import sqlite3
from random import randint as r
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog


def rand():
    return r(190, 255)


class Library(QMainWindow):
    def __init__(self):
        super(Library, self).__init__()
        self.n = 0
        self.author = ''
        self.pod = sqlite3.connect('проект_1/boks_db.sqlite')  # подключаем базу данных
        self.cu = self.pod.cursor()  # создаем указаатель
        self.main_menu()  # запускаем главное меню

    def main_menu(self):  # открываем главное меню и подключаем кнопки
        uic.loadUi('проект_1/lib.ui', self)
        self.pb.clicked.connect(self.big_ord)  # список всех книг
        self.pb2.clicked.connect(self.writers)  # список писателей
        self.pb3.clicked.connect(self.search)  # общий поиск

    def big_ord(self, text='', sorting=False):  # открываем список всех записанных книг
        uic.loadUi('проект_1/lib_books.ui', self)
        # подключаем кнопки
        self.push.clicked.connect(self.main_menu)  # возврат в главное меню
        self.push_2.clicked.connect(self.redact_book)  # редактирование
        self.push_4.clicked.connect(self.sorting)  # сортировка
        # получаем из базы даных все книги, которые есть
        data = self.cu.execute("""select books.name, authors.name, genres.title, publisher, words_amount from books
                              inner join authors on books.authorid = authors.id
                              inner join genres on books.genre = genres.id""").fetchall()
        if sorting:  # сортируем по алфавиту через функцию srоted с лямбдой
            data = sorted(data, key=lambda x: x[0])
        # записываем полученные данные в таблицу QTableWidget
        self.tableWidget.setRowCount(0)
        if not text:  # проверка флага поиска(если есть, то запущена поисковая строка)
            for i, row in enumerate(data):  # раскрываем список олученных книг
                n = QColor(rand(), 255, rand())  # подбираем уникальный для списка цвет
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)  # добавляем строчки в таблице для каждой новой книги из списка
                for j, elem in enumerate(row):  # раскрываем кортеж из данных о книге по элементам
                    t = QTableWidgetItem(str(elem))  # создаем элемент таблицы
                    t.setBackground(n)  # задаем ему ранее подобранный цыет
                    t.setFlags(Qt.ItemIsEnabled)  # запрещаем его реактирование во время работы программы
                    self.tableWidget.setItem(
                        i, j, t)  # вносим элемент на определенные строку и столбец
        else:  # поисковая строка запущена
            num = 0  # проверка добавленности хотябы одного элемента в таблицу
            for i, row in enumerate(data):  # делаем все те же операции,
                if text in f'{row[0]} {row[1]}':  # но с проверкой наличия текста из поисковой строки
                    n = QColor(rand(), rand(), rand())
                    self.tableWidget.setRowCount(
                        self.tableWidget.rowCount() + 1)
                    for j, elem in enumerate(row):
                        t = QTableWidgetItem(str(elem))
                        t.setBackground(n)
                        t.setFlags(Qt.ItemIsEnabled)
                        self.tableWidget.setItem(
                            num, j, t)
                    num += 1
            if not num:  # если в таблицу нечго не добавленно, а поиск бы активен
                self.eer.setText('Ничего нет. Или вы ошиблись в вводе')  # выводим ошибку

        self.push_3.clicked.connect(self.internal_search)  # запускаем поисковую строку через кнопку

    def sorting(self):  # сортировка
        if self.n % 2 == 0:  # при четных числах нажатия
            self.big_ord(sorting=True)  # сортирвка активна
        else:  # при нечетных - отключается
            self.big_ord(sorting=False)
        self.n += 1  # нумеровка нажатий

    def internal_search(self):  # активируем поиск
        text = self.eer.text().lower().capitalize()  # текст из поисковой строки в нужном виде
        self.big_ord(text)

    def redact_book(self):  # открываем окно редактирования и подключаем кнопки
        uic.loadUi('проект_1/redact.ui', self)
        self.bbp.clicked.connect(self.adding)  # переход к добавлению книг
        self.bbp_3.clicked.connect(self.big_ord)  # возвращаемся к общему списку книг
        self.bbp_2.clicked.connect(self.deleting)  # переход к удалению книг

    def deleting(self):  # окно удаления
        uic.loadUi('проект_1/delet.ui', self)
        self.rr_2.clicked.connect(self.big_ord)  # кнопка возврата к списку
        self.rr.clicked.connect(self.run_delete)  # кнопка начала процесса удаления

    def run_delete(self):
        name = self.pop.text()  # получаем название книги
        author = self.pop_2.text()  # и автора
        # берем необходимые данные из базы
        check1 = self.cu.execute("""select name from books where name = ?""", (name,)).fetchall()
        check = self.cu.execute("""select name from authors where name = ?""", (author,)).fetchall()
        check3 = self.cu.execute("""select name from authors where id in (select authorid from books
                     where name = ?)""", (name,)).fetchall()
        if check1:  # проверяем их наличие и звязь в базе
            if check:
                if check3:  # удаляем из базы
                    self.cu.execute("""delete from books where name = ? and authorid in (select id from authors
                           where name = ?)""", (name, author)).fetchall()
                    self.big_ord()
                else:  # в случае если книги нет или нет связи между книгой и автором
                    self.no_delet()  # возвращаем ошибку
            else:
                self.no_delet()
        else:
            self.no_delet()
        self.pod.commit()  # связываем продеанные операции с базой данных

    def no_delet(self):  # окно ошибки при удалении
        uic.loadUi('проект_1/never_delete.ui', self)
        self.tt.clicked.connect(self.deleting)

    def adding(self):  # окно добавления
        uic.loadUi('проект_1/add_book.ui', self)

        self.pp_2.clicked.connect(self.big_ord)  # кнопка возврата к списку
        self.pp.clicked.connect(self.run_add)  # кнопка начала процесса добавления

    def run_add(self):
        check_num = 0  # флаг проверки
        name = self.vv.text()  # получаем необходимы для добавления данные
        publ = self.vv_3.text()  # из полей ввода
        words = self.vv_5.text()
        bio = self.vv_6.text()
        # проверка наличия книги с таким же название, как у введенного
        if self.cu.execute("""select name from books where name = ?""", (name,)).fetchall():
            check_num += 1
        # проверка наличия и звязи с книгой введенного имени автора
        author = self.vv_2.text()
        if self.cu.execute("""select name from authors where name = ?""", (author,)).fetchall():
            author = self.cu.execute("""select id from authors where name = ?""", (author,)).fetchone()[0]
            check_num += 1
        else:  # добавление автора в базу, если его там нет
            self.cu.execute("""insert into authors(name, biography) values(?, ?)""", (author, bio)).fetchall()
            author = self.cu.execute("""select id from authors where name = ?""", (author,)).fetchone()[0]

        gen = self.vv_4.text()  # проверка наличия в базе введенного жанра
        if self.cu.execute("""select title from genres where title = ?""", (gen,)).fetchall():
            gen = self.cu.execute("""select id from genres where title = ?""", (gen,)).fetchone()[0]
        else:  # добавление в базу жаннра, если его там нет
            self.cu.execute("""insert into genres(title) values(?)""", (gen,)).fetchall()
            gen = self.cu.execute("""select id from genres where title = ?""", (gen,)).fetchone()[0]

        if check_num == 2:
            self.i_have()  # возвращение ошибки, если подобная книга уже есть
        else:  # добавление книги в базу, если ее там нет
            self.cu.execute("""insert into books(name, authorid, genre, publisher, words_amount)
                   values(?, ?, ?, ?, ?)""", (name, author, gen, publ, words)).fetchall()
        self.pod.commit()
        self.big_ord()  # возвращаемся к списку книг

    def i_have(self):  # генерация ошибки, если введенная книга имеется в базе
        uic.loadUi('проект_1/i_have.ui', self)
        self.ff.clicked.connect(self.adding)

    def writers(self):  # открываем окно списка писателей
        uic.loadUi('проект_1/writers.ui', self)
        self.bb.clicked.connect(self.main_menu)  # возврат в главное меню
        # получаем список писателей из базы
        data = self.cu.execute("""select name from authors""").fetchall()
        # заносим полученный список в ListWidget
        for i, x in enumerate(data):
            self.listWidget.addItem(x[0])
        # открываем биографию автора при двойном щелчке на его имя в списке
        self.listWidget.itemDoubleClicked.connect(self.bio)
        self.trr.textChanged.connect(self.wri_search)  # запускаем поиск автора в списке при введении текста

    def wri_search(self):  # процесс поиска автора в списке
        text = self.trr.text()  # берем текст из поля ввода
        data = self.cu.execute("""select name from authors""").fetchall()
        for i, x in enumerate(data):  # выделяем строку в списке, если в ней есть введеный текст
            if text in x[0]:
                self.listWidget.setCurrentRow(i)

    def bio(self):  # открываем окно биографии
        uic.loadUi('проект_1/bio.ui', self)
        self.jh.clicked.connect(self.writers)  # кнопка возврата к списку писателей

        data = self.cu.execute("""select name from authors""").fetchall()  # получаем список авторов

        n = self.listWidget.currentRow()  # берем номер выделенной щелчком строки
        for i, x in enumerate(data):  # сравниваем со списком авторов из базы
            if i == n:  # при совпадении
                self.kkk.setText(x[0])  # выводим нужное значение в заголовок
                self.author = x[0]  # имя нужного автора
        # берем из базы его биографию
        bio = self.cu.execute("""select biography from authors where name = ?""", (self.author,)).fetchone()[0]
        self.pte.setPlainText(bio)  # выводим найденую биографию на экран
        # кнопка перехода к списку книг от выбранного писателя
        self.pte_2.clicked.connect(self.au_books)
        # собираем данные для установки фото
        for_pix = self.cu.execute("""select photo from authors where name = ?""", (self.author,)).fetchone()[0]

        if for_pix:
            pix = QPixmap(for_pix)
        else:  # если фотографии автора нет, ставим заготовленный фон
            pix = QPixmap('проект_1/att.png')
        self.kkk_2.setPixmap(pix)  # выводим фото на экран через pixmap

        self.pte_3.clicked.connect(self.add_photo)  # активируем загрузку нового фото в программу

    def add_photo(self):  # добавление фотографии
        photo = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]  # находим адрес фотографии через диалоговое окно

        if photo:  # если нашли, то добавляем его в базу и связываемся с ней, чтоб ничего потом не пропало
            self.cu.execute("""update authors set photo = ? where name = ?""", (photo, self.author)).fetchall()
            self.pod.commit()

    def au_books(self):  # открываем окно со списком книг вбранного писателя
        uic.loadUi('проект_1/au_bok.ui', self)
        # находим в базе все книги и информацию о них от выбранного автора
        book_ord = self.cu.execute("""select books.name, genres.title, books.publisher, books.words_amount from books
                          inner join genres on books.genre = genres.id
                          where books.authorid in (select id from authors 
                          where name = ?)""", (self.author,)).fetchall()
        # выводим полученную информацию на экран черех TableWidget
        self.tableWidget.setRowCount(0)  # все так же, как и в общем списке книг
        for i, row in enumerate(book_ord):
            n = QColor(rand(), rand(), rand())
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                t = QTableWidgetItem(str(elem))
                t.setFlags(Qt.ItemIsEnabled)
                t.setBackground(n)
                self.tableWidget.setItem(
                    i, j, t)

        self.yy.clicked.connect(self.writers)  # кнопка возврата к списку авторов
        self.yy_2.clicked.connect(self.big_ord)  # кнопка перехода к списку всех книг

    def search(self):  # открываем окно поиска
        uic.loadUi('проект_1/search.ui', self)
        self.pushButton_2.clicked.connect(self.main_menu)  # кнопка возврата в главное меню
        self.gh.clicked.connect(self.run_search)  # кнопка начала процесса поиска
        self.hh.setText('Всего книг: ' + str(len(self.cu.execute("select name from books").fetchall())))  # сколько книг

    def run_search(self):  # процесс поиска
        d = self.cu.execute("""select books.name, authors.name, genres.title, publisher, words_amount from books
                              inner join authors on books.authorid = authors.id
                              inner join genres on books.genre = genres.id""").fetchall()  # data
        self.ad.setText('')
        krit = self.comboBox.currentText()  # вид критерия поиска
        kol = self.spinBox.value()  # количество книг, что нужно найти
        pol = self.lineEdit.text().lower().capitalize()  # значение критерия поиска

        if krit == 'По жанру' and pol:  # получаем данные из базы о книгах с введеным жанром
            d = self.cu.execute("""select books.name, authors.name, genres.title, publisher, words_amount from books
                        inner join authors on books.authorid = authors.id
                        inner join genres on books.genre = genres.id where title = ?""", (pol,)).fetchall()

        if krit == 'По названию' and pol:  # получаем данные из базы о книгах с введенным названием
            d = self.cu.execute("""select books.name, authors.name, genres.title, publisher, words_amount from books
                        inner join authors on books.authorid = authors.id
                        inner join genres on books.genre = genres.id where books.name = ?""", (pol,)).fetchall()
        if krit == 'По автору' and pol:  # получаем данные из базы о книгах с введенным автором
            d = self.cu.execute("""select books.name, authors.name, genres.title, publisher, words_amount from books
                        inner join authors on books.authorid = authors.id
                        inner join genres on books.genre = genres.id where authors.name = ?""", (pol,)).fetchall()
        if 0 < kol < len(d):  # выбираем первые несколько книг, если запрошенное количество книг меньше найденных
            d = d[:kol]

        if kol == len(d):  # ничего не меняем если запрошенное кол-во книг рано найденному
            pass

        try:  # пробуем сортировать (если кнопка не нажата, ничего не произойдет)
            sorting = self.bg.checkedButton().text()  # определяем, какую кнопку нажали
            if sorting == 'по алфавиту':  # сортируем по названию от а до я
                d = sorted(d, key=lambda x: x[0])
            if sorting == 'против алфавита':  # сортируем по названию от я до а
                d = sorted(d, key=lambda x: x[0], reverse=True)
            if '(а-я)' in sorting:  # сортируем по названию от а до я
                d = sorted(d, key=lambda x: x[1])
            if '(я-а)' in sorting:  # сортируем по названию от я до а
                d = sorted(d, key=lambda x: x[1], reverse=True)
        except AttributeError:
            pass
        if d:  # выводим найденные книги на экран через TableWidget, если таковые имеются
            self.tableWidget.setRowCount(0)  # тот же принцип, ка и в общем списке книг
            for i, row in enumerate(d):
                n = QColor(rand(), rand(), rand())
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    t = QTableWidgetItem(str(elem))
                    t.setFlags(Qt.ItemIsEnabled)
                    t.setBackground(n)
                    self.tableWidget.setItem(
                        i, j, t)
        else:  # если ничего не нашли выводим текст ошибки
            self.ad.setText('Ничего нет(>_<)')

    def closeEvent(self, event):  # при закрытии программы
        self.pod.commit()  # сначала связываемся с базой (на всякий)
        self.pod.close()  # после разрываем с ней связь


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    li = Library()
    li.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
