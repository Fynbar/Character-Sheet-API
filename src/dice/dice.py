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
    # req_data = request.get_json()
    filemane = 'Saved Files/{}.json'.format(name)
    with open(filemane, 'w') as json_file:
        # print(req_data)
        # print(req_data['name'])
        # print(jsonify(req_data))
        json.dump(data, json_file)
def jsonRead(name):
    # req_data = request.get_json()
    filename = 'Saved Files/{}.json'.format(name)
    with open(filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


class Dice(object):
    def __init__(self, dice, reroll=[], highest=0, lowest=0):
        print(dice, reroll, highest, lowest)
        self.dice = dice
        # self.diceType = diceType
        # self.diceNum = diceNum
        self.reroll = reroll
        self.results = []
        self.total = 0
        self.range = [highest, lowest]

    def rolls(self):
        self.results = [self.roll() for _ in range(self.dice["diceNum"])]
        # self.results.sort()
        self.total = (
            sum(
                self.results[self.range[0] : -1 * self.range[1]]
                if self.range[1] > 0
                else self.results[self.range[0] :]
            )
            + self.dice["constant"]
        )
        return {"dice": self.dice, "rolls": self.results, "total": self.total}

    def roll(self):
        r = random.randint(1, self.dice["diceType"])
        return r if r not in self.reroll else self.roll()

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