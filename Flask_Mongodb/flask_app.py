from flask import Flask, render_template, json,request, jsonify
from flask_pymongo import PyMongo
from pymongo import ReturnDocument
from bson import json_util
from marshmallow import Schema, fields, validate, ValidationError
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import config

app = Flask(__name__)
print(config.mongo_url)
app.config['MONGO_URI'] = config.mongo_url
mongo = PyMongo(app)

json.dumps = json_util.dumps


def validate_state(stat):
    if stat not in ['up','down','Up','Down','Err-disabled']:
        raise ValidationError('State must be one of the following values: "up", "Up","Down" or "down"')


class InterfaceSchema(Schema):
    Switch_Name = fields.String(required = True, validate=validate.Range(min=3, max=30))
    Interface_Name = fields.String(required = True, validate=validate.Range(min=3, max=30))
    Description = fields.String(validate=validate.Length(max=100))
    State = fields.String(validate=validate_state)


@app.route('/<switch_name>/interfaces.html',methods=['GET'])
def get_interfaces_html(switch_name):
    if not request.accept_mimetypes.accept_html:
        return 'You do not support html',406
    mongo_filter = {'Switch_Name':switch_name}
    try:
        result = mongo.db.Interfaces.find(mongo_filter)
        return render_template('interfaces.html', result=result)
    except ServerSelectionTimeoutError:
        return 'Can not connect to the mongodb server', 500


@app.route('/<switch_name>/interfaces.json',methods=['GET'])
def get_interfaces_json(switch_name):
    if not request.accept_mimetypes.accept_json:
        return 'You do not support json',406
    mongo_filter = {'Switch_Name':switch_name}
    try:
        result = mongo.db.Interfaces.find(mongo_filter)
        return jsonify(result)
    except ServerSelectionTimeoutError:
        return 'Could not connect to the mongodb server', 500


@app.route('/<switch_name>/<path:interface_name>/details.html',methods=['GET']) #path type is used because interface could contain "/" e.g. 'fa0/1'
def get_interface_details_html(switch_name, interface_name):
    if not request.accept_mimetypes.accept_html:
        return 'You do not support html',406
    mongo_filter = {'Switch_Name': switch_name, 'Interface_Name':interface_name}
    try:
        result = mongo.db.Interfaces.find_one(mongo_filter)
        if result:
            return render_template('interface.html', result=result)
        return '<h1>Could not find wanted interface</h1>', 400
    except ServerSelectionTimeoutError:
        return 'Could not connect to the mongodb server', 500


@app.route('/<switch_name>/<path:interface_name>/details.json',methods=['GET'])
def get_interface_details_json(switch_name, interface_name):
    if not request.accept_mimetypes.accept_json:
        return 'You do not support json format',406
    mongo_filter = {'Switch_Name': switch_name, 'Interface_Name':interface_name}
    try:
        result = mongo.db.Interfaces.find_one(mongo_filter)
        if result:
            return jsonify(result)
        return '<h1>Could not find wanted interface</h1>', 400
    except ServerSelectionTimeoutError:
        return 'Could not connect to the mongodb server', 500


@app.route('/<switch_name>/<ObjectId:_id>' ,methods=['PATCH'])
def update_interface(switch_name,_id):
    payload = request.get_json()
    if payload:
        try:
            validation_result = InterfaceSchema().load(payload,partial = True)
            mongo_result = mongo.db.Interfaces.find_one_and_update(
            {'_id':_id,
             'Switch_Name':switch_name},
            {'$set':validation_result},
             return_document = ReturnDocument.AFTER
            )
            if mongo_result:
                return jsonify(mongo_result), 200

        except ValidationError as err:
            return jsonify(err.messages), 400
        except ServerSelectionTimeoutError:
            return 'Could not connect to the mongodb server', 500
        except OperationFailure as err: #in the case that mongodb validation has failed
            return jsonify(err.details), 400
    return 'There is no request body', 400


if __name__=='__main__':
    app.run()






