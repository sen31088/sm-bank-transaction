import os
import pymongo
from dotenv import  load_dotenv

class DB_Config:
    
    load_dotenv()
    
    if not os.getenv("MONGO_USER") and not os.getenv("MONGO_PASS"):
        DB_URL = f"mongodb://{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"
    else:
        DB_URL= f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"


    DB_NAME = os.getenv("MONGO_DB")

    db_con = pymongo.MongoClient(DB_URL)

    db_name = db_con[DB_NAME]

    col_userdata = db_name['userdata']

    col_admindata = db_name['admindata']

    col_transactions = db_name['transaction']


