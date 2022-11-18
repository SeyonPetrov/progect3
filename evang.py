import sqlite3
import sys


pod = sqlite3.connect('проект_1/boks_db.sqlite')
cu = pod.cursor()

data = cu.execute("""select books.name, authors.name, genres.title, publisher, words_amount from books
                      inner join authors on books.authorid = authors.id
                      inner join genres on books.genre = genres.id""").fetchall()

print(data)
print(sorted(data, key=lambda x: x[0]))
pod.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
