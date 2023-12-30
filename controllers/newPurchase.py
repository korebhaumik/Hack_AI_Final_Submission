from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from helpers.dbConnect import bookCollection, purchasesCollection


def newPurchase(
    title,
    pricePerBook,
    quantity,
    wallet_address,
    datetime,
    delivery_date,
    delivery_address,
):
    try:
        if not title or not quantity or not pricePerBook or not wallet_address:
            print("Title or Quantity or pricePerBook cannot be null or empty.")
            return

        # First, find the current quantity of the book
        book_data = bookCollection.find_one({"title": title})
        if book_data:
            current_quantity = book_data.get("quantity", 0)
            current_No_Bought = book_data.get("number_bought", 0)

            # Check if enough books are available
            if current_quantity < quantity:
                print(f"Not enough books in stock. Available: {current_quantity}")
                return

            # Update the quantity in the bookstore collection
            update_result = bookCollection.find_one_and_update(
                {"title": title},
                {
                    "$set": {
                        "quantity": current_quantity - quantity,
                        "number_bought": current_No_Bought + quantity,
                    }
                },
                return_document=ReturnDocument.AFTER,
            )

            if not update_result:
                print("Failed to update the book quantity.")
                return

            # Record the purchase
            purchase_document = {
                "title": title,
                "pricePerBook": pricePerBook,
                "quantity": quantity,
                "wallet_address": wallet_address,
                "datetime": datetime,
                "delivery_date": delivery_date,
                "delivery_address": delivery_address,
            }

            insert_result = purchasesCollection.insert_one(purchase_document)
            if insert_result.inserted_id:
                return True
            else:
                print("Failed to insert purchase document.")
                return False
        else:
            print("Failed to find the book.")
            return False
    except Exception as e:
        print(e)
