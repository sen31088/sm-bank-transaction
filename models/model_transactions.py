from config import DB_Config
import pymongo

db_name = DB_Config.db_name


class Usertranscation():
    def __init__(self):
        self.db = db_name

    def get_data(self, collection_name):
        collection = self.db[collection_name]
        users = collection.find()
        return list(users)
    
    def find_and_sort_documents(self, collection_name, user_session, limit1=10):
        collection = self.db[collection_name]
        cursor = collection.find({'userid':user_session},{"TransID","Fromaccname","Fromaccno","Toaccno","Amount","Transtype","Date","Time","Accbal"},   sort=[( '_id', pymongo.DESCENDING )] ).limit(limit1)
        return list(cursor)
    
    def find_user_transcations(self, collection_name, datetime, search_year, search_month, search_date ):
        collection = self.db[collection_name]
        cursor = collection.find({ "Transdate": {"$gt": datetime(search_year, search_month, search_date)}}, {"TransID","Fromaccname","Fromaccno","Toaccno","Amount","Transtype","Date","Time","Accbal"})
        return list(cursor)

    def save(self, collection_name, data):
        collection = self.db[collection_name]
        return collection.insert_one(data)

class Userdata:
    collection = DB_Config.col_userdata

    @classmethod
    def save(cls, data):
        return cls.collection.insert_one(data)

    @classmethod
    def get_data(cls, data):
        return dict(cls.collection.find(data))
    
    
    @classmethod
    def get_userdata(cls, userid, idvalue):
        query = {userid: idvalue}
        #return dict(cls.collection.find_one({"userid":userid,"Accno":accno}))
        return cls.collection.find_one(query)
    
        
    @classmethod
    def get_data_one(cls, data):
        return dict(cls.collection.find_one(data))
    
    @classmethod
    def update(cls, data, updatedata):
        return cls.collection.update_one(data, updatedata)
    
    @classmethod
    def find_and_sort_documents(cls, sort_field='_id', sort_order= -1, limit1=1):
        cursor = cls.collection.find().sort(sort_field, sort_order).limit(limit1)
        return list(cursor)
    
    @classmethod
    def get_acc_data(cls, data):
        output = cls.collection.find(data)
        if output:
            return list(output)
        else:
            return 0