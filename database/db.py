from pymongo import MongoClient

client = MongoClient("mongodb+srv://smarttour:smartTour123@cluster0.gugbbt2.mongodb.net/smarttour?retryWrites=true&w=majority")

db = client["smarttour"]
users = db["users"]