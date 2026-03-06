from pymongo import MongoClient

client = MongoClient("mongodb+srv://smartour:<smartTour123>@cluster0.gugbbt2.mongodb.net/?appName=Cluster0")

db = client["smarttour"]

users = db["users"]