import random
from datetime import datetime
from string import ascii_letters, digits


class Verify:
    letters = ascii_letters + digits

    @classmethod
    def rand_id(cls):
        id_r = ""
        for i in range(2, 12):
            id_r += random.choice(cls.letters)
            if i % 4 == 0:
                id_r += "-"
        return id_r

    @classmethod
    def verify_str(cls, inst):
        if not isinstance(inst, str):
            raise TypeError("Type должно быть строкой")
        return inst

    @classmethod
    def verify_int(cls, inst):
        if not isinstance(inst, int):
            raise TypeError("Type должно быть целое число от 0 до 10 Включительно")
        return inst

    @classmethod
    def verify_isdigit(cls, inst):
        if not str(inst).isdigit():
            raise Exception("Может быть только цифрой в виде строки или целым числом")
        return inst


class Students:

    doc = "здесь нужно указать имя и фамилию студента, порядочность студента от 0 до 10 или по умолчанию будет 10," \
          " и укажите дату когда студент взял книгу ,пример(0000, 0, 0), " \
          "take_book вызывается чтобы забрать книгу, 1 аргумент = переменная книги, " \
          "2 аргумент = дата когда забирает студент книгу"\
          "back_book вызывается когда студент хочет вернуть книгу, 1 аргумент = переменная книги"

    def __init__(self, name: str, surname: str, stud_stat=10, b_time=None):
        self._name = Verify.verify_str(name)
        self._surname = Verify.verify_str(surname)
        self._stud_id = Verify.rand_id()
        self.book_c = []
        self._stud_stat = Verify.verify_int(stud_stat)
        self._b_time = b_time

    def take_book(self, book_copy, date):

        title_name = [j.book_title for j in [i for i in self.book_c]]
        if not isinstance(date, tuple):
            raise TypeError("Должно быть tuple с датой - пример (0000, 0, 0)")
        if book_copy.status != "Доступен":
            raise Exception("Эту книгу уже взял другой студент!")
        if book_copy.book_title in title_name:
            raise TypeError("такая книга уже есть у студента")
        if self.stud_stat == 0:
            raise Exception("Нельзя забрать книгу, порядочность = 0")
        self._b_time = datetime(*date)
        self.book_c.append(book_copy)
        if book_copy in self.book_c:
            book_copy.status = f"Взял студент с id = {self.stud_id}, дата взятия книги = {self._b_time.date()}"

    def back_book(self, book_copy):
        if book_copy in self.book_c:
            book_copy.status = "Доступен"
            self.book_c.remove(book_copy)
            if (datetime.today() - self._b_time).days > 14:
                late = (datetime.today() - self._b_time).days
                self._stud_stat = 0
                return f"Студент опоздал с книгой на {late} дней, порядочность студента = 0"

    def __str__(self):
        return f"{self.name} {self.surname}, id = {self.stud_id}, Статус порядочности = {self.stud_stat}, " \
               f"взятые книги - {[[i.full_status] for i in self.book_c]}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        Verify.verify_str(name)
        self._name = name

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, surname):
        Verify.verify_str(surname)
        self._surname = surname

    @property
    def stud_id(self):
        return self._stud_id

    @property
    def stud_stat(self):
        return self._stud_stat

    @stud_stat.setter
    def stud_stat(self, stat):
        Verify.verify_int(stat)
        self._stud_stat = stat


class BookCopy:

    doc = "Здесь указывается экземпляр книги и добавляются вручную с помощью append в self.Book.list_book(self)," \
          "если студент не вернет книгу в срок, порядочность студента будет = 0 и нельзя будет брать больше книг"

    def __init__(self, book, state: int, status="Доступен"):
        self.book = book
        self.book_title = Verify.verify_str(book.title)
        self.copy_id = Verify.rand_id()
        self.state = Verify.verify_int(state)
        self.status = status

    @property
    def full_status(self):
        return f"{self.book_title}, id копии = {self.copy_id}, состояние = {self.state}, статус = {self.status}"

    def __repr__(self):
        return f"{self.book_title},{self.copy_id},{self.state},{self.status}"


class Book:

    doc = "Здесь нужно указать саму книгу (название, авторов, год выпуска, ISBN, Жанр)"

    def __init__(self, title: str, authors: str, year: int, isbn: str, genre: str):
        self._title = Verify.verify_str(title)
        self._authors = Verify.verify_str(authors)
        self._year = Verify.verify_isdigit(year)
        self._ISBN = Verify.verify_str(isbn)
        self.genre = Verify.verify_str(genre)
        self.list_book = []

    @property
    def title(self):
        return self._title

    @property
    def authors(self):
        return self._authors

    @property
    def year(self):
        return self._year

    @property
    def isbn(self):
        return self._ISBN

    def __str__(self):
        return f"{self.title}, {self.authors}, {self.year}, {self.isbn}, {self.genre}," \
               f" Копии этой книги - {[[i.full_status] for i in self.list_book]}"


# Создаем образ книги
book1 = Book("Python. К вершинам мастерства", "Лучано Рамальо", 2015, "978-5-97060-384-0", "Обучение")
book2 = Book("Python. Чистый код для продолжающих", "Эл Свейгарт", 2021, "978-5-4461-1852-6", "Обучение")

# Создаем 2 переменных студентов
stud1 = Students("Vram", "Torosyan")
stud2 = Students("Gegham", "Petrosyan")

# Создал 2 копии каждой книги
book1.list_book.append(book1_ekz1 := BookCopy(book1, 6))
book1.list_book.append(book1_ekz2 := BookCopy(book1, 4))
book2.list_book.append(book2_ekz1 := BookCopy(book2, 9))
book2.list_book.append(book2_ekz2 := BookCopy(book2, 7))

# студент взял книгу
stud1.take_book(book1_ekz1, (2022, 4, 10))
stud2.take_book(book1_ekz2, (2023, 4, 20))

print(stud1)
print(stud2)
print()
print(book1)
print(book2)
