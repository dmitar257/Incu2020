import os


default_username = 'svetlana'
default_password = 'cisco123'

username = os.getenv('MONGO_USER',default_username)
password = os.getenv('MONGO_PWD',default_password)

host = 'localhost'
port = '27017'
database = 'Device_Configuration'
auth_source = database
mongo_url = 'mongodb://'+ username + ':' + password + '@' + host + ':' + port + \
            '/' + database
