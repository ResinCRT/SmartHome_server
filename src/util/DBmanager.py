import pymongo
import json

class MongoManager:
    def __init__(self, host, port=27017):
        self.host = host
        self.port = port
        self.connect_db()
        self.db_client = None

    def connect_db(self):
        self.db_client = pymongo.MongoClient(f"mongodb://{self.host}:{self.port}/")
        print(self.db_client)

    def print_db(self):
        db_test = self.db_client['testDB']
        collections = db_test['test'].find()
        print(collections)
        for x in collections:
            print(x)
            print(type(x))

class MongoObject:
    def __init__(self, client, db, collections="all"):
        self.client = client
        self.db = db
        self.collections = collections

    def store_DB(self, client, userdata, msg):
        message = str(msg.payload)

        dict_data = {"client": str(client),
                     "userdata": str(userdata),
                     "msg": message}

        cli = self.client[self.db][self.collections]
        print(cli.insert_one(dict_data))



if __name__ == "__main__":
    manager = MongoManager("192.168.0.20")
    test_module = MongoObject(manager, "testDB", "test2")
    manager.print_db()




