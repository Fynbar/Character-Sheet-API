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
        self.history = []


global_history = DiceHistory()


class DiceRoller(MethodView):
    def get(self):
        return jsonify(global_history.history)

    def post(self):
        # console.log()
        req_data = request.get_json()
        print(req_data)
        d = Dice(**req_data).rolls()
        global_history.history.append(d)
        return jsonify(d)

class StringRoller(MethodView):
    def get(self, dieString=""):
        # req_data = request.get_json()
        print(dieString)
        if dieString != "":
            s = stringDie(dieString)
            s.total()
            id = len(global_history.history)+1
            d = {'die':s.toDict(), 'id':id}    
            global_history.history.append(d)
            return jsonify(d)
        else:
            return jsonify(global_history.history)

    def post(self):
        # console.log()
        req_data = request.get_json()
        print(req_data)
        id = len(global_history.history)+1
        d = {'die':stringDie(req_data['string']), 'id':id}
        global_history.history.append(d)
        return jsonify(d)