import uuid
from string import ascii_letters
from pydantic import BaseModel, Field, ValidationError, validator, conint, EmailStr
from datetime import datetime


class ValidName:

    @classmethod
    def name_str_valid(cls, value):
        val = list(filter(lambda x: x not in ascii_letters, value))
        if len(val) > 0 or value != value.capitalize():
            raise TypeError("First name or last name must start with a capital letter and have only letters")
        return value

    @classmethod
    def __get_validators__(cls):
        yield cls.name_str_valid


class Students(BaseModel):
    name: ValidName
    surname: ValidName
    email: EmailStr
    stud_id: uuid.UUID = uuid.uuid4()
    book_c: list = Field(default_factory=list, repr=False)
    stud_stat: int = 10
    count_limit: int = 0
    limit: int = 5
    b_time: None | datetime = None

    def take_book(self, book_copy, date):
        if len(self.book_c) == self.limit:
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
        self.b_time = datetime(*date)
        self.book_c.append(book_copy)
        self.count_limit += 1
        if book_copy in self.book_c:
            book_copy.status = f"Took student with id = {self.stud_id}, book date = {self.b_time.date()}"

    def back_book(self, book_copy):
        if book_copy in self.book_c:
            book_copy.status = "Available"
            self.book_c.remove(book_copy)
            self.count_limit -= 1
            if (datetime.today() - self.b_time).days > 14:
                late = (datetime.today() - self.b_time).days
                self.stud_stat = 0
                self.b_time = None
                return f"The student was {late} days late with the book, the student's decency = 0"

    class Config:
        validate_assignment = True


class Book(BaseModel):
    title: str
    authors: tuple | str
    year: int
    ISBN: str
    genre: str
    list_book: list = Field(default_factory=list, repr=False)
    id_book: uuid.UUID = uuid.uuid4()


class BookCopy(BaseModel):
    book: Book = Field(repr=False)
    state: int
    title: str = ""
    copy_id: uuid.UUID = uuid.uuid4()
    status: str = "Available"

    def _init_private_attributes(self, *args, **kwargs):
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


book1 = Book(title="Fluent Python: Clear, Concise", authors="Luciano Ramalho",
             year=2015, ISBN="978-0-1323-5088-4", genre="Education")
book2 = Book(title="Clean Code: A Handbook of Agile Software Craftsmanship", authors=" Martin Robert", year=2008,
             ISBN="978-5-4461-1852-6", genre="Education")


stud1 = Students(name="Gegham", surname="Petrosyan", email="geghampetrosyan@bk.ru")
stud2 = Students(name="Vram", surname="Torosyan", email="vram_torosyan@mail.ru")


Library.change_stud_limit(stud1, 4)

# here we add a copy of the books to the list
book1.list_book.append(book1_ekz1 := BookCopy(book=book1, state=6))
book1.list_book.append(book1_ekz2 := BookCopy(book=book1, state=4))
book2.list_book.append(book2_ekz1 := BookCopy(book=book2, state=9))
book2.list_book.append(book2_ekz2 := BookCopy(book=book2, state=7))


stud2.take_book(book2_ekz1, (2000, 4, 23))  # student takes a book


#  stud1.back_book(book1_ekz1) the student returned the book

# if you return the book later than 14 days, then the student's decency will become = 0
# and the student will not be able to take more books


#  added to the Library of Books, Students and copy Books list
Library.enter_book(book1, book2)
Library.enter_studs(stud1, stud2)
Library.enter_book_copy(book1_ekz1, book1_ekz2, book2_ekz1, book2_ekz2)

Library.search_book("Python")
Library.search_copy_book("state=6")
Library.search_student("Vram")
print()
Library.find_all_free_books_copy()  # shows all available books
