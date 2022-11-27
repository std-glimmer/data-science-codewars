from pymongo import MongoClient

# Предпочитаемые языки программирования в зависимости от ранга
def get_database():
   client = MongoClient("mongodb://root:qwerty@45.12.18.238:27019/?authMechanism=DEFAULT")
   return client["codewars"]

def get_users_cursor():
   db = get_database()
   collection = db['users']
   return collection.find({})

def get_katas_cursor():
   db = get_database()
   collection = db['katas']
   return collection.find({})

def selectKata(id):
   db = get_database()
   collection = db['katas']
   return collection.find_one({'id' : id })