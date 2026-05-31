from pymongo import MongoClient

uri = "mongodb+srv://smarttour:smarttour@cluster0.gugbbt2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

print(client.admin.command("ping"))