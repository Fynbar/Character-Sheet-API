# from flask.json import jsonify
# from flask_restful import Resource
# , Api
from flask.views import MethodView
import json
from flask import request, make_response
from flask.json import jsonify
import random
# from flask_restful import Resource
# , Api
from dice.stringDie import stringDie
# from json_save.json_save import jsonRead, jsonWrite

def jsonWrite(name, data):
    filename = 'Saved Files/{}.json'.format(name)
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)

def jsonRead(name):
    filename = 'Saved Files/{}.json'.format(name)
    with open(filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


class DiceHistory(object):
    def __init__(self):
        self.history = jsonRead("history")
    def createId(self):
        id = len(list(self.history.keys()))+1
        return id
    def rollDie(self, string):
        id = hex(self.createId())[2:]
        dice = stringDie(string)
        dice.total()
        d = {'die':dice.toDict(), 'id':id, 'result':dice.value}
        self.history[id] = d
        return id


global_history = DiceHistory()


class DiceRoller(MethodView):
    def get(self):
        return jsonify(global_history.history)

    def post(self):
        # console.log()
        req_data = request.get_json()
        print(req_data)
        d = Dice(**req_data).rolls()
        # global_history.history.append(d)
        return jsonify(d)


class StringRoller(MethodView):
    def get(self, id=""):
        # req_data = request.get_json()
        print(id)
        if id == "":
            return jsonify(global_history.history)
        else:
            return jsonify(global_history.history.get(id))

    def options(self):
        print("Option:", request.get_json())
        return jsonify(0)
    def post(self):
        # console.log()
        req_data = request.get_json()
        if isinstance(req_data['string'], list):
            id = [global_history.rollDie(s) for s in req_data['string']]
        elif isinstance(req_data['string'], str):
            id = global_history.rollDie(req_data['string'])
        # s = stringDie(id)
        #     s.total()
        #     id = len(global_history.history)+1
        #     d = {'die':s.toDict(), 'id':id}    
        #     global_history.history[id] = d
        #     return jsonify(d)
        print(req_data)
        
        jsonWrite("history", global_history.history)
        print(id)
        return jsonify(id)