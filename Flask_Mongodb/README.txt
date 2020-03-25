config.py -> contains information about connection parameters, user should define env
	     variables 'MONGO_USER' and 'MONGO_PWD', or the default values will be used 
	     (username:'svetlana',passowrd:'cisco123').

database_creator -> used for creating and filling database with data. Schema is defined
		    here too. Must be run first.

flask_app -> flask application, using mongo database created in database_creator and info from config.py
	     for building mongo url. Here additional validation is done with marshmallow module.


templates -> folder that contains html files
 