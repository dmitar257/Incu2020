import pymongo
import config
from collections import OrderedDict


database_name = 'Device_Configuration'
colection_name='Interfaces'
vexpr = {"$jsonSchema":
  {
         "required": ["Switch_Name", "Interface_Name", "State" ],
         "properties": {
            "Switch_Name": {
               "bsonType": "string",
               "description": "must be a string and is required",
               "minLength":3,
               "maxLength":30
            },
             "Interface_Name": {
                 "bsonType": "string",
                 "description": "must be a string and is required",
                 "minLength": 3,
                 "maxLength": 30
             },
             "Description": {
                 "bsonType": "string",
                 "maxLength": 100
             },
             "State":{
                 "enum": ["Up", "Down", "up", "down", "err-disabled"],
                 "description": "is required and it must have one of predefined values"
             }
         }
  }
}


def fill_interfaces_collection(interfaces_col):
    posts = [{
            "Switch_Name": "bru-dna-1",
            "Interface_Name": "g1/0",
            "Description": "Connected to the switch2 gi1/2",
            "State": "up"
        },{
            "Switch_Name": "bru-dna-1",
            "Interface_Name": "fc1/1/0",
            "Description": "connected to the storage port 1",
            "State": "up"
        },{
            "Switch_Name": "mastodon",
            "Interface_Name": "GigabitEthernet1/0/3",
            "Description": "Connected to printer CX2",
            "State": "up"
        },{
            "Switch_Name": "mastodon",
            "Interface_Name": "GigabitEthernet1/0/5",
            "Description": "Connected to printer CX4",
            "State": "down"
        },{
            "Switch_Name": "mastodon",
            "Interface_Name": "GigabitEthernet1/4/3",
            "Description": "Connected to server SERV1",
            "State": "up"
        }]
    interfaces_col.insert_many(posts)


with pymongo.MongoClient(config.mongo_url) as client:
    #dbnames = client.list_database_names()
    db = client['Device_Configuration']
    colection = db['Interfaces']
    if colection.count_documents({}) == 0:
        fill_interfaces_collection(colection)




