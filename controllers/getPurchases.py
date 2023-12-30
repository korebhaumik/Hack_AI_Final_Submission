from helpers.dbConnect import purchasesCollection

def get_top5_recent_purchases():
    try:
        cursor = purchasesCollection.find().sort("datetime", -1).limit(5)
        recent_purchases = list(cursor)
        return recent_purchases
    except Exception as e:
        print(e)
