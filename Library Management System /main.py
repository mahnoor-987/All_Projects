import json
import os

class Library:
    def __init__(self, name, data_file="library_data.json"):
        self.name = name
        self.data_file = data_file
        self.books = []
        self.borrowed_books = {}
        self.load_data()

    # ---------- Book Management ----------
    def add_book(self, title, author):
        book_id = len(self.books) + len(self.borrowed_books) + 1
        book = {"id": book_id, "title": title, "author": author}
        self.books.append(book)
        print(f'📖 "{title}" by {author} added with ID {book_id}.')
        self.save_data()

    def show_books(self):
        if not self.books:
            print("❌ No books available in the library.")
        else:
            print("\n📚 Available Books:")
            for book in self.books:
                print(f'ID: {book["id"]} | {book["title"]} by {book["author"]}')

    def search_books(self, keyword):
        results = [book for book in self.books if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower()]
        if results:
            print("\n🔍 Search Results:")
            for book in results:
                print(f'ID: {book["id"]} | {book["title"]} by {book["author"]}')
        else:
            print("❌ No matching books found.")

    # ---------- Borrow & Return ----------
    def borrow_book(self, book_id, user):
        for book in self.books:
            if book["id"] == book_id:
                self.books.remove(book)
                self.borrowed_books[book_id] = {"book": book, "user": user}
                print(f'✅ {user} borrowed "{book["title"]}".')
                self.save_data()
                return
        print("❌ Book not available.")

    def return_book(self, book_id, user):
        if book_id in self.borrowed_books and self.borrowed_books[book_id]["user"] == user:
            book = self.borrowed_books[book_id]["book"]
            self.books.append(book)
            del self.borrowed_books[book_id]
            print(f'🔄 {user} returned "{book["title"]}".')
            self.save_data()
        else:
            print("❌ This book was not borrowed by you.")

    def show_borrowed_books(self):
        if not self.borrowed_books:
            print("📂 No borrowed books currently.")
        else:
            print("\n📂 Borrowed Books:")
            for book_id, record in self.borrowed_books.items():
                book = record["book"]
                user = record["user"]
                print(f'ID: {book_id} | "{book["title"]}" by {book["author"]} → Borrowed by {user}')

    # ---------- File Handling ----------
    def save_data(self):
        data = {"books": self.books, "borrowed_books": self.borrowed_books}
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.books = data.get("books", [])
                self.borrowed_books = data.get("borrowed_books", {})


# Main Program
def main():
    library = Library("City Library")

    while True:
        print("\n" + "="*40)
        print(f"📚 Welcome to {library.name} 📚")
        print("="*40)
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. View Borrowed Books")
        print("7. Exit")

        choice = input("👉 Enter your choice (1-7): ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            library.add_book(title, author)

        elif choice == "2":
            library.show_books()

        elif choice == "3":
            keyword = input("Enter keyword (title/author): ")
            library.search_books(keyword)

        elif choice == "4":
            try:
                book_id = int(input("Enter book ID to borrow: "))
                user = input("Enter your name: ")
                library.borrow_book(book_id, user)
            except ValueError:
                print("❌ Invalid ID. Please enter a number.")

        elif choice == "5":
            try:
                book_id = int(input("Enter book ID to return: "))
                user = input("Enter your name: ")
                library.return_book(book_id, user)
            except ValueError:
                print("❌ Invalid ID. Please enter a number.")

        elif choice == "6":
            library.show_borrowed_books()

        elif choice == "7":
            print("👋 Exiting Library System. Goodbye!")
            break

        else:
            print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
