from helpers.dbConnect import bookCollection


def get_book_price(title):
    try:
        book = bookCollection.find_one({"title": title}, {"_id": 0, "price": 1})

        if book:
            return book.get("price", "Price not available")
        else:
            return "Book not found"
    except Exception as e:
        print(e)
