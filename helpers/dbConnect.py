from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import find_dotenv, load_dotenv
import pymongo


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
MONGOURI = os.environ.get("MONGOURI")

print(MONGOURI)

# Create a new client and connect to the server
client = MongoClient(MONGOURI, server_api=ServerApi("1"))

print("connecting to mongodb")

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

bookCollection = client.hackai.bookstore
purchasesCollection = client.hackai.purchases
