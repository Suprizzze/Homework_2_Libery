from dataclasses import dataclass, field
from datetime import datetime
from string import ascii_letters, digits
import random
from Verify import Verify


class IdRandomMIx:  # generates id
    letters = ascii_letters + digits

    @classmethod
    def rand_id(cls):
        id_r = ""
        for i in range(2, 12):
            id_r += random.choice(cls.letters)
            if i % 4 == 0:
                id_r += "-"
        return id_r


@dataclass
class Students:
    _name: str
    _surname: str
    _email: str
    _stud_id: str = IdRandomMIx.rand_id()
    book_c: list = field(default_factory=list, repr=False)
    _stud_stat: int = 10
    _count_limit: int = 0
    _limit: int = 5
    _b_time: str | datetime = None

    def take_book(self, book_copy, date):
        if len(self.book_c) == self._limit:
            raise Exception("exceeded the limit")
        title_name = [j.book_title for j in [i for i in self.book_c]]
        if not isinstance(date, tuple):
            raise TypeError("Should be a tuple with date - example (0000, 0, 0)")
        if book_copy.status != "Available":
            raise Exception("Another student has already taken this book!")
        if book_copy.title in title_name:
            raise TypeError("the student already has such a book")
        if self.stud_stat == 0:
            raise Exception("Cannot pick up the book, decency = 0")
        self._b_time = datetime(*date)
        self.book_c.append(book_copy)
        self._count_limit += 1
        if book_copy in self.book_c:
            book_copy.status = f"Took student with id = {self.stud_id}, book date = {self._b_time.date()}"

    def back_book(self, book_copy):
        if book_copy in self.book_c:
            book_copy.status = "Available"
            self.book_c.remove(book_copy)
            self._count_limit -= 1
            if (datetime.today() - self._b_time).days > 14:
                late = (datetime.today() - self._b_time).days
                self._stud_stat = 0
                self._b_time = "None"
                return f"The student was {late} days late with the book, the student's decency = 0"

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
        return self._limit

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


@dataclass
class Book:
    _title: str
    _authors: str
    _year: int
    _ISBN: str
    genre: str
    list_book: list = field(default_factory=list, repr=False)
    _id_book: str = IdRandomMIx.rand_id()

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


@dataclass
class BookCopy:
    book: Book = field(repr=False)
    state: int
    title: str = ""
    copy_id: str = IdRandomMIx.rand_id()
    status: str = "Available"

    def __post_init__(self):
        self.title = self.book.title


class Library:  # library class - stores books, installs books, students - you can search in the lists you need
    name_lib = "Good Library"
    student_list = []
    books_list = []
    book_cop = []

    @staticmethod
    def change_stud_limit(stud, limit):  # changes the limit of books for student
        stud.limit = limit

    @classmethod
    def enter_studs(cls, *args):  # adds students to the library
        cls.student_list += list([i for i in args])

    @classmethod
    def enter_book(cls, *args):  # adds books to the library
        cls.books_list += list([i for i in args])

    @classmethod
    def enter_book_copy(cls, *args):  # adds copybooks to the library
        cls.book_cop += list([i for i in args])

    @classmethod
    def search_book(cls, word):  # search for the required word in the list of books and returns the found ones
        for_search = []
        for i in cls.books_list:
            if word in str(i):
                for_search.append(i)
        print(*for_search, sep="\n")

    @classmethod
    def search_copy_book(cls, word):  # search for the required word in the list of copybooks and returns the found ones
        for_search = []
        for i in cls.book_cop:
            if word in str(i):
                for_search.append(i)
        print(*for_search, sep="\n")

    @classmethod
    def search_student(cls, word):  # search for the required word in the list of students and returns the found ones
        for_search = []
        for i in cls.student_list:
            if word in str(i):
                for_search.append(i)
        print(*for_search, sep="\n")

    @classmethod
    def find_all_free_books_copy(cls):  # shows all available book copies
        for_search = []
        for i in cls.book_cop:
            if "Available" in str(i):
                for_search.append(i)
        print(*for_search, sep="\n")


book1 = Book("Fluent Python: Clear, Concise", "Luciano Ramalho", 2015, "978-0-1323-5088-4", "Education")
book2 = Book("Clean Code: A Handbook of Agile Software Craftsmanship", " Martin Robert", 2008,
             "978-5-4461-1852-6", "Education")


# создаем студентов
stud1 = Students("Vram", "Torosyan", "vram_torosyan@mail.ru")
stud2 = Students("Gegham", "Petrosyan", "Gegham_petrosyan@gmail.com")

Library.change_stud_limit(stud1, 4)

# here we add a copy of the books to the list

book1.list_book.append(book1_ekz1 := BookCopy(book1, 6))
book1.list_book.append(book1_ekz2 := BookCopy(book1, 4))
book2.list_book.append(book2_ekz1 := BookCopy(book2, 9))
book2.list_book.append(book2_ekz2 := BookCopy(book2, 7))


stud2.take_book(book2_ekz1, (2000, 4, 23))  # student takes a book


#  stud1.back_book(book1_ekz1) the student returned the book

# if you return the book later than 14 days, then the student's decency will become = 0
# and the student will not be able to take more books


#  added to the Library of Books, Students and copy Books list
Library.enter_book(book1, book2)
Library.enter_studs(stud1, stud2)
Library.enter_book_copy(book1_ekz1, book1_ekz2, book2_ekz1, book2_ekz2)

Library.search_book("Python")
Library.search_copy_book("6")
Library.search_student("Vram")
print()
Library.find_all_free_books_copy()  # shows all available books
