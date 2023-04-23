import random
from datetime import datetime
from string import ascii_letters, digits


class Verify:  # Проверяет тип данных и генерирует id
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


class Students:  # класс студент - может брать книгу, вернуть книгу

    doc = "здесь нужно указать имя и фамилию студента, порядочность студента от 0 до 10 или по умолчанию будет 10," \
          " и укажите дату когда студент взял книгу ,пример(0000, 0, 0), " \
          "take_book вызывается чтобы забрать книгу, 1 аргумент = переменная книги, " \
          "2 аргумент = дата когда забирает студент книгу"\
          "back_book вызывается когда студент хочет вернуть книгу, 1 аргумент = переменная книги"

    def __init__(self, name: str, surname: str, email: str, stud_stat=10, limit=5, b_time=None):
        self._name = Verify.verify_str(name)
        self._surname = Verify.verify_str(surname)
        self._email = Verify.verify_str(email)
        self._stud_id = Verify.rand_id()
        self.book_c = []
        self._stud_stat = Verify.verify_int(stud_stat)
        self._limit = Verify.verify_int(limit)
        self._count_limit = 0
        self._b_time = b_time

    def take_book(self, book_copy, date):
        if len(self.book_c) == self._limit:
            raise Exception("Вы перевесили лимит")
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
        self._count_limit += 1
        if book_copy in self.book_c:
            book_copy.status = f"Взял студент с id = {self.stud_id}, дата взятия книги = {self._b_time.date()}"

    def back_book(self, book_copy):
        if book_copy in self.book_c:
            book_copy.status = "Доступен"
            self.book_c.remove(book_copy)
            self._count_limit -= 1
            if (datetime.today() - self._b_time).days > 14:
                late = (datetime.today() - self._b_time).days
                self._stud_stat = 0
                return f"Студент опоздал с книгой на {late} дней, порядочность студента = 0"

    @property
    def full_status(self):
        return f"{self.name} {self.surname}, id = {self.stud_id}, {self._email}, лимит книг = {self._count_limit}/{self._limit} Статус порядочности = {self.stud_stat},"

    def __str__(self):
        return f"{self.name} {self.surname}, id = {self.stud_id}, {self.stud_stat}, {self._email}, лимит книг = {self._count_limit}/{self._limit} Статус порядочности = {self.stud_stat}, "

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
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        Verify.verify_str(email)
        self._email = email

    @property
    def limit(self):
        return self._email

    @limit.setter
    def limit(self, limit):
        Verify.verify_int(limit)
        self._limit = limit

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


class BookCopy:  # класс копии книг - создает копию нужной книги
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


class Book:  # класс Книги - создает книгу и хранит в себя копии этой книги

    doc = "Здесь нужно указать саму книгу (название, авторов, год выпуска, ISBN, Жанр)"

    def __init__(self, title: str, authors: str, year: int, isbn: str, genre: str):
        self._id_book = Verify.rand_id()
        self._title = Verify.verify_str(title)
        self._authors = Verify.verify_str(authors)
        self._year = Verify.verify_isdigit(year)
        self._ISBN = Verify.verify_str(isbn)
        self.genre = Verify.verify_str(genre)
        self.list_book = []

    @property
    def full_status(self):
        return f"{self.title},{self.authors},{self.year},{self.isbn},{self.genre}"

    @property
    def id_book(self):
        return self._id_book

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


class Library:  # класс библиотека - хранит в себя книги, копию книг, студентов - можно сделать поиск в нужных списках
    name_lib = "coollib"
    student_list = []
    books_list = []
    book_cop = []

    @staticmethod
    def change_stud_limit(stud, limit):  # меняет лимит книг конкретного студента
        stud.limit = limit

    @classmethod
    def enter_studs(cls, *args):  # добавляет студентов в библиотеку
        cls.student_list += list([[i] for i in args])

    @classmethod
    def enter_book(cls, *args):  # добавляет книг в библиотеку
        cls.books_list += list([[i] for i in args])

    @classmethod
    def enter_book_copy(cls, *args):  # добавляет копию книг в библиотеку
        cls.book_cop += list([[i] for i in args])

    @classmethod
    def search_book(cls, word):  # делает поиск нужного слово в списке книге и возвращает найденные
        for_search = []
        for i in cls.books_list:
            for j in i:
                if word in j:
                    for_search += i
        print(for_search)

    @classmethod
    def search_copy_book(cls, word):  # делает поиск нужного слово в списке копии книг и возвращает найденные
        for_search = []
        for i in cls.book_cop:
            for j in i:
                if word in j:
                    for_search += i
        print(for_search)

    @classmethod
    def search_student(cls, word):  # делает поиск нужного слово в списке студентов и возвращает найденные
        for_search = []
        for i in cls.student_list:
            for j in i:
                if word in j:
                    for_search += i
        print(for_search)

    @classmethod
    def find_all_free_books_copy(cls):  # показывает все доступные копии книг
        for_search = []
        for i in cls.book_cop:
            for j in i:
                if "Доступен" in j:
                    for_search += i
        print(for_search)


#  создаем книг
book1 = Book("Python К вершинам мастерства", "Лучано Рамальо", 2015, "978-5-97060-384-0", "Обучение")
book2 = Book("Python Чистый код для продолжающих", "Эл Свейгарт", 2021, "978-5-4461-1852-6", "Обучение")

#  создаем студентов
stud1 = Students("Vram", "Torosyan", "vram_torosyan@mail.ru")
stud2 = Students("Gegham", "Petrosyan","Gegham_petrosyan@gmail.com")

#  тут поменял у студента 1 лимит на 4
Library.change_stud_limit(stud1, 4)

#  тут создаем копию книг и добавляем и сразу добавляем их в список книги по копии
#  мог сделать так, чтобы сразу добавился в список Библиотеки, но не стал
book1.list_book.append(book1_ekz1 := BookCopy(book1, 6))
book1.list_book.append(book1_ekz2 := BookCopy(book1, 4))
book2.list_book.append(book2_ekz1 := BookCopy(book2, 9))
book2.list_book.append(book2_ekz2 := BookCopy(book2, 7))

#  показывает что студент взял книгу и дату и id студента
stud1.take_book(book1_ekz1, (2023, 4, 25))

#  stud1.back_book(book1_ekz1) так можно вернуть книгу
#  если вернуть книгу позже чем 14 дней то порядочность студента станет = 0 и студент не сможет больше взять книг
print(stud1)
print(book1)
print()

#  добавляем в список Библиотеки
Library.enter_book(book1.full_status, book2.full_status)
Library.enter_studs(stud1.full_status, stud2.full_status)
Library.enter_book_copy(book1_ekz1.full_status, book1_ekz2.full_status, book2_ekz1.full_status, book2_ekz2.full_status)

# показывает все доступные книги
Library.find_all_free_books_copy()

# ищем студента по имени и приносит все данные про него
Library.search_student("Gegham")


print()
print(Library.books_list)
print(Library.student_list)
print(Library.book_cop)




