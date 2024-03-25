
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

   
def fill_db(db):
    db.cats.insert_many([
    {
        'name': 'Lama',
        'age': 2,
        'features': ['ходить в лоток', 'не дає себе гладити', 'сірий'],
    },
    {
        'name': 'Liza',
        'age': 4,
        'features': ['ходить в лоток', 'дає себе гладити', 'білий'],
    },
    {
        'name': 'Boris',
        'age': 12,
        'features': ['ходить в лоток', 'не дає себе гладити', 'сірий'],
    },
    {
        'name': 'Murzik',
        'age': 1,
        'features': ['ходить в лоток', 'дає себе гладити', 'чорний'],
    },
    ])

def read_all(db):
    print( list(db.cats.find()) )

def read_cat(db,name_cat):
    print( list(db.cats.find( {'name': {'$eq': name_cat}} )) )

def update_age_cat(db,name_cat,age):
    db.cats.update_one({'name': name_cat}, {'$set': {'age': age}}, True)

def update_feature_cat(db,name_cat,feature):
    db.cats.update_one({'name': name_cat}, {'$push': {'features': feature}}, True)

def delete_cat(db,name_cat):
    db.cats.delete_one({"name": name_cat})

def delete_all(db):
    db.cats.delete_many({})

if __name__ == "__main__": 
    
    uri = "mongodb+srv://user:mysecretpassword@cluster0.bb7cstx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"    
    
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client.cats
    try:
        fill_db(db)
        read_all(db)
        read_cat(db,"Boris")
        update_age_cat(db,"Boris",5)
        update_feature_cat(db,'Boris',"розумняка")
        delete_cat(db,"Boris")
        delete_all(db)
        q=0
    except Exception as e:
        print(e)        