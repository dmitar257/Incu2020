import os
import pymongo

default_username = 'svetlana'
default_password = 'cisco123'

if 'MONGO_USER' in os.environ and 'MONGO_PWD' in os.environ:
    username = os.getenv('MONGO_USER')
    password = os.getenv('MONGO_PWD')
else:
    username = default_username
    password = default_password

host = 'localhost'
port = '27017'
database = 'Device_Configuration'
mongo_url = 'mongodb://'+ username + ':' + password + '@' + host + ':' + port


auth_source = ''
with pymongo.MongoClient(mongo_url) as client:
    dbnames = client.list_database_names()
    for db_name in dbnames:
        res = client[db_name].command({'usersInfo': {'user': username,'db':db_name}})
        if len(res['users']) > 0 :
            auth_source = db_name
            break
if auth_source != '':
    mongo_url += "/"+database+'?authSource='+db_name
else:
    mongo_url += "/"+database




