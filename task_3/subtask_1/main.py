from enum import Enum
from abc import ABC, abstractmethod


class ItemStatus(Enum):
    AVAILABLE = "AVAILABLE"
    CHECKED_OUT = "CHECKED_OUT"
    LOST = "LOST"


class LibraryItem(ABC):
    _item_types = {}

    def __init__(self, title):
        self.title = title
        self._status = ItemStatus.AVAILABLE         #note to self "1"

    
    def checkout(self):
        if self._status == ItemStatus.AVAILABLE:
            self._status = ItemStatus.CHECKED_OUT
        else:
            raise ValueError("Item is not available")
    
    

    def return_item(self):
        if self._status == ItemStatus.CHECKED_OUT:
            self._status = ItemStatus.AVAILABLE
        else:
            raise ValueError("Item wasn't checked out")


    def mark_lost(self):
        if self._status == ItemStatus.LOST:
            raise ValueError("Item is already lost")

        else:
            self._status = ItemStatus.LOST

    def set_status(self, status):
        self._status = ItemStatus[status]

    @classmethod
    def from_dict(cls, items):
        item_type = cls._item_types[items["type"]]
        new_item = item_type.from_dict(items)
        
        if "status" in items:
            new_item.set_status(items["status"])

        return new_item


    def __str__(self):
        return f"{self.title} type: {self.__class__.__name__} is {self._status.value}"

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title})"
    
    def __lt__(self, second):
        return self.title < second.title


    @property
    @abstractmethod
    def loan_period(self):
        pass



class Book(LibraryItem):
    def __init__(self, title, author, isbn):
        super().__init__(title)  
        self.author = author
        self.isbn = isbn
    
    @classmethod
    def from_dict(cls, items):
        return cls(items["title"],items["author"],items["isbn"])
        
     #ISBN 13
    @staticmethod
    def is_valid_isbn(isbn):
        if len(isbn) != 13:
            return False

        total = 0

        for i in range(12):
            if i % 2 == 0:
                total += int(isbn[i])
            else:
                total += int(isbn[i]) * 3

        check_digit = (10 - (total % 10)) % 10
        return check_digit == int(isbn[12])        

    @property
    def loan_period(self):
        return 21



class DVD(LibraryItem):
    def __init__(self, title, director):
        super().__init__(title)
        self.director = director

    @classmethod
    def from_dict(cls, items):
        return cls(items["title"], items["director"])
   
    @property
    def loan_period(self):
        return 5




class Magazine(LibraryItem):
    def __init__(self, title, issue):
        super().__init__(title)
        self.issue = issue

    @classmethod
    def from_dict(cls, items):
        return cls(items["title"],items["issue"])
        
    @property
    def loan_period(self):
        return 14
    
class Library:
    def __init__(self):
        self.items = []
    def add_item(self, item):
        self.items.append(item)
    def checkout(self, title):
        for item in self.items:
            if item.title == title:
                item.checkout()
                return
        raise ValueError("Item not found")

    def return_item(self, title):
        for item in self.items:
            if item.title == title:
                item.return_item()
                return

        raise ValueError("Item not found")


    def mark_lost(self, title):
        for item in self.items:
            if item.title == title:
                item.mark_lost()
                return

        raise ValueError("Item not found")
    
    def find_title(self, title):
        for item in self.items:
            if item.title == title:
                return item

        return None
   
    def list_available(self):
        available_items = []

        for item in self.items:
            if item._status == ItemStatus.AVAILABLE:
                available_items.append(item)

        return available_items




class Database:
    def __init__(self):
        self.filename = "database.txt"
    
    def save(self, items):
        with open(self.filename, "w") as file:
            for item in items:
                data = {"type": type(item).__name__,"title": item.title, "status": item._status.value}

                for key, value in vars(item).items():
                    if key != "_status" and key != "title":
                        data[key] = value

                line = "|".join(f"{key}={value}" for key, value in data.items())
                file.write(line + "\n")


    def load(self):
        items = []

        with open(self.filename, "r") as file:
            for line in file:
                data = {}

                parts = line.strip().split("|")

                for part in parts:
                    key, value = part.split("=")
                    data[key] = value

                item = LibraryItem.from_dict(data)
                items.append(item)

        return items


LibraryItem._item_types = {  "Book": Book,   "DVD": DVD,  "Magazine": Magazine}


print("\n--- FINAL TEST ---")

book_data = {
    "type": "Book",
    "title": "Dune",
    "author": "Frank Herbert",
    "isbn": "9780441013593",
    "status": "AVAILABLE"
}

dvd_data = {
    "type": "DVD",
    "title": "Inception",
    "director": "Christopher Nolan",
    "status": "CHECKED_OUT"
}

magazine_data = {
    "type": "Magazine",
    "title": "National Geographic",
    "issue": "2026-08",
    "status": "AVAILABLE"
}

book = LibraryItem.from_dict(book_data)
dvd = LibraryItem.from_dict(dvd_data)
magazine = LibraryItem.from_dict(magazine_data)

print(book)
print(dvd)
print(magazine)

print("\n--- LOAN PERIODS ---")
print(book.loan_period)
print(dvd.loan_period)
print(magazine.loan_period)

print("\n--- SORTING ---")
items = [book, dvd, magazine]
print(sorted(items))

print("\n--- ISBN ---")
print(Book.is_valid_isbn("9780441013593"))
print(Book.is_valid_isbn("1234567890123"))

print("\n--- DATABASE ---")
database = Database()
database.save(items)

loaded_items = database.load()

for item in loaded_items:
    print(item)




