
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://smarttour:smarttour@cluster0.gugbbt2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

db = client["smarttour"]
users = db["users"]