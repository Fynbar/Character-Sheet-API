import json
from flask import Flask, request, make_response
from flask.json import jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

# , Api
from flask.views import MethodView

# , cross_origin
# from flask.json import jsonify
# from flask.views import View, MethodView
# from pprint import pprint
from json_save.json_save import SaveJSONAPI
from dice.dice import DiceRoller

# from beam_bending.beam_bending import BeamAPI, BeamEndCondAPI
# , ThermoState



class BaseAPI(MethodView):
    def get(self):
        # print(state_id)
        return json.dumps({"text": "Hello World!"})

    def post(self):
        print(request.is_json)
        if request.is_json:
            req_data = request.get_json()
            with open("Saved Files/test.json", "w") as json_file:
                print(req_data)
                print(req_data["name"])
                print(jsonify(req_data))
                json.dump(req_data, json_file)
            return make_response(jsonify(req_data))
        else:
            return make_response(jsonify({"response": "Error non-json type"}))

    def delete(self):
        # delete a single state
        pass

    def put(self):
        # update a single state
        pass


app = Flask(__name__)
CORS(app)
app.app_context()
api = Api(app)
#
# @app.route("/")
# def hello():
#     return json.dumps({'text': 'Hello World!'})

base_view = BaseAPI.as_view("base_api")

app.add_url_rule("/", view_func=base_view, methods=["GET", "PUT", "POST", "DELETE"])


json_view = SaveJSONAPI.as_view("json_api")

app.add_url_rule(
    "/saveJSON", view_func=json_view, methods=["GET", "PUT", "POST", "DELETE"]
)


class Employees(Resource):
    def get(self):
        return {"employees": [{"id": 1, "name": "Balram"}, {"id": 2, "name": "Tom"}]}


api.add_resource(Employees, "/employees")  # Route_1



dice_view = DiceRoller.as_view("dice_view")

app.add_url_rule("/diceHistory", view_func=dice_view, methods=["POST", "GET"])

# Thermodynamic States
# state_view = StateAPI.as_view('state_api')
# app.add_url_rule('/states/', defaults={'state_id': None},
#                  view_func=state_view, methods=['GET', ])
# app.add_url_rule('/states/', view_func=state_view, methods=['POST', ])
# app.add_url_rule('/states/<int:state_id>', view_func=state_view,
#                  methods=['GET', 'PUT', 'DELETE'])
# # Api to get the max and min saturation temp
# limit_view = StateLimitAPI.as_view('limit_api')
# app.add_url_rule('/stateLimits/', defaults={'material': None},
#                  view_func=limit_view, methods=['GET', ])

# # Beam Bending
# bending_view = BeamAPI.as_view('bending_api')

# app.add_url_rule('/bendings/', view_func=bending_view, methods=['POST', ])
# app.add_url_rule('/bendings/<int:bending_id>', view_func=bending_view,
#                  methods=['GET', 'PUT', 'DELETE'])
# # Api to get the types of end conditions
# endCond_view = BeamEndCondAPI.as_view('endCond_api')

# app.add_url_rule('/beamEnds/', view_func=endCond_view, methods=['GET', ])


def readJsonFile(filename):
    try:
        with open("Saved Files/{}.json".format(filename), "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return "Sorry, but {}.json doesn't exist".format(filename)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message


s = [readJsonFile("test"), readJsonFile("test2"), readJsonFile("test3")]
# # api.add_resource(ThermoState, '/allstates') # Route_2
print("lwmon")
if __name__ == "__main__":
    print("Loading Backend...")
    [print(x) for x in s]
    app.run(port=5002)


# with open('./Saved Files/srd_5e_monsters.json') as f:
#     monsters = json.load(f)

# monster_list = []

# for i, m in enumerate(monsters):
#     m['id'] = i + 1
#     monster_list.append(SetProperties(m))

# with open('Saved Files/monster.json', 'w') as json_file:
#     json.dump(monster_list, json_file)
