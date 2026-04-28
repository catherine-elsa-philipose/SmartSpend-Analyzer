 
from pymongo import MongoClient

def save_to_mongodb(data):
    """
    Saves cleaned receipt data into MongoDB 'smartspend' database, 'receipts' collection
    """
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["smartspend"]
        receipts_collection = db["receipts"]
        result = receipts_collection.insert_one(data)
        print(f"✅ Data inserted with ID: {result.inserted_id}")
    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")
