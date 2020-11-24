import pymongo
from pymongo import MongoClient

def get_mongodb_uri() -> str:
    with open('tokens/mongodb_url.key', 'r') as f:
        data = f.read()

    return data


cluster = MongoClient(get_mongodb_uri())

db = cluster['uncledunk']
economy_collection = db['economy']
settings_collection = db['settings']